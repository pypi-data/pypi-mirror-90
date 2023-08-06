#!/usr/bin/env python

import argparse
import sys

import pandas

from pickemOdder import get_normed_data


def get_sorted_wins_dataframe(data, win_percentage_cut_off=50):
    header = data[0].split(',')
    df = pandas.DataFrame.from_records(data[1:], columns=header)
    return (
        df
        .groupby(by=header[:4])
        .mean()
        .sort_values('away_win', ascending=False)
    )


def main():
    ap = argparse.ArgumentParser(description='Parse input game stats and output rank ordered picks ordered by away_wins')
    ap.add_argument('infile', nargs='?', type=argparse.FileType('r'), default=sys.stdin)
    ap.add_argument('outfile', nargs='?', type=argparse.FileType('w'), default=sys.stdout)

    args = ap.parse_args()
    data = get_normed_data(args.infile)
    if not data:
        return -1
    args.outfile.write(str(get_sorted_wins_dataframe(data)))
    return 0


if __name__ == '__main__':
    sys.exit(main())
