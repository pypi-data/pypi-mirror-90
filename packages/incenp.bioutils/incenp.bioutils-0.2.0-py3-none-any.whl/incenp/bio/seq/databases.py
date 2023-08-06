# -*- coding: utf-8 -*-
# Incenp.Bioutils - Incenp.org's utilities for computational biology
# Copyright © 2018,2020 Damien Goutte-Gattat
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

"""Uniform access to biological databases.

The purpose of this module is to provide a uniform way to fetch
sequences from a range of biological databases. One use of this module
is to provide the backend to make database-backed USAs work, but the
database adapters defined here can also be used on their own.
"""

from configparser import ConfigParser, NoOptionError
from os import getenv
from urllib.error import HTTPError

from Bio import Entrez
from Bio import ExPASy
from Bio import SeqIO
from BioSQL.BioSeq import DBSeqRecord
from BioSQL.BioSeqDatabase import open_database
from incenp.bio import Error


class DatabaseProvider(object):
    """Provides database adapters for biological databases.
    
    This object provides a unique way to access a set of user-configured
    set of sequence databases.
    
    The databases this object gives access to should be described in a
    INI-style configuration file, located in 
    `$XDG_CONFIG_HOME/bioutils/databases.ini`.
    
    Each section in the configuration file describes a database. Within a
    section, the mandatory ``type`` parameter indicates the type of
    database and therefore the type of database adapter to use to query
    that database. Other parameters are dependent on the database type.
    
    Supported database types:
    
    BioSQL database (``type: biosql``)
      Any database following the BioSQL scheme. Parameters for this type
      of database are:
      
      * ``driver`` indicating the SQL driver to use;
      * ``host`` for the hostname of the SQL server;
      * ``user`` for the user account to connect to the server with;
      * ``password`` for the associated password;
      * ``database`` for the SQL database name;
      * ``subdb`` for the name of the BioSQL subdatabase, if any.
      
    ExPASy database (``type: expasy``)
      The ExPASy server. This type expects no parameter.
      
    Entrez database (``type: entrez``)
      One of the NCBI Entrez database. Parameters for this type of
      database are:
      
      * ``email`` for the email address to send to the NCBI server along
        with each query;
      * ``database`` for the name of the Entrez database (can be
        ``nuccore`` or ``protein``, for the DNA/RNA or protein database
        respectively).
        
    Here is an example configuration file::
    
         [db1]
         type: biosql
         host: localhost
         user: bioutils
         database: mydb
         
         [uniprot]
         type: expasy
         
         [genbank]
         type: entrez
         email: bioutils@example.org
         database: nuccore
         
    With such a configuration file, the database provider can either be
    used directly::
    
        # Create the object and parse the configuration file
        dbprovider = DatabaseProvider()
        
        # Query the ExPASy server
        dbprovider['uniprot'].fetch('NP_001800')
        
    or through a USA::
    
        # Query the ExPASy server
        usa.read_usa('uniprot::NP_001800', databases=dbprovider)
        
    """

    def __init__(self):
        self.cfg = ConfigParser()
        self.adapters = {}
        self.biosql_servers = {}

        cfg_file = '{}/bioutils/databases.ini'.format(
            getenv('XDG_CONFIG_HOME', default='{}/.config'.format(
                getenv('HOME', default='.'))))
        self.cfg.read(cfg_file)

    def __contains__(self, database):
        """Check if the specified database name exists."""

        return self.cfg.has_section(database)

    def __getitem__(self, database):
        """Gets the adapter for the specified database name."""

        if not database in self.adapters:
            self._init_database(database)
        return self.adapters[database]

    def close(self):
        """Frees all resources associated with the databases."""

        for adapter in self.adapters.values():
            adapter.close()
        for server in self.biosql_servers.values():
            server.close()

    def _init_database(self, database):
        if not self.cfg.has_section(database):
            raise Error(f"No configuration for database {database!r}")

        try:
            dbtype = self.cfg.get(database, 'type')
        except NoOptionError:
            raise Error(f"No type specified for database {database!r}")

        if dbtype == 'biosql':
            server = self._get_biosql_server(database)
            subdb = self.cfg.get(database, 'subdb', fallback=None)
            if subdb:
                if not subdb in server:
                    raise Error(f"No subdatabase {subdb} on server")
                adapter = BioSqlAdapter(server[subdb].adaptor,
                                        server[subdb].dbid)
            else:
                adapter = BioSqlAdapter(server.adaptor)

            self.adapters[database] = adapter
        elif dbtype == 'expasy':
            self.adapters[database] = ExpasyAdapter()
        elif dbtype == 'entrez':
            try:
                email = self.cfg.get(database, 'email')
                dbname = self.cfg.get(database, 'database')
            except NoOptionError:
                raise Error("Incomplete configuration for database "
                            f"{database!r}")

            if dbname not in ['nuccore', 'protein']:
                raise Error(f"Invalid database for {database!r}: {dbname}")

            self.adapters[database] = EntrezAdapter(email, dbname)
        else:
            raise Error(f"Unsupported database type: {dbtype}")

    def _get_biosql_server(self, name):
        if not name in self.biosql_servers:

            if not self.cfg.has_section(name):
                raise Error(f"No section {name!r}")

            if self.cfg.has_option(name, 'server'):
                return self._get_biosql_server(self.cfg.get(name, 'server'))

            conn_settings = {}
            try:
                driver = self.cfg.get(name, 'driver')
                conn_settings['driver'] = driver

                if driver == 'sqlite3':
                    conn_settings['database'] = self.cfg.get(name, 'database')
                else:
                    conn_settings['host'] = self.cfg.get(name, 'host')
                    conn_settings['user'] = self.cfg.get(name, 'user')
                    conn_settings['database'] = self.cfg.get(name, 'database')
                    conn_settings['password'] = self.cfg.get(name, 'password',
                                                             fallback=None)
            except NoOptionError:
                raise Error(f"Incomplete configuration for database {name!r}")

            try:
                server = open_database(**conn_settings)
            except Exception as e:
                raise Error("Cannot connect to BioSQL server", e)

            self.biosql_servers[name] = server

        return self.biosql_servers[name]


