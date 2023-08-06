
pygments-doconce: syntax coloring for DocOnce files
===================================================

Overview
--------

This package provides a `Pygments <http://pygments.org/>`_ lexer for
`DocOnce <http://doconce.github.io/doconce>`_ files.
The lexer is published as an entry point and, once installed, Pygments will
pick it up automatically.

You can then use the ``doconce`` language with Pygments::

        $ pygmentize -l doconce test.do.txt

In `Sphinx <http://sphinx-doc.org/>`_ documents the lexer is selected with
the ``highlight`` directive::

        .. highlight:: doconce

Thanks to pygments-openssl project for providing a template `<https://github.com/stefanholek/pygments-openssl>`_

Installation
------------

Use your favorite installer to install ``pygments-doconce`` into the same
Python you have installed Pygments.

Installing ``pygments-doconce`` distributed on PyPi:

        $ pip install pygments-doconce

Constructing an egg from repository::

        $ git clone https://github.com/hplgit/pygments-doconce.git
        $ cd pygments-doconce
        $ python setup.py install

DocOnce is needed for the lexer to work. Refer to `DocOnce <http://doconce.github.io/doconce>`

To verify the installation of ``pygments-doconce`` run::

        $ pygmentize -L lexer | grep -i doconce
        * doconce:
        DocOnce