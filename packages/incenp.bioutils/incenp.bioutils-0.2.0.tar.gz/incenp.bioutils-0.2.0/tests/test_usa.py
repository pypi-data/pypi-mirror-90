# -*- coding: utf-8 -*-
# Incenp.Bioutils - Incenp.org's utilities for computational biology
# Copyright © 2020 Damien Goutte-Gattat
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.

import unittest

from Bio.SeqRecord import SeqRecord
from incenp.bio.seq import usa
from incenp.bio.seq.databases import DatabaseProvider


def compare_fragment(a, b, msg=None):
    if a.start != b.start or a.end != b.end or a.reverse != b.reverse:
        raise unittest.TestCase.failureException(msg)


class TestAsisUSA(unittest.TestCase):

    def test_parse_asis_usa(self):
        """Check that asis:: USAs are parsed correctly."""

        usas = usa.parse_usa('asis::AAAACCCCGGGGTTTT')
        self.assertIsInstance(usas, usa.AsisUSA)

        records = usas.read()
        self.assertEqual(len(records), 1)
        self.assertIsInstance(records[0], SeqRecord)
        self.assertEqual(records[0].seq, 'AAAACCCCGGGGTTTT')


class TestProgramUSA(unittest.TestCase):

    def setUp(self):
        self.addTypeEqualityFunc(usa.FragmentSpec, compare_fragment)

    def test_identify_program_usa(self):
        """Check that program-based USAs are recognized."""

        usas = usa.parse_usa('program|')
        self.assertIsInstance(usas, usa.ProgramUSA)
        self.assertEqual(usas.program, 'program')
        self.assertListEqual(usas.args, [])

    def test_parse_program_usa_args(self):
        """Check that arguments of a program-based USA are recognized."""

        usas = usa.parse_usa('program id name|')
        self.assertIsInstance(usas, usa.ProgramUSA)
        self.assertEqual(usas.program, 'program')
        self.assertListEqual(usas.args, ['id', 'name'])

    def test_parse_complex_program_usa(self):
        """Check that a complex program-based USA can be parsed."""

        usas = usa.parse_usa('genbank::program id name|[6:20:r]')
        self.assertIsInstance(usas, usa.ProgramUSA)
        self.assertEqual(usas.format, 'genbank')
        self.assertEqual(usas.program, 'program')
        self.assertListEqual(usas.args, ['id', 'name'])
        self.assertEqual(usas.fragment, usa.FragmentSpec(6, 20, True))

    def test_read_program_usa(self):
        """Check that we can read from a program-based USA."""

        usas = usa.parse_usa('genbank::cat tests/samples.gb|')
        records = usas.read()
        self.assertEqual(len(records), 10)
        self.assertEqual(records[0].name, 'EMBOSS_001')


