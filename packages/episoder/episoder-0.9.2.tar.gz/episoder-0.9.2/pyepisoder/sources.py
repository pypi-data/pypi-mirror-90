# episoder, https://code.ott.net/episoder
#
# Copyright (C) 2004-2021 Stefan Ott. All rights reserved.
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import logging
from sys import stderr

from bs4 import BeautifulSoup
from re import search, match
from json import dumps
from datetime import datetime

import requests

from .database import Episode, Show


class ParserSelector(object):

    class _Inner(object):

        def __init__(self):

            self._tvdb = TVDB()
            self._epguides = Epguides()
            self._tvcom = TVCom()

        def parser_for(self, url):

            for parser in [self._tvdb, self._epguides, self._tvcom]:
                if parser.accept(url):
                    return parser

            return None

    _instance = None

    @staticmethod
    def instance():

        if not ParserSelector._instance:
            ParserSelector._instance = ParserSelector._Inner()

        return ParserSelector._instance


class InvalidLoginError(Exception):

    pass


class TVDBShowNotFoundError(Exception):

    pass


class TVDBNotLoggedInError(Exception):

    pass


class TVDBOffline(object):

    def __init__(self, tvdb):

        self._tvdb = tvdb
        self._log = logging.getLogger("TVDB (offline)")

    def __str__(self):

        return "thetvdb.com parser (ready)"

    def __repr__(self):

        return "<TVDBOffline>"

    def _post_login(self, data, user_agent):

        url = "https://api.thetvdb.com/login"
        head = {"Content-type": "application/json",
            "User-Agent": user_agent}
        body = dumps(data).encode("utf8")
        response = requests.post(url, body, headers=head)
        data = response.json()

        if response.status_code == 401:
            raise InvalidLoginError(data.get("Error"))

        self._log.info("Successful login")
        return data.get("token")

    def lookup(self, _, __):

        raise TVDBNotLoggedInError()

    def login(self, args):

        body = {"apikey": args.tvdb_key}
        self.token = self._post_login(body, args.agent)

    def parse(self, _, __, ___):

        raise TVDBNotLoggedInError()

    def _set_token(self, token):

        self._tvdb.change(TVDBOnline(token))

    token = property(None, _set_token)


class TVDBOnline(object):

    def __init__(self, token):

        self._token = token
        self._log = logging.getLogger("TVDB (online)")

    def __str__(self):

        return "thetvdb.com parser (authorized)"

    def __repr__(self):

        return "<TVDBOnline>"

    def _get(self, url, params, agent):

        url = "https://api.thetvdb.com/%s" % url
        head = {"Content-type": "application/json",
            "User-Agent": agent,
            "Authorization": "Bearer %s" % self._token}
        response = requests.get(url, headers=head, params=params)
        data = response.json()

        if response.status_code == 404:
            raise TVDBShowNotFoundError(data.get("Error"))

        return data

    def _get_episodes(self, show, page, agent):

        show_id = int(show.url)
        opts = {"page": page}
        result = self._get("series/%d/episodes" % show_id, opts, agent)
        return (result.get("data"), result.get("links"))

    def lookup(self, term, agent):

        def mkshow(entry):

            name = entry.get("seriesName")
            url = str(entry.get("id")).encode("utf8").decode("utf8")
            return Show(name, url=url)

        matches = self._get("search/series", {"name": term}, agent)
        return map(mkshow, matches.get("data"))

    def login(self, args):

        pass

    def _fetch_episodes(self, show, page, agent):

        def airdate(row):

            aired = row.get("firstAired")

            if aired == "0000-00-00":
                return datetime(1970, 1, 1)

            return datetime.strptime(aired, "%Y-%m-%d").date()

        def mkepisode(row):

            num = int(row.get("airedEpisodeNumber", "0") or 0)
            name = row.get("episodeName") or u"Unnamed episode"
            season = int(row.get("airedSeason", "0") or 0)
            aired = airdate(row)
            pnum = u"UNK"

            self._log.debug("Found episode %s", name)
            return Episode(name, season, num, aired, pnum, 0)

        def isvalid(row):

            return row.get("firstAired") not in [None, ""]

        (data, links) = self._get_episodes(show, page, agent)
        valid = filter(isvalid, data)
        episodes = [mkepisode(row) for row in valid]

        # handle pagination
        next_ = links.get("next") or 0
        if next_ > page:
            try:
                more = self._fetch_episodes(show, next_, agent)
                episodes.extend(more)
            except TVDBShowNotFoundError:
                msg = "Error parsing %s: failed to load page %d"
                self._log.error(msg, show.name, next_)

        return episodes

    def parse(self, show, db, user_agent):

        result = self._get("series/%d" % int(show.url), {}, user_agent)
        data = result.get("data")

        # update show data
        show.name = data.get("seriesName", show.name)
        show.updated = datetime.now()

        self._log.debug("Updating show '%s'", show.name)

        if data.get("status") == "Continuing":
            show.status = Show.RUNNING
        else:
            show.status = Show.ENDED

        # load episodes
        try:
            episodes = self._fetch_episodes(show, 1, user_agent)
        except TVDBShowNotFoundError:
            #raise
            return

        for (idx, episode) in enumerate(sorted(episodes)):

            episode.totalnum = idx + 1
            db.add_episode(episode, show)

        db.commit()


