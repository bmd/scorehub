from itertools import izip, chain, repeat
import requests
import re
from abc import abstractmethod


class BaseParser(object):
    def group(self, n, iterable, padvalue=None):
        return izip(*[chain(iterable, repeat(padvalue, n - 1))] * n)

    @abstractmethod
    def get_scores_json(self):
        raise NotImplementedError


class NcaafParser(BaseParser):
    def __init__(self):
        self.data_url = 'http://sports.espn.go.com/ncf/bottomline/scores'
        self.box_score_url = 'http://sports.espn.go.com/ncf/boxscore?gameId={game_id}'

    def get_scores_json(self):
        data = self._get_web_data(self.data_url)
        return self._parse_ncaaf_scores(data)

    def _get_web_data(self, fetch_url):
        # request raw data from ESPN url
        r = requests.get(fetch_url)
        # do some heavy-duty cleanup
        encoded = [e.replace('%26', '&') for e in r.text.replace('%20', ' ').split('&') if
                   re.match('^ncf_s_(left|right|url)[0-9]+=.*', e)]
        # group the strings into games
        return [list(e) for e in self.group(2, encoded)]

    def _parse_ncaaf_scores(self, raw):
        games = []
        for game in raw:
            game_type = self._determine_game_type(game[0])
            if game_type in ['complete', 'inprogress']:
                games.append(self._parse_in_progres_or_finished_game(game[0], game[1]))
            else:
                games.append(self._parse_future_game(game[0], game[1]))
        return games

    def _determine_game_type(self, gamestring):
        # set up regex to determine type
        complete = re.compile('.*\(FINAL.*\) ?$')
        to_play = re.compile('.*\((SAT|SUN|MON|TUE|WED|THU|FRI).*\)$')
        # make type determination
        if to_play.match(gamestring):
            return 'unplayed'
        elif complete.match(gamestring):
            return 'complete'
        else:
            return 'inprogress'

    def _parse_in_progres_or_finished_game(self, gamestring, gamelink):
        game_record = re.compile(
            '(?:.*=)(\^)?(\(\d{1,2}\))?([^0-9]+)(\d{1,2})(?: {3})(\^)?(\(\d{1,2}\))?([^0-9]+)(\d{1,2}).*(\(.*\))')
        # game_link = re.compile('^(?:.*=)(.*)')
        m = game_record.match(gamestring)
        g = m.groups()
        m2 = re.match('^(?:.*=)(.*)', gamelink)
        url = 'http://sports.espn.go.com/ncf/boxscore?gameId=' + m2.groups()[0]
        game = {
            'away': {
                'winner': True if g[0] else False,
                'ranked': int(g[1].replace('(', '').replace(')', '')) if g[1] else False,
                'team': g[2].strip(),
                'score': int(g[3].strip())
            },
            'home': {
                'winner': True if g[4] else False,
                'ranked': int(g[5].replace('(', '').replace(')', '')) if g[5] else False,
                'team': g[6].strip(),
                'score': int(g[7].strip())
            },
            'status': g[8].strip('(').strip(')'),
            '_links': {
                'score': {
                    'href': self.box_score_url.format(game_id=m2.groups()[0])
                }
            }
        }
        return game

    def _parse_future_game(self, gamestring, gamelink):
        game_record = re.compile('(?:.*=)(\(\d{1,2}\))?(.*)(?:\ at\ )(\(\d{1,2}\))?(.*)(\(.*\))')
        game_link = re.compile('^(?:.*=)(.*)')
        m = game_record.match(gamestring)
        g = m.groups()
        m2 = game_link.match(gamelink)
        game = {
            'home': {
                'team': g[3].strip(),
                'rank': int(g[2].replace('(', '').replace(')', '')) if g[2] else False
            },
            'away': {
                'team': g[1].strip(),
                'rank': int(g[0].replace('(', '').replace(')', '')) if g[0] else False
            },

            'status': '',
            '_links': {
                'score': {
                    'href': self.box_score_url.format(game_id=m2.groups()[0])
                }
            }
        }
        return game


class NcaabParser(BaseParser):
    def __init__(self):
        self.data_url = 'http://sports.espn.go.com/ncb/bottomline/scores'
        self.box_score_url = 'http://sports.espn.go.com/ncb/boxscore?gameId={game_id}'
