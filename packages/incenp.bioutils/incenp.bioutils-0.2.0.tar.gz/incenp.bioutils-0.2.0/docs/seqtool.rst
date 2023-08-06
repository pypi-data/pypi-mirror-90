*******************
The seqtool command
*******************

The ``seqtool`` command provides subcommands to perform various
operations on sequence files.

All subcommands operate on sequences specified as :doc:`Uniform Sequence
Addresses <usa>`.


The cat subcommand
==================

The ``cat`` subcommand is analog to the Unix command of the same name.
It reads sequence files and writes out another sequence file. It can be
used for several purposes:

* converting a sequence file from one format to another;
* clean up a sequence file from spurious annotations left by some
  molecular biology programs;
* catenate several sequences into a single sequence (keeping all the
  associated sequence features).


Examples
--------

Converting a Genbank file into a FASTA file::

    $ seqtool cat genbank::file.gb -o fasta::file.fasta

Creating a new sequence by catenating several input sequences together,
and setting some annotations in the resulting sequence::

    $ seqtool -o genbank::result.gb \
      --name "NEWSEQ" \
      --description "This is my catenated sequence" \
      --division SYN \
      --clean
      fasta::left.fasta abi::middle.ab1 genbank::left.gb


The siresist subcommand
=======================

The ``siresist`` subcommand takes a DNA sequence as input and generate
a new DNA sequence with the same translation but using different codons.


The gateway subcommand
======================

The ``gateway`` subcommand performs *in silico* Gatewayⓡ  reactions. It
automatically detects the appropriate *attB/P/L/R* sites within the two
input sequences and generates an output sequence with all the features
appropriately copied over.


The plasmm subcommand
=====================

Given the annotated sequence of a plasmid, the ``plasmm`` subcommand
generates a PDF file describing that plasmid, with a map and list of the
main sequence features.


The blast and dotter subcommands
================================

Those are wrappers for the different BLAST commands (``blastn``,
``blastp``, ``tblastn``, and so on) from the `NCBI BLAST package`_ and
the ``dotter`` command from the `SeqTools package`_.

.. _NCBI BLAST package: https://blast.ncbi.nlm.nih.gov/Blast.cgi?CMD=Web&PAGE_TYPE=BlastDocs&DOC_TYPE=Download
.. _SeqTools package: https://www.sanger.ac.uk/tool/seqtools/

They don’t give access to all the options of the original programs, but
their main interest is that they can be used with sequences in any format
supported by Biopython’s ``SeqIO`` module, whereas the original programs
only read files in the FASTA format.
