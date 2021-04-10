.. tft_parse documentation master file, created by
   sphinx-quickstart on Wed Apr  7 17:28:12 2021.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

tft_parse
==========

This is a parser for Teamfigt Tactics (TFT) match history. The purpose of this library is
to quickly get match related info.

**Example**::
    >>> match = tft_parse.MatchDto(data)
    >>> match.metadata.region
    'OC1'
    >>>print(match.metadata.__dict__)

.. toctree::
   :maxdepth: 2
   :caption: Contents:


Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`