class TestDatabaseUSA(unittest.TestCase):

    def setUp(self):
        db_provider = DatabaseProvider()
        db_provider.cfg.clear()
        db_provider.cfg.add_section('db1')
        db_provider.cfg.set('db1', 'type', 'biosql')
        db_provider.cfg.set('db1', 'driver', 'sqlite3')
        db_provider.cfg.set('db1', 'database', 'tests/samples.sqlite')
        db_provider.cfg.set('db1', 'subdb', 'tests')
        self.db_provider = db_provider

    def _parse(self, u):
        return usa.parse_usa(u, databases=self.db_provider)

    def test_defaulting_to_file(self):
        """Check that database-based USAs are parsed as file-based
           USAs if the database is not recognized."""

        usas = self._parse('dbname')
        self.assertIsInstance(usas, usa.FileUSA)

    def test_recognize_database_usa(self):
        """Check that database-based USAs are recognized as such."""

        usas = self._parse('db1')
        self.assertIsInstance(usas, usa.DatabaseUSA)
        self.assertEqual(usas.database, self.db_provider['db1'])

    def test_parse_database_identifier(self):
        """Check that database-based USAs with identifier are parsed correctly."""

        usas = self._parse('db1:id')
        self.assertIsInstance(usas, usa.DatabaseUSA)
        self.assertEqual(usas.database, self.db_provider['db1'])
        self.assertEqual(usas.identifier, 'id')

    def test_parse_database_keyword(self):
        """Check that database-based USAs with keyword search are parsed correctly."""

        usas = self._parse('db1-acc:word')
        self.assertIsInstance(usas, usa.DatabaseUSA)
        self.assertEqual(usas.database, self.db_provider['db1'])
        self.assertEqual(usas.field, 'acc')
        self.assertEqual(usas.keyword, 'word')

    def test_parse_invalid_database_usa(self):
        """Check that invalid database-based USAs are recognized as such."""

        with self.assertRaisesRegex(usa.Error, "Invalid database USA: keyword required"):
            self._parse('db1-acc')

        with self.assertRaisesRegex(usa.Error, "Invalid database USA: too many parts"):
            self._parse('db1:id:extra')

    def test_read_database_usa(self):
        """Check that we can read sequences from a database-based USA."""

        usas = self._parse('db1')
        records = usas.read()
        self.assertEqual(len(records), 10)
        self.assertEqual(records[0].name, 'EMBOSS_001')

    def test_read_database_usa_with_identifiers(self):
        """Check that we can filter by identifier."""

        usas = self._parse('db1:EMBOSS_001')
        records = usas.read()
        self.assertEqual(len(records), 1)
        self.assertEqual(records[0].name, 'EMBOSS_001')

        usas = self._parse('db1:EMBOSS_099')
        records = usas.read()
        self.assertEqual(len(records), 0)

        usas = self._parse('db1:EMBOSS_00?')
        records = usas.read()
        self.assertEqual(len(records), 9)
        self.assertEqual(records[0].name, 'EMBOSS_001')

        usas = self._parse('db1:EMBOSS_*')
        records = usas.read()
        self.assertEqual(len(records), 10)
        self.assertEqual(records[0].name, 'EMBOSS_001')

        usas = self._parse('db1:TES_000002')
        records = usas.read()
        self.assertEqual(len(records), 1)
        self.assertEqual(records[0].name, 'EMBOSS_002')

    def test_read_database_usa_with_fields(self):
        """Check that we can filter by search fields."""

        usas = self._parse('db1-acc:TES_000003')
        records = usas.read()
        self.assertEqual(len(records), 1)
        self.assertEqual(records[0].name, 'EMBOSS_003')

        usas = self._parse('db1-acc:TES_0000?0')
        records = usas.read()
        self.assertEqual(len(records), 1)
        self.assertEqual(records[0].name, 'EMBOSS_010')

        usas = self._parse('db1-acc:TES_0000*')
        records = usas.read()
        self.assertEqual(len(records), 10)

        usas = self._parse('db1-sv:TES_000009.?')
        records = usas.read()
        self.assertEqual(len(records), 1)
        self.assertEqual(records[0].name, 'EMBOSS_009')

        usas = self._parse('db1-sv:10')
        records = usas.read()
        self.assertEqual(len(records), 1)
        self.assertEqual(records[0].name, 'EMBOSS_010')

        usas = self._parse('db1-id:EMBOSS_002')
        records = usas.read()
        self.assertEqual(len(records), 1)
        self.assertEqual(records[0].name, 'EMBOSS_002')

        with self.assertRaisesRegex(usa.Error, 'Unsupported search field'):
            usa.read_usa('db1-des:long', databases=self.db_provider)

        with self.assertRaisesRegex(usa.Error, 'Unsupported search field'):
            usa.read_usa('db1-key:sample', databases=self.db_provider)

        with self.assertRaisesRegex(usa.Error, 'Unsupported search field'):
            usa.read_usa('db1-org:Homo', databases=self.db_provider)


