Endi Split pdf
###############

Split a large pdf file into several pieces.

Licence
--------

This is a free software (GPLv3), see LICENCE.txt for licencing info.

What does it do
----------------

Provide a PDF file with all the salary sheets (or other type). In each page, you
provide an ancode and a name ("name" of the employee and a specific key called
"ancode").  This program splits the pdf into separated salary sheets.

It allows the people in charge of the salary sheet distribution to generate a
file from their accounting software and to get an output with a structured
directory structure.

enDI matches that directory structure to distribute the salary sheets through
its interface.

By extension, it's possible to configure splitting for several type of data.

How
....

The original file is named <filetype>_<year>_<month>.pdf (e.g :
salaire_2020_11.pdf).

- The filetype is used to fetch the appropriate parsing configuration.

- The generated pdfs are placed under a directory named
  <filetype>/<year>/<month>/.

Using the configuration the tool searches for an "ancode" and a "name"
into the pdf pages. It generates files in the form <ancode>_<name>.pdf
containing the pages with the associated keywords, into the appropriate
directory.

Installation
-------------

Distro dependencies
....................

Install the pdftotext command line tool.

Debian based distros

.. code-block:: console

    apt-get install poppler-utils virtualenvwrapper

Install from pypi
..................

.. code-block:: console

    mkvirtualenv splitpdf
    pip install endi-split-pdf

Install from source
.....................

Setup a python virtual environment

.. code-block:: console

    mkvirtualenv splitpdf
    pip install -r requirements.txt
    pip install -e

Development mode
.................

.. code-block:: console

    pip install -e .[dev]


Configuration
--------------

Main config file
  Defaults to `~/.endi_split_pdf_config.yaml`
  Specifiable by use -c <configfile>

Format is yaml.

Configure :

    - Filetypes
    - For each filetype, a parsing strategy describing the datatype to extract,
      the way they are extracted and the name of the file to generate. (Several
      parser can be provided, here we have three parsers for ancode and two for
      name)


Example

.. code:: yaml

    salaire:
        filename_template: {data1}_{data2}_{data3}.pdf
        datatypes:
           data1:
              - type: regex
                regex: '[\s]{30,80}(?P<ancode>[A-Z]{4,12})\s+'
                from_line: 11
                to_line: 14
                strict: True
                regex_group_name: ancode

              - type: coordinates
                line: 12
                column: 40
                prefix: "     "
              - type: coordinates
                line: 13
                column: 40
                prefix: "     "

            data2:
              - type: regex
                regex: '\s+(M|Mme|Mlle)\s+(?P<name>[\w\s]+)(\n|$)'
                from_line: 6
                to_line: 9
                regex_group_name: name
                strict: True

              - type: coordinates
                line: 8
                column: 50

            data3:
              - type: coordinates
                line: 2
                column: 60
                prefix: "Section :"



Here we configured the parsing of files named salaire_<year>_<month>.pdf

For each page, we'll extract three data and group all pages by matching
data1/data2/data3 3-uples. The pages will be grouped in a file named with the
`filename_template`.

Finders
........

For each data you can cumulate several "finders" to achieve data retrieval.
Finders are used in the specified order.

There are two types of finders.

RegexDataFinder
~~~~~~~~~~~~~~~~~

Use a regex to find the data in the page's string representation (pdftotext
output)

regex

    The regex to use for matching the data (ancode or name) we're looking for.

strict (default to False)

    If True a result is returned if only one item matches the regexp

from_line / to_line (optionnal)

    Specify a range of lines to restrict the amount of data we look at
    The Finder will only look between from_line and to_line line numbers (starts
    with 1).

regex_group_name (optionnal)

    If the regexp uses groups, specify the group matching the data


CoordinateDataFinder
~~~~~~~~~~~~~~~~~~~~~

Use coordinates to find the data in the page's string representation (pdftotext
output)

line

    The line where to look for the data

column

    Where to start in the line

prefix (optionnal)

    A prefix after which we should find the data


Logging
.........

This program supports advanced logging configuration with the following options.

.. code-block:: yaml

    verbosity: DEBUG

Available options are DEBUG/INFO/WARNING/ERROR/CRITICAL

Syslog logging
~~~~~~~~~~~~~~~~

.. code-block:: yaml

    use_syslog: true

Mail logging
~~~~~~~~~~~~~~

.. code-block:: yaml

    log_to_mail: true
    mail:
        host: localhost
        from: admin@host.fr
        to: contact@example.net
        subject: '[%(hostname)s] Log of the pdf splitter'


That program is smart enough to use syslog if the config specifies it.

It logs to mail if the config contains `log_to_mail: True`


Examples
--------

A full run::

    endi-split-pdf-run -c myconfig.yaml playground/salaires_2013_07.pdf

Test that the file is parseable on the 5 first pages::

    endi-split-pdf-run  -c myconfig.yaml playground/salaires_2013_07.pdf -r 5

Use `-v` for debug messages.

Use `-h` to get a complete overview of options.


Known problems
--------------

* for payrolls
    cannot handle some PDF files, especially if there is no outline and the
    charset is 'binary'.
    Check this with::

        file -i $filename.pdf

Known problems
---------------

When the logs returns messages like :

CRITICAL  - No page of output!

If the end user generates his files with Sage "Édition pilotée", the problem may
be that the end user used "print to PDF" export instead of "Save to PDF".
