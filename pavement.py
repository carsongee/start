"""
Paver file to get dev stuff running.
"""
from io import open
from os import environ as env
from subprocess import Popen

from paver.easy import tasks


@tasks.task
def run():
    """Run the dev servers."""
    env['FLASK_DEBUG'] = '1'
    env['FLASK_APP'] = 'start.py'
    with open('.env', 'r') as config:
        for line in config.read().splitlines():
            name, value = line.split('=', 1)
            env[name] = value.strip("'")
    try:
        redis = Popen(
            ['redis-server'],
             shell=True,
        )
        flask = Popen(
            ['flask run'],
            shell=True,
        )
        webpack = Popen(
            ['npm run dev'],
            shell=True,
        )
        redis.communicate()
        flask.communicate()
        webpack.communicate()
    except KeyboardInterrupt:
        print('Killing development environment')
        flask.kill()
        webpack.kill()
