**************************
Installing Incenp.Bioutils
**************************

Installing from PyPI
====================

Packages for Incenp.Bioutils are published on the
`Python Package Index`_ under the name ``incenp.bioutils``. To install
the latest version from PyPI:

.. _Python Package Index: https://pypi.org/project/incenp.bioutils/

.. code-block:: console

   $ pip install -U incenp.bioutils


Installing from source
======================

You may download a release tarball from the `homepage`_ or from the
`release page`_, and then proceed to a manual installation:

.. _homepage: https://incenp.org/dvlpt/bioutils.html
.. _release page: https://git.incenp.org/damien/bioutils/releases

.. code-block:: console

   $ tar zxf incenp.bioutils-|version|.tar.gz
   $ cd incenp.bioutils-|version|
   $ python setup.py build
   $ python setup.py install

You may also clone the repository:

.. code-block:: console

   $ git clone https://git.incenp.org/damien/bioutils.git

and then proceed as above.


Dependencies
============

Incenp.Bioutils requires the following Python dependencies to work:

* `Biopython <https://biopython.org>`_
* `Click <https://palletsprojects.com/p/click/>`_
* `Click-Shell <https://github.com/clarkperkins/click-shell>`_

If you install Incenp.Bioutils from the Python Package Index with `pip`
as described above, those dependencies should be automatically installed
if they are not already available on your system.


Testing the installation
========================

You can check whether Incenp.Bioutils has been installed correctly by
trying to invoke one of the command-line utilities it provides:

.. code-block:: console

   $ seqtool --version
   seqtool |version|
   Copyright © 2020 Damien Goutte-Gattat

   This program is released under the GNU General Public License.
   See the COPYING file or <http://www.gnu.org/licenses/gpl.html>
