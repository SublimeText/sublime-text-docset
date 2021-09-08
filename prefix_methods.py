#!/usr/bin/env python3

"""
Dashing can source a symbol's name from a specified attribute
instead of the literal text.

This script prefixes all method names with their containing class and module
and adds it as an attribute that we tell dashing to use later.
"""

import sys
from pathlib import Path

from bs4 import BeautifulSoup

API_PATH = "www.sublimetext.com/docs/api_reference.html"
NAME_ATTR = "data-qual-name"
SKIP_ATTR = "data-skip"
FUNC_ATTR = "data-function"

KEYWORD_MAP = {
    "Module": "module",
    "Class": "class",
    "Value": "type",
    "Tuple": "type",
    "Dict": "type",
}


def main():
    path = Path(__file__).parent / API_PATH

    with path.open(encoding='utf-8') as file:
        html = file.read()

    soup = BeautifulSoup(html, 'lxml')

    # Fix `sublime` heading
    if sublime_span := soup.select_one("h2#sublime span"):
        sublime_span.name = 'code'

    for section in soup.select("section section"):
        headings = section.select("h2")
        print(f"\n{headings=}")
        if not headings:
            continue
        if len(headings) > 1:
            print("Found multiple or no headings")
            return 1
        h2 = headings[0]
        if not (code := h2.select_one('code')):
            continue

        namespace = code.string.strip()

        # Assign class to heading code tag
        heading_text = h2.get_text()
        for keyword, class_ in KEYWORD_MAP.items():
            if keyword in heading_text:
                code['class'] = class_
                break
        else:
            print("Unexpected text:", h2)
            return 1

        # Traverse td.mth and set attr
        for td in section.select('td.mth'):
            name = td.get_text()
            if (
                # Skip dummy fields and constructors
                name == '(no methods)'
                or name.partition('(')[0] == namespace.rpartition('.')[-1]
            ):
                td[SKIP_ATTR] = 1
            else:
                td[NAME_ATTR] = f"{namespace}.{td.get_text()}"
                if code['class'] == 'module':
                    td[FUNC_ATTR] = 1
            
            print(f"{td}")

    with path.open('w', encoding='utf-8') as file:
        # Can't prettify as that would introduce whitespace around inline tags
        file.write(str(soup))


if __name__ == '__main__':
    sys.exit(main())
