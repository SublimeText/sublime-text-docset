import unittest
import sqlite3

from abc import ABC


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


class SublimeMergeDocsetTestCase(DocsetTestCaseBase):
    NAME = 'sublime-merge.docset'


class SublimeTextDocsetTestCase(DocsetTestCaseBase):
    NAME = 'sublime-text.docset'


# Don't test the base class directly
del DocsetTestCaseBase