class TVDB(object):

    def __init__(self):

        self._state = TVDBOffline(self)

    def __str__(self):

        return str(self._state)

    def __repr__(self):

        return "TVDB %s" % repr(self._state)

    def login(self, args):

        self._state.login(args)

    def lookup(self, text, args):

        return self._state.lookup(text, args.agent)

    def parse(self, show, db, args):

        return self._state.parse(show, db, args.agent)

    def change(self, state):

        self._state = state

    @staticmethod
    def accept(url):

        return url.isdigit()


class Epguides(object):

    def __init__(self):

        self.logger = logging.getLogger("Epguides")

    def __str__(self):

        return "epguides.com parser"

    def __repr__(self):

        return "Epguides()"

    @staticmethod
    def accept(url):

        return "epguides.com/" in url

    def login(self, args):

        pass

    def guess_encoding(self, response):

        raw = response.raw.read()
        text = raw.decode("iso-8859-1")

        if "charset=iso-8859-1" in text:
            return "iso-8859-1"

        return "utf8"

    def parse(self, show, db, args):

        headers = {"User-Agent": args.agent}
        response = requests.get(show.url, headers=headers)
        response.encoding = self.guess_encoding(response)

        for line in response.text.split("\n"):
            self._parse_line(line, show, db)

        show.updated = datetime.now()
        db.commit()


    def _html_line(self, line):

        def contents(field):
            if not len(field.contents):
                return ""
            else:
                return field.contents[0].strip()

        line = BeautifulSoup(line, "html.parser")
        epinfos = line.find_all("td", class_="epinfo")

        # We expect 3 cells, otherwise we refuse to go on
        if len(epinfos) < 3:
            return None

        total = contents(epinfos[0]).split(".",1)[0]
        try:
            total = int(total)
        except ValueError:
            # Some shows have specials (numbered separately)
            total = -1

        details = contents(epinfos[1]).split("-")
        if len(details) < 2:
            return None

        [season, epnum] = details
        day = contents(epinfos[2])
        if not day:
            # Drop episodes without date
            return None

        title = contents(line.find("td", class_="eptitle").find("a"))

        # prodnum is None, we dont' have those
        return (total, season, epnum, None, day, title)

    def _parse_line(self, line, show, db):

        # Name of the show
        res = search(r"<title>(.*)</title>", line)
        if res:
            title = res.groups()[0]
            show.name = title.split(" (a ")[0]

        # Current status (running / ended)
        res = search(r'<span class="status">(.*)</span>', line)
        if res:
            text = res.groups()[0]
            if "current" in text:
                show.status = Show.RUNNING
            else:
                show.status = Show.ENDED
        else:
            if search(r"aired.*to.*[\d+]", line):
                show.status = Show.ENDED

        # Current status in new HTML version
        res = search(r"Status: (.*)<br />", line)
        if res:
            text = res.groups()[0]
            if "ended" in text:
                show.status = Show.ENDED
            else:
                show.status = Show.RUNNING

        if search(r"<td class=.epinfo", line):
            fields = self._html_line(line)
            if fields:
                (total, season, epnum, prodnum, day, title) = fields
            else:
                return

        # Known formatting supported by this fine regex:
        # 4.     1-4        19 Jun 02  <a [..]>title</a>
        #   1.  19- 1   01-01    5 Jan 88  <a [..]>title</a>
        # 23     3-05       27/Mar/98  <a [..]>title</a>
        # 65.   17-10       23 Apr 05  <a [..]>title</a>
        # 101.   5-15       09 May 09  <a [..]>title</a>
        # 254.    - 5  05-254   15 Jan 92  <a [..]>title</a>
        else:
            res = search(r"^ *(\d+)\.? +(\d*)- ?(\d+) +([a-zA-Z0-9-]*)" \
            r" +(\d{1,2}[ /][A-Z][a-z]{2}[ /]\d{2}) *<a.*>(.*)</a>", line)

            if res:
                fields = res.groups()
                (total, season, epnum, prodnum, day, title) = fields
            else:
                return

        day = day.replace("/", " ")
        airtime = datetime.strptime(day, "%d %b %y")

        self.logger.debug("Found episode %s", title)
        db.add_episode(Episode(title, season or 0, epnum,
                airtime.date(), prodnum, total), show)

class TVCom(object):

    def __init__(self):

        self._log = logging.getLogger("TVCom")

    def __str__(self):

        return "dummy tv.com parser to detect old urls"

    def __repr__(self):

        return "TVCom()"

    @staticmethod
    def accept(url):

        exp = "http://(www.)?tv.com/.*"
        return match(exp, url)

    def parse(self, source, _, __):

        self._log.error("The url %s is no longer supported", source.url)

    def login(self):

        pass
