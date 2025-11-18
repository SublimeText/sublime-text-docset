#!/usr/bin/env python3

"""
Mangles our tweaked TOML format into the `dashing` JSON format
"""
import sys

from tomllib import load
from json import dump

CONFIG_MAP = {
    '../resources/sublime-text.toml': '../sublime-text/www.sublimetext.com/dashing.json',
    '../resources/sublime-merge.toml': '../sublime-merge/www.sublimemerge.com/dashing.json',
}


def main():
    for toml_path, json_path in CONFIG_MAP.items():
        with open(toml_path, 'rb') as f:
            dashing = load(f)

        selector_list = dashing['selectors']
        selector_dict = {}

        for path in selector_list:
            for toml_item in selector_list[path]:
                if not toml_item:
                    continue

                # Pad the selector until it is unique
                css = toml_item['css']
                while css in selector_dict:
                    css += ' '

                matchpath = fr'/{path}\.html$'
                if path == 'GLOBAL':
                    matchpath = r'\.html$'

                json_item = toml_item
                json_item['matchpath'] = matchpath
                del json_item['css']

                selector_dict[css] = json_item

        # Replace [selectors] with the `dashing` format
        dashing['selectors'] = selector_dict

        with open(json_path, 'w') as f:
            dump(dashing, f, indent=4)


if __name__ == '__main__':
    sys.exit(main())
