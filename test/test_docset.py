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
        not_contains: list[tuple[str,str]] | None = None,
    ):
        sql = '''
            SELECT  type, name
            FROM    searchIndex
            WHERE   path LIKE :path_like
        '''
        data = {'path_like': f'{path}#%'}
        res = self.cur.execute(sql, data)
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

        for pair in not_contains or []:
            self.assertNotIn(pair, items)


class SublimeMergeDocsetTestCase(DocsetTestCaseBase):
    NAME = 'sublime-merge.docset'

    def test_home(self):
        contains = [
            ('Guide', 'Documentation'),
            ('Section', 'General'),
            ('Section', 'Features'),
            ('Section', 'Customization'),
            ('Section', 'Miscellaneous'),
            ('Section', 'Package Development'),
        ]
        self._test_a_doc_page_index('docs/index.html', contains)

    def test_key_bindings(self):
        contains = [
            ('Guide', 'Key Bindings'),
            ('Setting', '"keys" Key'),
            ('Section', 'Bindings'),
            ('Filter', '"search_mode"'),
        ]
        self._test_a_doc_page_index('docs/key_bindings.html', contains)

    def test_themes(self):
        contains = [
            ('Guide', 'Themes'),
            ('Property', 'layer#.opacity'),
            ('Section', 'Settings'),
            ('Setting', 'overlay_scroll_bars'),
            ('Element', 'root_tabs'),
            ('Property', 'puck_color'),
        ]
        self._test_a_doc_page_index('docs/themes.html', contains)

    def test_menus(self):
        contains = [
            ('Guide', 'Menus'),
            ('Section', 'Entries'),
            ('File', 'Action.sublime-menu'),
            ('Setting', '"mnemonic"'),
            ('Variable', '$git_dir'),
        ]
        self._test_a_doc_page_index('docs/menus.html', contains)

    def test_packages(self):
        contains = [
            ('Guide', 'Packages'),
            ('Section', 'Package Directories'),
            ('File', '%APPDATA%\\Sublime Merge\\Installed Packages\\'),
            ('File', '~/Library/Application Support/Sublime Merge/Installed Packages/'),
        ]
        self._test_a_doc_page_index('docs/packages.html', contains)

    def test_minihtml(self):
        contains = [
            ('Guide', 'minihtml Reference'),
            ('Section', 'CSS'),
            ('Variable', 'var(--greenish)'),
        ]
        self._test_a_doc_page_index('docs/minihtml.html', contains)