class TestFileUSA(unittest.TestCase):

    def test_identify_file_usa(self):
        """Check that file-based USAs are recognized as such."""

        usas = usa.parse_usa('file.fasta')
        self.assertIsInstance(usas, usa.FileUSA)
        self.assertEqual(usas.filename, 'file.fasta')

    def test_parse_file_usa_with_identifier(self):
        """Check that file-based USAs with an identifier are parsed correctly."""

        usas = usa.parse_usa('file.fasta:id')
        self.assertIsInstance(usas, usa.FileUSA)
        self.assertEqual(usas.filename, 'file.fasta')
        self.assertEqual(usas.identifier.pattern, '^id$')
        self.assertIsNone(usas.field)
        self.assertIsNone(usas.keyword)

    def test_parse_file_usa_with_keyword(self):
        """Check that file-based USAs with a keyword search are parsed correctly."""

        usas = usa.parse_usa('file.fasta:des:keyword')
        self.assertIsInstance(usas, usa.FileUSA)
        self.assertEqual(usas.filename, 'file.fasta')
        self.assertEqual(usas.field, 'des')
        self.assertEqual(usas.keyword.pattern, '^keyword$')
        self.assertIsNone(usas.identifier)

    def test_parse_invalid_file_usa(self):
        """Check that invalid file-based USAs are recognized as such."""

        with self.assertRaisesRegex(usa.Error, "Invalid file USA: too many parts"):
            usa.parse_usa('file.fasta:acc:keyword:extra')

        with self.assertRaisesRegex(usa.Error, "Unrecognized search field: field"):
            usa.parse_usa('file.fasta:field:keyword')

    def test_read_file_usa(self):
        """Check that we can read sequences from a file-based USA."""

        usas = usa.parse_usa('tests/samples.gb')
        records = usas.read()
        self.assertEqual(len(records), 10)
        self.assertEqual(records[0].name, 'EMBOSS_001')

    def test_read_file_usa_with_identifiers(self):
        """Check that we can filter by identifier."""

        usas = usa.parse_usa('tests/samples.gb:EMBOSS_001')
        records = usas.read()
        self.assertEqual(len(records), 1)
        self.assertEqual(records[0].name, 'EMBOSS_001')

        usas = usa.parse_usa('tests/samples.gb:EMBOSS_099')
        records = usas.read()
        self.assertEqual(len(records), 0)

        usas = usa.parse_usa('tests/samples.gb:EMBOSS_00?')
        records = usas.read()
        self.assertEqual(len(records), 9)
        self.assertEqual(records[0].name, 'EMBOSS_001')

        usas = usa.parse_usa('tests/samples.gb:EMBOSS_*')
        records = usas.read()
        self.assertEqual(len(records), 10)
        self.assertEqual(records[0].name, 'EMBOSS_001')

        usas = usa.parse_usa('tests/samples.gb:TES_000002')
        records = usas.read()
        self.assertEqual(len(records), 1)
        self.assertEqual(records[0].name, 'EMBOSS_002')

    def test_read_file_usa_with_fields(self):
        """Check that we can filter by search fields."""

        usas = usa.parse_usa('tests/samples.gb:acc:TES_000003')
        records = usas.read()
        self.assertEqual(len(records), 1)
        self.assertEqual(records[0].name, 'EMBOSS_003')

        usas = usa.parse_usa('tests/samples.gb:acc:TES_0000?0')
        records = usas.read()
        self.assertEqual(len(records), 1)
        self.assertEqual(records[0].name, 'EMBOSS_010')

        usas = usa.parse_usa('tests/samples.gb:acc:TES_0000*')
        records = usas.read()
        self.assertEqual(len(records), 10)

        usas = usa.parse_usa('tests/samples.gb:sv:TES_000009.?')
        records = usas.read()
        self.assertEqual(len(records), 1)
        self.assertEqual(records[0].name, 'EMBOSS_009')

        usas = usa.parse_usa('tests/samples.gb:sv:10')
        records = usas.read()
        self.assertEqual(len(records), 1)
        self.assertEqual(records[0].name, 'EMBOSS_010')

        usas = usa.parse_usa('tests/samples.gb:id:EMBOSS_002')
        records = usas.read()
        self.assertEqual(len(records), 1)
        self.assertEqual(records[0].name, 'EMBOSS_002')

        usas = usa.parse_usa('tests/samples.gb:des:long')
        records = usas.read()
        self.assertEqual(len(records), 0)

        usas = usa.parse_usa('tests/samples.gb:des:long*')
        records = usas.read()
        self.assertEqual(len(records), 2)
        self.assertEqual(records[0].name, 'EMBOSS_006')

        usas = usa.parse_usa('tests/samples.gb:key:sample')
        records = usas.read()
        self.assertEqual(len(records), 1)
        self.assertEqual(records[0].name, 'EMBOSS_005')

        usas = usa.parse_usa('tests/samples.gb:key:sample*')
        records = usas.read()
        self.assertEqual(len(records), 2)
        self.assertEqual(records[1].name, 'EMBOSS_006')

        usas = usa.parse_usa('tests/samples.gb:org:Homo')
        records = usas.read()
        self.assertEqual(len(records), 1)
        self.assertEqual(records[0].name, 'EMBOSS_004')

        usas = usa.parse_usa('tests/samples.gb:org:Drosophila')
        records = usas.read()
        self.assertEqual(len(records), 1)
        self.assertEqual(records[0].name, 'EMBOSS_005')


