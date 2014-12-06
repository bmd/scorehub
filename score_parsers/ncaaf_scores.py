import re
import requests


from score_parsers.common import group


def get_ncaaf_scores():
    raw = process_raw_game_data('http://sports.espn.go.com/ncf/bottomline/scores')
    gs = {'complete': [], 'inprogress': [], 'unplayed': []}
    for game in raw:
        t = determine_game_type(game[0])
        if t in ['complete', 'inprogress']:
            gs[t].append(parse_in_progres_or_finished_game(game[0], game[1]))
        else:
            gs[t].append(parse_future_game(game[0], game[1]))
    return gs


def process_raw_game_data(fetch_url):
    # request raw data from ESPN url
    r = requests.get(fetch_url)
    # do some heavy-duty cleanup
    encoded = [e.replace('%26', '&') for e in r.text.replace('%20', ' ').split('&') if re.match('^ncf_s_(left|right|url)[0-9]+=.*', e)]
    # group the strings into games
    return [list(e) for e in group(2, encoded)]


def determine_game_type(gamestring):
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


def parse_in_progres_or_finished_game(gamestring, gamelink):
    game_record = re.compile('(?:.*=)(\^)?(\(\d{1,2}\))?([^0-9]+)(\d{1,2})(?: {3})(\^)?(\(\d{1,2}\))?([^0-9]+)(\d{1,2}).*(\(.*\))')
    #game_link = re.compile('^(?:.*=)(.*)')
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
        'status': g[8],
        'score_link': url
    }
    return game


def parse_future_game(gamestring, gamelink):
    game_record = re.compile('(?:.*\=)(\(\d{1,2}\))?(.*)(?:\ at\ )(\(\d{1,2}\))?(.*)(\(.*\))')
    game_link = re.compile('^(?:.*=)(.*)')
    m = game_record.match(gamestring)
    g = m.groups()
    m2 = game_link.match(gamelink)
    url = 'http://sports.espn.go.com/ncf/boxscore?gameId=' + m2.groups()[0]
    game = {
        'away': {
            'team': g[1].strip(),
            'ranked': int(g[0].replace('(', '').replace(')', '')) if g[0] else False
        },
        'home': {
            'team': g[3].strip(),
            'ranked': int(g[2].replace('(', '').replace(')', '')) if g[2] else False
        },
        'status': '',
        'score_link': url
    }
    return game