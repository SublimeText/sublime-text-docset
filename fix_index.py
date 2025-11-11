#!/usr/bin/env python3

"""
Tweaks the docset SQLite index after creation
"""
import sys
import sqlite3

SQLITE_PATH_FMT = 'out/{}/Contents/Resources/docSet.dsidx'
DOCSET_FIXES = {
    'sublime-text.docset': [
        ('docs/distraction_free.html',
         'Packages/Default/Distraction\nFree.sublime-settings',
         'Packages/Default/Distraction Free.sublime-settings',),
        ('docs/distraction_free.html',
         'Packages/User/Distraction\nFree.sublime-settings',
         'Packages/User/Distraction Free.sublime-settings',),
        ('docs/syntax.html',
         '<comment_token> SYNTAX\nTEST "<syntax_file>"',
         '<comment_token> SYNTAX TEST "<syntax_file>"', ),
    ],
    'sublime-merge.docset': []
}


def main():
    for docset in DOCSET_FIXES:
        con = sqlite3.connect(SQLITE_PATH_FMT.format(docset))
        cur = con.cursor()

        for fix in DOCSET_FIXES[docset]:
            path, old_name, new_name = fix
            data = {
                'old_name': old_name,
                'new_name': new_name,
                'path_like': path + '#%',
            }

            cur.execute(
                '''
                UPDATE  searchIndex
                SET     name = :new_name
                WHERE   name = :old_name
                        AND path LIKE :path_like
                ''',
                data
            )
            con.commit()
        con.close()


if __name__ == '__main__':
    sys.exit(main())
