tft_parse
=========

Implementation of TFT's `api`_. The purpose of this library is to quickly get info from match's json.

Example
-------

.. code-block:: python

    >>> import tft_parse
    >>> import requests
    >>> import json

    >>> data = requests.get('https://raw.githubusercontent.com/tftdata/tft_parse/main/tests/match.json')
    >>> data = json.loads(data.content)

    >>> match = tft_parse.MatchDto(data)

    >>> print(match.info.patch)
    11.3
    >>> print(match.metadata.region)
    OC1





.. _api: https://developer.riotgames.com/apis#tft-match-v1