========
Overview
========

.. start-badges

.. list-table::
    :stub-columns: 1

    * - docs
      - |docs|
    * - tests
      - | |travis| |appveyor| |requires|
        | |codecov|
        | |landscape| |scrutinizer| |codeclimate|
    * - package
      - | |version| |wheel| |supported-versions| |supported-implementations|
        | |commits-since|
.. |docs| image:: https://readthedocs.org/projects/python-pytestmar/badge/?style=flat
    :target: https://readthedocs.org/projects/python-pytestmar
    :alt: Documentation Status

.. |travis| image:: https://api.travis-ci.org/Elamraoui-Sohayb/python-pytestmar.svg?branch=master
    :alt: Travis-CI Build Status
    :target: https://travis-ci.org/Elamraoui-Sohayb/python-pytestmar

.. |appveyor| image:: https://ci.appveyor.com/api/projects/status/github/Elamraoui-Sohayb/python-pytestmar?branch=master&svg=true
    :alt: AppVeyor Build Status
    :target: https://ci.appveyor.com/project/Elamraoui-Sohayb/python-pytestmar

.. |requires| image:: https://requires.io/github/Elamraoui-Sohayb/python-pytestmar/requirements.svg?branch=master
    :alt: Requirements Status
    :target: https://requires.io/github/Elamraoui-Sohayb/python-pytestmar/requirements/?branch=master

.. |codecov| image:: https://codecov.io/gh/Elamraoui-Sohayb/python-pytestmar/branch/master/graphs/badge.svg?branch=master
    :alt: Coverage Status
    :target: https://codecov.io/github/Elamraoui-Sohayb/python-pytestmar

.. |landscape| image:: https://landscape.io/github/Elamraoui-Sohayb/python-pytestmar/master/landscape.svg?style=flat
    :target: https://landscape.io/github/Elamraoui-Sohayb/python-pytestmar/master
    :alt: Code Quality Status

.. |codeclimate| image:: https://codeclimate.com/github/Elamraoui-Sohayb/python-pytestmar/badges/gpa.svg
   :target: https://codeclimate.com/github/Elamraoui-Sohayb/python-pytestmar
   :alt: CodeClimate Quality Status

.. |version| image:: https://img.shields.io/pypi/v/pytestmar.svg
    :alt: PyPI Package latest release
    :target: https://pypi.org/project/pytestmar

.. |wheel| image:: https://img.shields.io/pypi/wheel/pytestmar.svg
    :alt: PyPI Wheel
    :target: https://pypi.org/project/pytestmar

.. |supported-versions| image:: https://img.shields.io/pypi/pyversions/pytestmar.svg
    :alt: Supported versions
    :target: https://pypi.org/project/pytestmar

.. |supported-implementations| image:: https://img.shields.io/pypi/implementation/pytestmar.svg
    :alt: Supported implementations
    :target: https://pypi.org/project/pytestmar

.. |commits-since| image:: https://img.shields.io/github/commits-since/Elamraoui-Sohayb/python-pytestmar/v0.0.0.svg
    :alt: Commits since latest release
    :target: https://github.com/Elamraoui-Sohayb/python-pytestmar/compare/v0.0.0...master


.. |scrutinizer| image:: https://img.shields.io/scrutinizer/quality/g/Elamraoui-Sohayb/python-pytestmar/master.svg
    :alt: Scrutinizer Status
    :target: https://scrutinizer-ci.com/g/Elamraoui-Sohayb/python-pytestmar/


.. end-badges

first packagin attempt

* Free software: MIT license

Installation
============

::

    pip install pytestmar

You can also install the in-development version with::

    pip install https://github.com/Elamraoui-Sohayb/python-pytestmar/archive/master.zip


Documentation
=============


https://python-pytestmar.readthedocs.io/


Development
===========

To run all the tests run::

    tox

Note, to combine the coverage data from all the tox environments run:

.. list-table::
    :widths: 10 90
    :stub-columns: 1

    - - Windows
      - ::

            set PYTEST_ADDOPTS=--cov-append
            tox

    - - Other
      - ::

            PYTEST_ADDOPTS=--cov-append tox
