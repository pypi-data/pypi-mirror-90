********************
The seqvault command
********************

The ``seqvault`` command provides a command-line interface to `BioSQL`_
databases.

.. _BioSQL: https://biosql.org/

It is intended to be used with a slightly modified version of the BioSQL
database schema (provided with ``Incenp.Bioutils`` source code in the
``biosql`` directory), where every `biodatabase` is associated with a
3-letters prefix. That prefix is then used to automatically assign
accession numbers (of the form ``PRE_xxxxxx``, where ``PRE`` is the
prefix) when importing sequences into the database. However ``seqvault``
can also be used with pristine BioSQL databases.


Setting up the BioSQL database
==============================

If you don’t already have a BioSQL database (or access to one), follow
those instructions to setup one.


With PostgreSQL
---------------

Create a new PostgreSQL user account and a new database::

    # createuser <username>
    # createdb -O owner <username> <dbname>

Initialize the newly created database by running the provided
``biosql/biosqldb-pgsql.sql`` script::

    # psql -h localhost -U <username> <dbname> < biosql/biosqldb-pg.sql


With SQLite
-----------

Create and initialize the database with the following command::

    $ sqlite3 mydb.sqlite < biosql/biosqldb-sqlite.sql


Configuring seqvault
====================

Create an INI-style configuration file named ``databases.ini`` in the
``$XDG_CONFIG_HOME/bioutils`` directory, describing the BioSQL server(s)
to use with ``seqvault``. For example, to access the two databases
created above, use the following file::

    [db1]
    type: biosql
    driver: psycopg2
    host: localhost
    user: <username>
    database: <dbname>

    [db2]
    type: biosql
    driver: sqlite3
    database: <path/to/mydb.sqlite>

If the ``username`` user account on the PostgreSQL is password-protected,
add a ``password`` option in the corresponding section.

The ``seqvault`` program will by default connect to the first server
described in the configuration file. Use the ``-s`` option to choose
another section from the configuration file.


Using seqvault
==============

The following examples show some typical uses of ``seqvault``.

Creating a new BioSQL subdatabase named *plasmids* with the prefix
``PLM``::

    $ seqvault newdb -p PLM plasmids

Importing a sequence from a file into the subdatabase::

    $ seqvault add plasmids genbank::file.gb

Listing all sequences in a subdatabase::

    $ seqvault list plasmids

Extracting a sequence from a subdatabase::

    $ seqvault get PLM_123456

