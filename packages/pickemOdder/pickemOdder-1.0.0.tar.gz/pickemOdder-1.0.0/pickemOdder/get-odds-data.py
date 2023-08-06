#!/usr/bin/env python

import argparse
import sys
import os
import urllib
import json

import requests

HOST = 'https://api.the-odds-api.com'
PATH = '/v3/odds'


def get_url(key):
    params = urllib.parse.urlencode({
        'sport': 'americanfootball_nfl',
        'region': 'us',
        'mkt': 'h2h',
        'apiKey': key,
    })
    return f'{HOST}{PATH}/?{params}'


def main():
    ap = argparse.ArgumentParser(description=f'gets odds data from {HOST}')
    ap.add_argument('outfile', nargs='?', type=argparse.FileType('w'), default=sys.stdout)
    ap.add_argument(
        '-k', '--key', help='api key for odds api', type=str,
        default=os.environ.get('ODDS_API_KEY', '')
    )

    args = ap.parse_args()
    if not args.key:
        sys.stderr.write('No apikey provided\n')
        return -1

    try:
        response = requests.get(get_url(args.key), timeout=2)
        response.raise_for_status()
    except Exception as err:
        sys.stderr.write(f'Failed to get data. Error{err}')
        return -1
    else:
        json.dump(response.json(), args.outfile)
        used, remain = response.headers['x-requests-used'], response.headers['x-requests-remaining']
        sys.stderr.write(f'{used} of {remain} api requests remain')
    return 0


if __name__ == '__main__':
    sys.exit(main())
