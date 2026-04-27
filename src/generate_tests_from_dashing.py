#!/usr/bin/env python3

"""
Strip portions of the HTML pages that we don't need
"""
import sys
from collections import defaultdict
from re import match, sub

DASHING_LOGS = [
    '../out/dashing-sublime-merge.txt',
    '../out/dashing-sublime-text.txt',
]


def dump_test_stuff(doc_path, assertions):
    if not doc_path:
        return

    name = match(r'docs/([\w-]+)\.html', doc_path).group(1)
    tests = f'''
    def test_{name.replace('-', '_')}(self):
        contains = [
            {('\n' + (' ' * 12)).join(sorted(assertions.keys()))}
        ]
        self._test_a_doc_page_index('{doc_path}', contains)'''
    print(tests)

    for assertion in [k for k in sorted(assertions.keys()) if assertions[k] > 1]:
        print(f'{" " * 8}### {assertion} was found {assertions[assertion]} times')


def process_dashing_output(dashing_filepath):
    doc_path = None
    assertion_histogram = defaultdict(int)

    with open(dashing_filepath, 'r') as dashing_file:

        for line in dashing_file:
            doc_path_match = match(r'(docs/[\w-]+\.html) looks like HTML$', line)
            test_match = match(r"Match: '(.+)' is type (\w+) at", line)

            if doc_path_match:
                dump_test_stuff(doc_path, assertion_histogram)
                assertion_histogram = defaultdict(int)
                doc_path = doc_path_match.group(1)
            elif test_match:
                index_type = test_match.group(2)
                index_text = test_match.group(1).replace('\\', '\\\\')
                assertion = f"('{index_type}', '{index_text}'),"
                assertion_histogram[assertion] += 1

        dump_test_stuff(doc_path, assertion_histogram)


def main():

    for dump in DASHING_LOGS:
        print(f'\n# Starting test case for {dump} ###########################')
        process_dashing_output(dump)


if __name__ == '__main__':
    sys.exit(main())