class DatabaseAdapter(object):
    """Base class for database-specific access providers.
    
    This class defines the common interface shared by all the database
    adapters.
    """

    def query(self, field, pattern):
        """Gets records matching the specified query pattern.
        
        This method queries the underlying database for all records
        matching the indicated pattern in the specified field.
        
        The *field* argument can take the following values:
        
        * ``acc`` to search for an accession number;
        * ``id`` to search for a record name;
        * ``sv`` to search for a versioned accession number or a
          sequence identifier;
        * ``des`` to search for words in a record's description;
        * ``org`` to search for an organism;
        * ``key`` to search for words in a record's keywords.
        
        Not all database adapters may support all those types of
        queries.
        
        The *pattern* argument may contain wildcards: ``?`` stands for
        any character, and ``*`` stands for any number of characters.
        Not all database adapters may support wildcards.
        
        :param field: the database field to search against
        :param pattern: the pattern to search for
        :return: the matching records, as a list of
            :class:`Bio.SeqRecord.SeqRecord` objects (or objects with a
            compatible interface, such as
            :class:`BioSQL.BioSeq.DBSeqRecord`)
        """

        raise Error("Querying this database is not supported")

    def fetch(self, identifier):
        """Gets records matching the specified identifier.
        
        This method queries the underlying database for all records
        whose name or accession number matches the specified pattern.
        
        The identifier may contain wildcards: ``?`` stands for any
        character, and ``*`` stands for any number of characters. Not
        all database adapters may support wildcards.
        
        :param identifier: the pattern to look for
        :return: the matching records, as a list of 
            :class:`Bio.SeqRecord.SeqRecord` objects (or objects with a
            compatible interface, such as
            :class:`BioSQL.BioSeq.DBSeqRecord`)
        """

        raise Error("Fetching from this database is not supported")

    def fetchall(self):
        """Gets all records in the database.
        
        This method returns *all* the records contained in the
        underlying database.
        
        Not all database adapters may support this method. In
        particular, it is expected that adapters for online databases
        will most likely not support it.
        
        :return: the database records, as a list of
            :class:`Bio.SeqRecord.SeqRecord` objects (or objects with a
            compatible interface, such as
            :class:`BioSQL.BioSeq.DBSeqRecord`)
        """

        raise Error("Fetching all records from this database is not "
                    "supported")

    def close(self):
        """Frees resources associated with the database."""

        pass


def _pattern_to_sql_pattern(pattern):
    pat = []
    for char in pattern:
        if char in '%_':
            pat.append('\\')
            pat.append(char)
        elif char == '?':
            pat.append('_')
        elif char == '*':
            pat.append('%')
        else:
            pat.append(char)
    return ''.join(pat)


