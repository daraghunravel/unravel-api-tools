#!/usr/bin/env python

from __future__ import print_function

import sys
import os
import time
from argparse import ArgumentParser

try:
    import requests
except ImportError:
    raise Exception(
        'requests package not installed. '
        'please run "pip install requests"')

try:
    import ruamel.yaml as yaml
except ImportError:
    raise Exception(
        'ruamel.yaml package not installed. '
        'please run "pip install ruamel.yaml"')

URL = 'https://alpha-api.unravel.io/v1'

parser = ArgumentParser(description='Submit a test description to Unravel API')
parser.add_argument('path', type=str, help='Path to the test definition file.')


def read(path):
    """
    Read the input file and substitue environment variables where appropriate.
    """
    with open(path) as f:
        data = f.read()
    data = data.format(**os.environ)
    return data


def create_session(api_key):
    """
    Create a requests session with API-relevant headers.
    """
    session = requests.Session()
    session.headers.update({
        'Unravel-API-Key': api_key,
        'Content-Type': 'application/yaml',
        'Accept': 'application/yaml',
    })
    return session


def submit(session, data):
    """
    Submit a test description to the Unravel API.
    """
    response = session.post('{}/test'.format(URL), data)
    if not response.status_code == 202:
        raise Exception(json_message(response))
    return response.headers['Location']


def poll(session, queue_url):
    """
    Wait for the test to finish and return the response URL.
    """
    while True:
        response = session.get(queue_url, allow_redirects=False)
        if not response.status_code == 200:
            break
        print(response.text)
        time.sleep(10)
    if not response.status_code == 303:
        raise Exception(json_message(response))
    return response.headers['Location']


def json_message(response):
    try:
        return response.json()['message']
    except Exception:
        return response.text


def main():
    args = parser.parse_args()
    env_var = 'UNRAVEL_API_KEY'
    if not env_var in os.environ:
        raise Exception('Set the {} environment variable.'.format(env_var))
    api_key = os.environ[env_var]
    data = read(args.path)
    session = create_session(api_key)
    queue_url = submit(session, data)
    print('submitted: {}'.format(queue_url))
    results_url = poll(session, queue_url)
    print('complete: {}'.format(results_url))
    response = session.get(results_url)
    if not response.status_code == 200:
        raise Exception(json_message(response))
    print('-' * 80)
    print(response.text)
    result = yaml.safe_load(response.text)
    sys.exit(0 if result['passed'] else 1)


if __name__ == '__main__':
    try:
        main()
    except Exception as e:
        sys.stderr.write('{}\n'.format(e))
        sys.exit(1)
