import io
from os.path import dirname, join, realpath
from random import randint

from flask import Flask, render_template, jsonify
import requests
import yaml

BING = 'https://www.bing.com'
PATH = dirname(realpath(__file__))
CONFIG = yaml.load(io.open(join(PATH, 'data.yml'), 'r', encoding='UTF-8'))

app = Flask(__name__, static_folder='./dist/static', template_folder='./dist/')


def rando(list_like):
    """
    Returns a random item from the list_like object.
    """
    return list_like[randint(0, len(list_like) - 1)]


@app.route('/start-api/v1/config')
def config():
    """Return our configuration to client."""
    data = {}
    data['greeting'] = rando(CONFIG['greetings'])
    data['fixed_links'] = CONFIG['fixed_links']
    data['name'] = CONFIG['name']
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


@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def catch_all(path):
    """Let Vue handle routing."""
    # If we're in debug run it all to the javascript dev server
    if app.debug:
        return requests.get('http://localhost:8080/{}'.format(path)).text
    return render_template("index.html")
