#!/usr/bin/env python3

"""
Dump a summary of the docset SQLite index
"""
import sys
import csv
import sqlite3

SQLITE_PATH_FMT = '../out/{}/Contents/Resources/docSet.dsidx'
TABLE_PATH_FMT = '../resources/{}-summary.csv'
DOCSETS = {
    'sublime-text.docset',
    'sublime-merge.docset',
}


def main():
    for docset in DOCSETS:
        con = sqlite3.connect(SQLITE_PATH_FMT.format(docset))
        cur = con.cursor()

        sql = '''
            SELECT  substr(path, 0, instr(path, '#')) AS p,
                    type,
                    name,
                    COUNT(*)
            FROM    searchIndex
            GROUP BY substr(path, 0, instr(path, '#')),
                    type,
                    name
            ORDER BY p, type, name
        '''
        res = cur.execute(sql)

        with open(TABLE_PATH_FMT.format(docset), 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(('Path', 'Type', 'Name', 'Count'))
            writer.writerows(res.fetchall())

        con.close()


if __name__ == '__main__':
    sys.exit(main())
