#!/usr/bin/env python3

"""
Mangles our tweaked TOML format into the `dashing` JSON format
"""
from tomllib import load
from json import dump


CONFIG_MAP = {
    'resources/sublime-text.toml': 'sublime-text/www.sublimetext.com/dashing.json',
    'resources/sublime-merge.toml': 'sublime-merge/www.sublimemerge.com/dashing.json',
}


for toml_path, json_path in CONFIG_MAP.items():
    with open(toml_path, 'rb') as f:
        dashing = load(f)

        selector_list = dashing['selectors']
        selector_dict = {}

        for path in selector_list:
            for obj in selector_list[path]:
                if not obj:
                    continue
                print(path, obj)
                css = obj['css']
                while css in selector_dict:
                    css += ' '

                item = {
                    **obj,
                    'matchpath': fr'/{path}\.html$' if path else r'\.html$'
                }
                del item['css']

                print(item)
                selector_dict[css] = item

        dashing['selectors'] = selector_dict
        print(dashing)
    with open(json_path, 'w') as f:
        dump(dashing, f, indent=4)
