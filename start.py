from ast import literal_eval
from datetime import datetime, timedelta
import io
import logging
from os import environ as env
from os.path import abspath, dirname, join, realpath
from random import randint
import sys
from urllib.parse import urlparse

from flask import Flask, render_template, jsonify
from flask_htpasswd import HtPasswdAuth
from google_calendar_parser import CalendarParser
from pytz import utc
import requests
from werkzeug.contrib.cache import RedisCache, SimpleCache
import yaml

API_PREFIX = '/start-api/v1/'
BING = 'https://www.bing.com'
PATH = dirname(realpath(__file__))
CONFIG = yaml.load(io.open(join(PATH, 'data.yml'), 'r', encoding='UTF-8'))
GH_URL = 'https://api.github.com/'
GH_TOKEN = env.get('GH_TOKEN', None)
GH_HEADERS = {'Authorization': 'token {}'.format(GH_TOKEN)}
GH_USERNAME = env.get('GH_USERNAME')
GH_SEARCH_PREFIX = 'search/issues?q=state:open type:pr '
GH_SEARCHES = (
    ('review-requests', 'review-requested:{}'.format(GH_USERNAME)),
    ('changes-requested', 'review:changes_requested author:{}'.format(GH_USERNAME)),
    ('approved', 'review:approved author:{}'.format(GH_USERNAME)),
)

CAL_URLS = env.get('CAL_URLS', False)
CAL_URLS = literal_eval(CAL_URLS) if CAL_URLS else {}

CACHE_CONFIG = urlparse(env.get('REDIS_CACHE', 'redis://localhost:6379'))

# Write out htpasswd to path if environment variable set
HTPASSWD_PATH = abspath('.htpasswd')
HTPASSWD = env.get('START_HTPASSWD')
if HTPASSWD:
    with open(HTPASSWD_PATH, 'w') as wfile:
        wfile.write(HTPASSWD)

app = Flask(__name__, static_folder='./dist/static', template_folder='./dist/')
app.logger.addHandler(logging.StreamHandler(sys.stdout))
app.logger.setLevel(logging.INFO)
log = app.logger
app.config['FLASK_AUTH_ALL'] = True
app.config['FLASK_HTPASSWD_PATH'] = HTPASSWD_PATH

if env.get('USE_REDIS', False):
    cache = RedisCache(
        host=CACHE_CONFIG.hostname,
        port=CACHE_CONFIG.port,
        password=CACHE_CONFIG.password,
        db=CACHE_CONFIG.path[1:]
    )
else:
    cache = SimpleCache()

htpasswd = HtPasswdAuth(app)


def rando(list_like):
    """
    Returns a random item from the list_like object.
    """
    return list_like[randint(0, len(list_like) - 1)]


@app.route(API_PREFIX + 'config')
def config():
    """Return our configuration to client."""
    data = cache.get('unchanging-config')
    if data is None:
        log.info('Configuration is not cached, building')
        data = {}
        data['fixed_links'] = CONFIG['fixed_links']
        data['header_links'] = CONFIG['header_links']
        data['name'] = CONFIG['name']
        # TODO: Move these off into javascript since they are authless
        try:
            response = requests.get(
                BING + '/HPImageArchive.aspx?format=js&idx=0&n=1&mkt=en-US'
            )
            data['background_img'] = BING + response.json()['images'][0]['url']
        except requests.RequestException:
            data['background_img'] = (
                'http://www.bing.com/az/hprichbg/rb/'
                'MeerkatAmuck_EN-US5734433814_1920x1080.jpg'
            )
        cache.set('unchanging-config', data, timeout=60 * 60 * 5)

    data['greeting'] = rando(CONFIG['greetings'])
    try:
        data['quote'] = rando(requests.get(
            'https://gist.githubusercontent.com/dmakk767/'
            '9375ff01aff76f1788aead1df9a66338/raw/'
            '491f8c2e91b7d3b8f1c8230e32d9c9bc1a1adfa6/Quotes.json%2520'
        ).json())
    except requests.RequestException:
        pass

    return jsonify(data)


@app.route(API_PREFIX + 'github')
def github():
    """Get pull requests and any other github related data."""
    if GH_TOKEN is None:
        log.error('No Github Token is set.')
        return jsonify({})
    gh_cache = cache.get('github-cache')
    if gh_cache is not None:
        log.info('Using cache for github response')
        return gh_cache

    data = {}
    for key, search in GH_SEARCHES:
        try:
            response = requests.get(
                GH_URL + GH_SEARCH_PREFIX + search,
                headers=GH_HEADERS,
                timeout=5,
            ).json()
            data[key] = response['items']
        except requests.RequestException:
            pass
    response = jsonify(data)
    cache.set('github-cache', response, timeout=60 * 5)
    return response


@app.route(API_PREFIX + 'cal')
def cal():
    """Grab today's calendar items from a list of icals."""
    # Use cache for today if available
    todays_events = cache.get('todays-events')
    if todays_events is not None:
        log.info('Using cache for calendar events')
        return todays_events

    now = datetime.now()
    todays_events = {}
    for cal in CAL_URLS:
        todays_events[cal['name']] = []
        cal_parser = CalendarParser(ics_url=cal['url'])
        for event in cal_parser.parse_ics(overwrite_events=False):
            if now < event.start_time < now + timedelta(days=1):
                if cal_parser.time_zone != utc and cal_parser.time_zone is not None:
                    # We need to localize and because Flask until 0.13
                    # it won't handle timezone aware, so we have to
                    # float it back.
                    event.start_time = cal_parser.time_zone.localize(
                        event.start_time
                    ).astimezone(utc)
                    event.end_time = cal_parser.time_zone.localize(
                        event.end_time
                    ).astimezone(utc)
                todays_events[cal['name']].append(event)

    results = jsonify(todays_events)
    cache.set('todays-events', results, timeout=60 * 60 * 5)
    return results


@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def catch_all(path):
    """Let Vue handle routing."""
    # If we're in debug run it all to the javascript dev server
    if app.debug:
        return requests.get('http://localhost:8080/{}'.format(path)).text
    return render_template("index.html")
