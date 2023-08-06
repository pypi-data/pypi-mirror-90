**************************
Uniform Sequence Addresses
**************************

The ``Incenp.Bioutils`` package supports the `Uniform Sequence Address`_
scheme designed and used by the `EMBOSS package`_. All command-line
tools can read and write sequences from and to a location specified by
such addresses.

.. _Uniform Sequence Address: http://emboss.sourceforge.net/docs/themes/UniformSequenceAddress.html
.. _EMBOSS package: http://emboss.sourceforge.net/what/


Principle and examples
======================

Briefly, a *Uniform Sequence Address* or *USA* is a unified way to
specify the location and optionally the format of a biological sequence.

Please see the EMBOSS document referred to above for a complete
description of USAs, including a formal specification of their syntax.

Here are some examples of USAs:

genbank::file.gb
   Get all sequences in the file ``file.gb``, expected to be in the
   *Genbank* format.

fasta::file.fasta[20:100]
   Get the segment 20..100 from all sequences in the *FASTA* file
   ``file.fasta``.

fasta::file.fast[20:100:r]
   Same as the previous example, but reverse-complement the segments.

genbank::file.gb:SEQ1
   Get the sequence named ``SEQ1`` from the *Genbank* file ``file.gb``.

mydb:SEQ1
   Get the sequence named ``SEQ`` from the database ``mydb``.


Configuration of databases
==========================

To fetch sequences from biological databases as in the last example
above, the databases to use must first be described in a configuration
file located in ``$XDG_CONFIG_HOME/bioutils/databases.ini``.

Each section in this INI-style file describes a database. The database
identifier in a USA must match the name of one of the sections in the
file. For example, the last USA above assumes the ``databases.ini`` file
contains a section named *mydb*.

Within a section, the ``type`` parameter indicates the type of database.
Supported database types are:

biosql
    A SQL database using the BioSQL schema, as supported by Biopython.

expasy
    The ExPASy server.

entrez
    One of the NCBI Entrez database.


BioSQL databases
----------------

A section describing a BioSQL database must contain at least the
following parameters:

driver
    Indicates the Python SQL driver (dependent on the underlying SQL
    database server; for example, ``psycopg2`` for a PostgreSQL server,
    or ``sqlite3`` for a SQLite database).

database
    The name of the database. For a SQLite database, this is the path
    to the database file.

For non-SQLite servers, other parameters indicate how to connect to the
server: ``host`` for the server’s hostname, ``user`` for the name of the
account on the server, ``password`` for the associated password (this
last one may be absent, if the account is not password-protected).

An optional parameter ``subdb`` may contain the name of a BioSQL
subdatabase. If that parameter is present in a section, USAs referring
to that section will only look for sequences in the corresponding
subdatabase (the default is to look in the entire database, regardless
of subdatabases).

If several sections refer to the same BioSQL server (e.g. to describe
several subdatabases in the same server), the connection parameters
(``driver``, ``database``, ``host``, ``user`` and ``password``) may be
replaced by a single ``server`` parameter containing the name of another
section in the file where those parameters are defined.

For example, assuming a PostgreSQL-based BioSQL server containing two
subdatabases named *plasmids* and *genes*, one can have the following
``databases.ini`` file::

    [myserver]
    type: biosql
    driver: psycopg2
    host: localhost
    user: myuser
    password: mypassword
    database: mydatabase

    [plasmids]
    type: biosql
    server: myserver
    subdb: plasmids

    [genes]
    type: biosql
    server: myserver
    subdb: genes

With such a file, the USA ``myserver:SEQ1`` will look for a sequence
named *SEQ1* in all the subdatabases on the server, whereas the USA
``plasmids:SEQ2`` will look for a sequence named *SEQ2* only in the
*plasmids* subdatabase.


ExPAsY database
---------------

This type of database does not need any parameter. USAs referring to
such a database will be resolved by querying directly the ExPASy server.

It is only possible to refer to a sequence by its accession number.
Field-based queries, as described in the USA specification, are not
supported.

Example configuration::

    [uniprot]
    type: expasy

Example USA::

    uniprot:P49450


Entrez databases
----------------

This type of database expects the following parameters:

email
    The email address to send to the NCBI server along with each query.

database
    The Entrez database to use. It can be ``nuccore`` for the DNA/RNA
    database, or ``protein`` for the protein database.

As for the ExPASy database type, only references by accession numbers
are supported.

Example configuration::

    [genbank]
    type: entrez
    email: myemail@example.org
    database: nuccore

    [gbprot]
    type: entrez
    email: myemail@example.org
    database: protein

Example USAs::

    genbank:NM_001809
    gbprot:NP_001800
