#!/usr/bin/env python

import sys
import requests
import argparse



def main(arguments):
    res = []

    parser = argparse.ArgumentParser(description='Extract status result from ODNB.')
    # parser.add_argument('--exact', help="find an exact match of the game", action="store_true")
    # args = parser.parse_args()

    try:

        with open("odnb-lista.txt") as fp, open('odnb-result.txt', 'a+') as wt:
            line = fp.readline()
            while line:
                print(line)


                # ODNB: search?q=Iris+Murdoch&searchBtn=Search&isQuickSearch=true
                payload = {'q': line.replace('\r\n', ''), 'searchBtn': 'Search', 'isQuickSearch': 'true'}
                r = requests.get('https://www.oxforddnb.com/search', params=payload)
                r.raise_for_status()
                wt.write(line.replace('\n', '') + ';'+ str(r.status_code))
                line = fp.readline()

    finally:
        fp.close()
        wt.close()

if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
