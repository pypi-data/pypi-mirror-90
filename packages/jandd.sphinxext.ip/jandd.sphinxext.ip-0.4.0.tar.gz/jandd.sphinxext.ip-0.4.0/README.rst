==================
jandd.sphinxext.ip
==================

This is an IP address extension for `Sphinx`_. The extension provides a domain
*ip* that allows marking IPv4 and IPv6 addresses in documentation and contains
directives to collect information regarding IP addresses in IP ranges.

.. _Sphinx: http://www.sphinx-doc.org/

Development
===========

The extension is developed in a git repository that can be cloned by running::

    git clone https://git.dittberner.info/jan/sphinxext-ip.git

Running test
------------

To install all dependencies and run the tests use::

    pipenv install --dev
    pipenv run pytest

Contributors
============

* `Jan Dittberner`_

.. _Jan Dittberner: https://jan.dittberner.info/
