#!/usr/bin/env python

import sys
import requests
import argparse
import html2text
import re


def main(arguments):
    res = []

    parser = argparse.ArgumentParser(description='Extract author first paragraph from wikipedia.')
    # parser.add_argument('--exact', help="find an exact match of the game", action="store_true")
    # args = parser.parse_args()

    try:

        with open("autores.txt") as fp, open('result.txt', 'a+') as wt:
            line = fp.readline()
            while line:
                print(line)

                # ?search=Keith+McCarthy&title=&go=Go&wprov=acrw1_0
                # https://en.wikipedia.org/w/index.php?search=Keith+McCarthy&title=Special%3ASearch&go=Go&wprov=acrw1_0
                # https://en.wikipedia.org/w/index.php?go=Go&search=Keith%2BMcCarthy&title=Special%253ASearch&ns0=1
                payload = {'search': line.replace('\r\n', ''), 'title': 'Special:Search', 'go': 'Go',
                           'wprov': 'acrw1_0'}
                r = requests.get('https://en.wikipedia.org/w/index.php', params=payload)
                r.raise_for_status()

                h = html2text.HTML2Text()
                h.ignore_links = True
                h.single_line_break = True
                h.ignore_tables = True
                h.body_width = False
                content = h.handle(r.content.decode('utf8'))

                matches = re.findall("\*\*.*", content)
                matches = list(filter(lambda x: "may not meet" not in x and "Learn how and when" not in x and "may refer to" not in x, matches))

                if len(matches) == 0:
                    wt.write(line.replace('\r\n', '') + ';' + '\n')
                    line = fp.readline()
                    continue

                wt.write(line.replace('\r\n', '') + ';' + matches[0].encode('utf8') + '\n')
                line = fp.readline()
    finally:
        fp.close()
        wt.close()

if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