class SublimeTextDocsetTestCase(DocsetTestCaseBase):
    NAME = 'sublime-text.docset'

    def test_home(self):
        contains = [
            ('Guide', 'Documentation'),
            ('Section', 'Usage'),
            ('Section', 'Customization'),
            ('Section', 'Miscellaneous'),
            ('Section', 'Package Development'),
        ]
        self._test_a_doc_page_index('docs/index.html', contains)

    def test_git_integration(self):
        contains = [
            ('Guide', 'Git Integration'),
            ('Attribute', 'Staged Modification'),
            ('Section', 'Diff Markers'),
            ('Command', 'Open Git Repository…'),
            ('Command', 'Sublime Merge: Folder History'),
            ('Setting', 'show_git_status'),
        ]
        self._test_a_doc_page_index('docs/git_integration.html', contains)

    def test_incremental_diff(self):
        contains = [
            ('Guide', 'Incremental Diff'),
            ('Section', 'Diff Markers'),
            ('Tag', 'diff.inserted'),
            ('Setting', 'mini_diff'),
        ]
        self._test_a_doc_page_index('docs/incremental_diff.html', contains)

    def test_indexing(self):
        contains = [
            ('Guide', 'Indexing'),
            ('Section', 'Status'),
            ('Setting', 'index_exclude_patterns'),
        ]
        self._test_a_doc_page_index('docs/indexing.html', contains)

    def test_completions(self):
        contains = [
            ('Guide', 'Completions'),
            ('Section', 'Completion Metadata'),
            ('Setting', 'auto_complete_delay'),
            ('Field', 'tabTrigger'),
            ('Value', 'Navigation'),
            ('Value', '"navigation"'),
            ('Variable', '$TM_FILEPATH'),
        ]
        self._test_a_doc_page_index('docs/completions.html', contains)

    def test_distraction_free_mode(self):
        contains = [
            ('Guide', 'Distraction Free Mode'),
            ('Section', 'Customization'),
            ('Setting', '"gutter"'),
            ('File', 'Packages/User/Distraction Free.sublime-settings'),
        ]
        self._test_a_doc_page_index('docs/distraction_free.html', contains)

    def test_projects(self):
        contains = [
            ('Guide', 'Projects'),
            ('Section', 'Project Format'),
            ('Setting', 'follow_symlinks'),
        ]
        self._test_a_doc_page_index('docs/projects.html', contains)

    def test_settings(self):
        contains = [
            ('Guide', 'Settings'),
            ('Section', 'Categories'),
            ('File', 'Packages/Default/Preferences.sublime-settings'),
        ]
        self._test_a_doc_page_index('docs/settings.html', contains)

    def test_key_bindings(self):
        contains = [
            ('Guide', 'Key Bindings'),
            ('Section', 'User Bindings'),
            ('Filter', '"has_prev_field"'),
            ('Setting', '"args" Key'),
        ]
        self._test_a_doc_page_index('docs/key_bindings.html', contains)

    def test_indentation_settings(self):
        contains = [
            ('Guide', 'Indentation Settings'),
            ('Section', 'Converting Between Tabs and Spaces'),
            ('Setting', 'indent_to_bracket'),
            ('Setting', 'use_tab_stops'),
        ]
        self._test_a_doc_page_index('docs/indentation.html', contains)

    def test_spell_checking(self):
        contains = [
            ('Guide', 'Spell Checking'),
            ('Section', 'Dictionaries'),
            ('Setting', 'spell_check'),
            ('Command', 'next_misspelling'),
        ]
        not_contains = [
            ('Command', 'word'),
        ]
        self._test_a_doc_page_index('docs/spell_checking.html', contains,
                                    not_contains=not_contains)

    def test_build_systems(self):
        contains = [
            ('Guide', 'Build Systems'),
            ('Section', 'Custom Options'),
            ('Option', 'quiet'),
            ('Variable', '$project_path'),
        ]
        self._test_a_doc_page_index('docs/build_systems.html', contains)

    def test_packages(self):
        contains = [
            ('Guide', 'Packages'),
            ('Section', 'Locations'),
            ('File', '<data_path>/Installed Packages/'),
        ]
        self._test_a_doc_page_index('docs/packages.html', contains)

    def test_file_patterns(self):
        contains = [
            ('Guide', 'File Patterns'),
            ('Section', 'Uses'),
            ('Setting', '"binary_file_patterns"'),
        ]
        self._test_a_doc_page_index('docs/file_patterns.html', contains)

    def test_safe_mode(self):
        contains = [
            ('Guide', 'Safe Mode'),
            ('Section', 'Behavior'),
            ('File', '~/.config/sublime-text-safe-mode/'),
            ('Command', 'subl --safe-mode'),
        ]
        self._test_a_doc_page_index('docs/safe_mode.html', contains)

    def test_reverting_install(self):
        contains = [
            ('Guide', 'Reverting to a Freshly Installed State'),
            ('Section', 'Cache'),
            ('File', '~/Library/Application Support/Sublime Text'),
            ('File', '~/.cache/sublime-text'),
        ]
        self._test_a_doc_page_index('docs/revert.html', contains)

    def test_ligatures(self):
        contains = [
            ('Guide', 'Ligatures'),
            ('Section', 'Troubleshooting'),
            ('Option', '"no_clig"'),
        ]
        self._test_a_doc_page_index('docs/ligatures.html', contains)

    def test_portable_license(self):
        contains = [
            ('Guide', 'Portable License Keys'),
            ('Section', 'Steps'),
            ('File', '~/Library/Application Support/Sublime Text/Local'),
        ]
        self._test_a_doc_page_index('docs/portable_license_keys.html', contains)

    def test_color_schemes(self):
        contains = [
            ('Guide', 'Color Schemes'),
            ('Section', 'Scope Rules'),
            ('Setting', 'minimap_border'),
            ('Function', 'blenda() adjuster'),
        ]
        self._test_a_doc_page_index('docs/color_schemes.html', contains)

    def test_themes(self):
        contains = [
            ('Guide', 'Themes'),
            ('Section', 'Inheritance'),
            ('Property', 'indent_top_level'),
            ('Property', 'fg'),
            ('Element', 'disclosure_button_control'),
            ('Setting', 'overlay_scroll_bars'),
        ]
        self._test_a_doc_page_index('docs/themes.html', contains)

    def test_menus(self):
        contains = [
            ('Guide', 'Menus'),
            ('Section', 'Entries'),
            ('File', 'Side Bar Mount Point.sublime-menu'),
            ('Setting', 'mnemonic'),
        ]
        self._test_a_doc_page_index('docs/menus.html', contains)

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

    def test_syntax_definitions(self):
        contains = [
            ('Guide', 'Syntax Definitions'),
            ('Section', 'Including Other Files'),
            ('Trait', 'first_line_match'),
            ('Instruction', 'pop'),
            ('Instruction', 'meta_content_scope'),
            ('Test', '^'),
            ('Test', '<-'),
            ('Test', 'local-definition'),
        ]
        not_contains = [
            ('Trait', '.'),
            ('Trait', '0'),
            ('Trait', '1'),
            ('Trait', '2'),
            ('Instruction', '.'),
            ('Instruction', '0'),
            ('Instruction', '1'),
            ('Instruction', '2'),
            ('Instruction', '#'),
            ('Instruction', ':'),
            ('Instruction', '['),
            ('Instruction', '{'),
            ('Instruction', 'true'),
        ]
        self._test_a_doc_page_index('docs/syntax.html', contains,
                                    not_contains=not_contains)

    def test_scope_naming(self):
        contains = [
            ('Guide', 'Scope Naming'),
            ('Section', 'Syntax Definitions'),
            ('Tag', 'constant.numeric.integer.hexadecimal'),
        ]
        self._test_a_doc_page_index('docs/scope_naming.html', contains)

    def test_minihtml(self):
        contains = [
            ('Guide', 'minihtml Reference'),
            ('Section', 'CSS'),
            ('Element', '<p>'),
            ('Element', '<h3>'),
            ('Element', '<ul>'),
            ('Attribute', 'href'),
            ('Variable', 'var(--greenish)'),
            ('Style', 'padding-top'),
            ('Function', 'lightness()'),
            ('Function', 'l()'),
        ]
        not_contains = [
            ('Element', 'file://'),
        ]
        self._test_a_doc_page_index('docs/minihtml.html', contains,
                                    not_contains=not_contains)


# Don't test the base class directly
del DocsetTestCaseBase