class BioSqlAdapter(DatabaseAdapter):
    """Adapter for BioSQL-based sequence databases.
    
    This adapter provides access to any biological database following
    the BioSQL schema, as supported by Biopython's ``Bio.BioSQL``
    module.
    
    Usage::
    
        from BioSQL.BioSeqDatabase import open_database
        
        server = open_database(...)
        
        # For a server-wide adapter
        adapter = BioSqlAdapter(server.adaptor)
        
        # For an adapter restricted to a subdatabase
        database = server[database_name]
        adapter = BioSqlAdapter(database.adaptor, database.dbid)

    """

    def __init__(self, adaptor, dbid=None):
        """Creates a new BioSQL database adapter.
        
        :param adaptor: a :class:`BioSQL.BioSeqDatabase.Adaptor` object
            connected to the target database
        :param dbid: a BioSQL subdatabase identifier; if ``None``,
            queries will search for records in the entire BioSQL server,
            regardless of subdatabases
        """

        self.adaptor = adaptor
        self.dbid = dbid

    def query(self, field, keyword):
        if field == 'acc':
            sql = (
                'SELECT bioentry_id FROM bioentry '
                'WHERE accession LIKE %s ESCAPE \'\\\''
                )
            args = [_pattern_to_sql_pattern(keyword)]
        elif field == 'id':
            sql = (
                'SELECT bioentry_id FROM bioentry '
                'WHERE name LIKE %s ESCAPE \'\\\''
                )
            args = [_pattern_to_sql_pattern(keyword)]
        elif field == 'sv':
            if '.' in keyword:
                accession, version = keyword.split('.')
                if '*' in version or '?' in version:
                    # Version is represented as an integer in the BioSQL
                    # schema and cannot be matched against a pattern,
                    # so here we don't match on version at all.
                    sql = (
                        'SELECT bioentry_id FROM bioentry '
                        'WHERE accession LIKE %s ESCAPE \'\\\''
                        )
                    args = [_pattern_to_sql_pattern(accession)]
                else:
                    sql = (
                        'SELECT bioentry_id FROM bioentry '
                        'WHERE (accession LIKE %s ESCAPE \'\\\' '
                        '       AND version = %s)'
                        )
                    args = [_pattern_to_sql_pattern(accession), version]
            else:
                sql = (
                    'SELECT bioentry_id FROM bioentry '
                    'WHERE (accession LIKE %s ESCAPE \'\\\' '
                    '       OR identifier LIKE %s ESCAPE \'\\\')'
                    )
                pattern = _pattern_to_sql_pattern(keyword)
                args = [pattern, pattern]
        else:
            raise Error(f"Unsupported search field: {field}")

        if self.dbid is not None:
            sql = sql + ' AND biodatabase_id = %s'
            args.append(self.dbid)

        res = self.adaptor.execute_and_fetchall(sql, args)
        return [DBSeqRecord(self.adaptor, r[0]) for r in res]

    def fetch(self, identifier):
        pattern = _pattern_to_sql_pattern(identifier)
        sql = (
            'SELECT bioentry_id FROM bioentry '
            'WHERE (accession LIKE %s ESCAPE \'\\\' '
            '       OR name LIKE %s ESCAPE \'\\\')'
            )
        args = [pattern, pattern]

        if self.dbid is not None:
            sql += ' AND biodatabase_id = %s'
            args.append(self.dbid)

        res = self.adaptor.execute_and_fetchall(sql, args)
        return [DBSeqRecord(self.adaptor, r[0]) for r in res]

    def fetchall(self):
        if self.dbid is not None:
            sql = (
                'SELECT max(bioentry_id) FROM bioentry '
                'WHERE biodatabase_id = %s '
                'GROUP BY accession ORDER BY accession'
                )
            args = [self.dbid]
        else:
            sql = (
                'SELECT max(bioentry_id) FROM bioentry '
                'GROUP BY accession ORDER BY accession'
                )
            args = []
        res = self.adaptor.execute_and_fetchall(sql, args)
        return [DBSeqRecord(self.adaptor, r[0]) for r in res]


class ExpasyAdapter(DatabaseAdapter):
    """Adapter for the ExPASy sequence server.
    
    This adapter queries the ExPASy server to fetch sequences directly
    over the Internet.
    
    Only queries by identifier (without wildcards) are supported.
    """

    def fetch(self, identifier):
        try:
            handle = ExPASy.get_sprot_raw(identifier)
        except ValueError:
            return []
        except HTTPError as e:
            raise Error(f"Cannot fetch sequence {identifier}", e)

        return [rec for rec in SeqIO.parse(handle, 'swiss')]


class EntrezAdapter(DatabaseAdapter):
    """Adapter for the NCBI E-Utilities.
    
    This adapter queries the NCBI server to fetch sequences directly
    over the Internet.
    
    Only queries by identifier (without wildcards) are supported.
    """

    def __init__(self, email, database):
        """Creates a new Entrez adapter.
        
        :param email: the email address to pass on to the NCBI server
            along with any query
        :param database: the name of the Entrez database to query; can
            be ``nuccore`` or ``protein``, for DNA/RNA or protein
            sequences respectively
        """
        self.database = database
        Entrez.email = email

    def fetch(self, identifier):
        try:
            handle = Entrez.efetch(db=self.database, id=identifier,
                                   rettype='gb', retmode='text')
        except HTTPError as e:
            raise Error(f"Cannot fetch sequence {identifier}", e)

        return [rec for rec in SeqIO.parse(handle, 'genbank')]
