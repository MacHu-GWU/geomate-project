Welcome to geomate Documentation
===================================================================================================
Features:

- Batch geocoding large amount of data.
- Address or coordinates (reverse geocoding) supported.
- Automatically handle input type, so you can mix address and coordinate in an array.
- Automatically store data in Sqlite database.
- Smart API keys quota management, you would never stuck at getting GeocoderQuotaExceeded error.
- Built in logging system, or you can plug on yours.
- Quick result lookup.


Quick Link:

- `GitHub Homepage <https://github.com/MacHu-GWU/geomate-project>`_
- `Online Documentation <https://pypi.python.org/pypi/geomate>`_
- `PyPI download <https://pypi.python.org/pypi/geomate>`_
- `Install <install_>`_
- `Issue submit and feature request <https://github.com/MacHu-GWU/geomate-project/issues>`_


Usage Example
---------------------------------------------------------------------------------------------------
Basically, you only need to do three things, and geomate will take care of everything else for you:

1. Prepare your API keys.
2. Give the path of your database file.
3. Create a list of address or coordinate you want to geocode.

.. code-block:: python

    import geomate
    import pprint

    # put your google map API key here, what you see here is all fake
    api_keys = [
        "GoogleGeoCodingApiKey01", # user1
        "GoogleGeoCodingApiKey02", # user2
        ...
        "GoogleGeoCodingApiKey99", # user991ihu8",
    ]

    # create a google geocode API client
    googlegeocoder = geomate.GoogleGeocoder(api_keys=api_keys)
    googlegeocoder.check_usable() # show you which keys are available

    # bind to a geocoder and database
    batch = geomate.BatchGeocoder(googlegeocoder, db_file="geocode.sqlite3")

    # construct your todo address list anyway you want
    list_of_address = [
        "675 15th St NW Washington, DC 20005",
        "2317 Morgan Ln Dunn Loring, VA 22027",
        "1201 Rockville Pike Rockville, MD 20852",
        (39.085801, -77.084513),
        (38.872719, -77.306417),
        (38.902027, -77.053536),
    ]

    batch.process(list_of_address) # process everything

    # see what's we have done
    for address in list_of_address:
        pprint.pprint(batch.lookup(address))


.. _install:

Install
--------------------------------------------------------------------------------

``geomate`` is released on PyPI, so all you need is:

.. code-block:: console

    $ pip install geomate

To upgrade to latest version:

.. code-block:: console

    $ pip install --upgrade geomate

Prerequisit: `geopy <https://pypi.python.org/pypi/geopy>`_, to install:

.. code-block:: console

    $ pip install geopy
