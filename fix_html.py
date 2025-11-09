#!/usr/bin/env python3

"""
Strip portions of the HTML pages that we don't need
"""
import sys
from pathlib import Path

from bs4 import BeautifulSoup

DOC_ROOTS = [
    'sublime-text/www.sublimetext.com/docs',
    'sublime-merge/www.sublimemerge.com/docs',
]


def delete_skins(soup):
    """Strip header and ad content"""
    for element in soup.find_all(['header', 'nav', 'aside']):
        if not element:
            continue
        element.decompose()

    for h1 in soup.find_all('h1'):
        if not h1:
            continue
        h1_version = h1.find('div', class_='versions')
        if not h1_version:
            continue
        h1_version.decompose()

    twitter = soup.find('div', class_='twitter_follow')
    if twitter:
        twitter.decompose()


def remove_link_icon(soup):
    """Drop the permalink icon"""
    for a in soup.find_all('a', string='🔗'):
        a.decompose()


def main():

    for root in DOC_ROOTS:
        root_directory = Path(root)
        for path in root_directory.rglob('*.html'):

            with path.open(encoding='utf-8') as file:
                html = file.read()

            soup = BeautifulSoup(html, 'lxml')

            delete_skins(soup)
            remove_link_icon(soup)

            with path.open('w', encoding='utf-8') as file:
                # Can't prettify as that would introduce whitespace around inline tags
                file.write(str(soup))


if __name__ == '__main__':
    sys.exit(main())
