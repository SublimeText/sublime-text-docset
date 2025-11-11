import unittest
import sqlite3

from abc import ABC
from collections import defaultdict


class DocsetTestCaseBase(ABC, unittest.TestCase):
    NAME = None
    SQLITE_PATH_FMT = '../out/{}/Contents/Resources/docSet.dsidx'

    @classmethod
    def setUpClass(cls):
        cls.con = sqlite3.connect(cls.SQLITE_PATH_FMT.format(cls.NAME))
        cls.cur = cls.con.cursor()

    @classmethod
    def tearDownClass(cls):
        cls.con.close()

    def test_no_empty_aliases(self):
        """The docset index must not contain empty entries"""
        sql = '''
            SELECT  *
            FROM    searchIndex
            WHERE   name = ''
        '''
        res = self.cur.execute(sql)
        self.assertFalse(res.fetchall())

    def test_no_newline_aliases(self):
        """The docset index must not contain entries with newlines in them"""
        sql = '''
            SELECT  *
            FROM    searchIndex
            WHERE   name LIKE '%\n%'
        '''
        res = self.cur.execute(sql)
        self.assertFalse(res.fetchall())

    @unittest.skip('Not implemented')
    def test_no_broken_paths(self):
        """The docset index must not contain broken paths"""
        pass

    def test_paths_are_autolinks(self):
        """Sanity check dashing format"""
        sql = '''
            SELECT  *
            FROM    searchIndex
            WHERE   path NOT LIKE 'docs/%.html#autolink-%'
        '''
        res = self.cur.execute(sql)
        self.assertFalse(res.fetchall())

    def _test_a_doc_page_index(
        self, path: str,
        contains_strict: list[tuple[str,str]],
        contains_lenient: list[tuple[str,str]] | None = None,
    ):
        sql = f'''
            SELECT  type, name
            FROM    searchIndex
            WHERE   path LIKE '{path}#%'
        '''
        res = self.cur.execute(sql)
        items = res.fetchall()

        for pair in contains_lenient or []:
            self.assertIn(pair, items)

        lookup = defaultdict(list)
        for check in contains_strict:
            lookup[check[1]].append(check[0])

        for pair in contains_strict:
            self.assertIn(pair, items)

            ds_type, ds_term = pair
            lookup_result = lookup[ds_term][:]
            self.assertFalse(lookup_result.remove(ds_type))


class SublimeMergeDocsetTestCase(DocsetTestCaseBase):
    NAME = 'sublime-merge.docset'


class SublimeTextDocsetTestCase(DocsetTestCaseBase):
    NAME = 'sublime-text.docset'

    def test_api_reference(self):
        contains = [
            ('Guide', 'API Reference'),
            ('Module', 'sublime'),
            ('Module', 'sublime_plugin'),
            ('Class', 'sublime.Window'),
            ('Type', 'sublime.Kind'),
            ('Type', 'sublime.Event'),
            ('Class', 'sublime_plugin.EventListener'),
            ('Method', 'sublime_plugin.ViewEventListener.on_activated'),
            ('Function', 'sublime.cache_path'),
            ('Attribute', 'sublime.KindId.COLOR_YELLOWISH'),
            ('Attribute', 'sublime.RegionFlags.DRAW_EMPTY_AS_OVERWRITE'),
        ]
        self._test_a_doc_page_index('docs/api_reference.html', contains)


# Don't test the base class directly
del DocsetTestCaseBase