class TestListUSA(unittest.TestCase):

    def setUp(self):
        self.addTypeEqualityFunc(usa.FragmentSpec, compare_fragment)

    def test_recognize_list_usa(self):
        """Check that list USAs are recognized as such."""

        usas = usa.parse_usa('list:tests/usas.txt')
        self.assertIsInstance(usas, usa.ListUSA)

        usas = usa.parse_usa('@tests/usas.txt')
        self.assertIsInstance(usas, usa.ListUSA)

    def test_ignore_blank_and_comments(self):
        """Check that blank lines and comments are ignored."""

        usas = usa.parse_usa('list:tests/usas.txt')
        self.assertEqual(len(usas.usas), 6)

    def test_format_transmission(self):
        """Check that format information is properly transmitted to child USAs."""

        usas = usa.parse_usa('list:tests/usas.txt')
        self.assertEqual(usas.usas[0].format, 'asis')
        self.assertEqual(usas.usas[1].format, 'fasta')
        self.assertEqual(usas.usas[2].format, 'genbank')

        usas = usa.parse_usa('pearson::list:tests/usas.txt')
        self.assertEqual(usas.usas[0].format, 'asis')
        self.assertEqual(usas.usas[1].format, 'fasta')
        self.assertEqual(usas.usas[2].format, 'genbank')

    def test_fragment_transmission(self):
        """Check that fragment specifiers are properly transmitted to child USAs."""

        usas = usa.parse_usa('list:tests/usas.txt')
        self.assertIsNone(usas.usas[0].fragment)
        self.assertEqual(usas.usas[1].fragment, usa.FragmentSpec(3, 5, True))
        self.assertIsNone(usas.usas[2].fragment)
        self.assertEqual(usas.usas[3].fragment, usa.FragmentSpec(3, 5, None))
        self.assertEqual(usas.usas[4].fragment, usa.FragmentSpec(3, None, None))
        self.assertEqual(usas.usas[5].fragment, usa.FragmentSpec(None, 5, True))

        usas = usa.parse_usa('list:tests/usas.txt[2:8]')
        self.assertEqual(usas.usas[0].fragment, usa.FragmentSpec(2, 8, None))
        self.assertEqual(usas.usas[1].fragment, usa.FragmentSpec(3, 5, True))
        self.assertEqual(usas.usas[2].fragment, usa.FragmentSpec(2, 8, None))
        self.assertEqual(usas.usas[3].fragment, usa.FragmentSpec(3, 5, None))
        self.assertEqual(usas.usas[4].fragment, usa.FragmentSpec(3, 8, None))
        self.assertEqual(usas.usas[5].fragment, usa.FragmentSpec(2, 5, True))


class TestUSA(unittest.TestCase):

    def setUp(self):
        self.addTypeEqualityFunc(usa.FragmentSpec, compare_fragment)

    def test_parse_format(self):
        """Check that format specifiers are parsed correctly."""

        usas = usa.parse_usa('fasta::file')
        self.assertEqual(usas.format, 'fasta')

        usas = usa.parse_usa('genbank::file')
        self.assertEqual(usas.format, 'genbank')

    def test_default_format(self):
        """Check that format defaults to FASTA."""

        usas = usa.parse_usa('file')
        self.assertEqual(usas.format, 'fasta')

    def test_explicit_format(self):
        """Check that explicit formats override auto-detection."""

        usas = usa.parse_usa('pearson::file.gb')
        self.assertEqual(usas.format, 'pearson')

    def test_disable_format_autodetection(self):
        """Check that autodetection of format can be disabled."""

        usas = usa.parse_usa('file.gb', extensions_map={})
        self.assertEqual(usas.format, 'fasta')

    def test_parse_fragment_specifier(self):
        """Check that fragment specifiers are parsed correctly."""

        usas = usa.parse_usa('asis::AAAACCCCGGGGTTTT')
        self.assertIsNone(usas.fragment)

        usas = usa.parse_usa('asis::AAAACCCCGGGGTTTT[2:5]')
        self.assertEqual(usas.fragment, usa.FragmentSpec(2, 5, None))

        records = usas.read()
        self.assertEqual(len(records[0]), 4)
        self.assertEqual(records[0].seq, 'AAAC')

        records = usa.read_usa('asis::AAAACCCCGGGGTTTT[8:]')
        self.assertEqual(records[0].seq, 'CGGGGTTTT')

        records = usa.read_usa('asis::AAAACCCCGGGGTTTT[:6:r]')
        self.assertEqual(records[0].seq, 'GGTTTT')

        records = usa.read_usa('asis::AAAACCCCGGGGTTTT[2:-2]')
        self.assertEqual(records[0].seq, 'AAACCCCGGGGTTT')
