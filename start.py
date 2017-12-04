import io
from os import environ as env
from os.path import abspath, dirname, join, realpath
from random import randint

from flask import Flask, render_template, jsonify
from flask_htpasswd import HtPasswdAuth
import requests
import yaml

API_PREFIX = '/start-api/v1/'
BING = 'https://www.bing.com'
PATH = dirname(realpath(__file__))
CONFIG = yaml.load(io.open(join(PATH, 'data.yml'), 'r', encoding='UTF-8'))
GH_URL = 'https://api.github.com/'
GH_HEADERS = {'Authorization': 'token {}'.format(env.get('GH_TOKEN'))}
GH_USERNAME = env.get('GH_USERNAME')
GH_SEARCH_PREFIX = 'search/issues?q=state:open type:pr '
GH_SEARCHES = (
    ('review-requests', 'review-requested:{}'.format(GH_USERNAME)),
    ('changes-requested', 'review:changes_requested author:{}'.format(GH_USERNAME)),
    ('approved', 'review:approved author:{}'.format(GH_USERNAME)),
)
# Write out htpasswd to path if environment variable set
HTPASSWD_PATH = abspath('.htpasswd')
HTPASSWD = env.get('START_HTPASSWD')
if HTPASSWD:
    with open(HTPASSWD_PATH, 'w') as wfile:
        wfile.write(HTPASSWD)

app = Flask(__name__, static_folder='./dist/static', template_folder='./dist/')
app.config['FLASK_AUTH_ALL'] = True
app.config['FLASK_HTPASSWD_PATH'] = HTPASSWD_PATH
htpasswd = HtPasswdAuth(app)


def rando(list_like):
    """
    Returns a random item from the list_like object.
    """
    return list_like[randint(0, len(list_like) - 1)]


@app.route(API_PREFIX + 'config')
def config():
    """Return our configuration to client."""
    data = {}
    data['greeting'] = rando(CONFIG['greetings'])
    data['fixed_links'] = CONFIG['fixed_links']
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
    return jsonify(data)

@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def catch_all(path):
    """Let Vue handle routing."""
    # If we're in debug run it all to the javascript dev server
    if app.debug:
        return requests.get('http://localhost:8080/{}'.format(path)).text
    return render_template("index.html")

