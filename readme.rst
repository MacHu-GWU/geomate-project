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


.. _usage:

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

    batch.process_this(list_of_address) # process everything

    # see what's we have done
    for address in list_of_address:
        pprint.pprint(batch.lookup(address))

.. image:: http://pythonhosted.org/geomate/_static/GeomateLog.png


.. _advance:

Advance Usage
---------------------------------------------------------------------------------------------------
Suppose you got 10000 address, but 5000 of them are invalid address, which is not able to geocoded. And invalid address happens to be at begin of the queue. You probably don't want to waste API quota on that. geomate provide a keyword ``shuffle`` to randomlly perform the geocoding, so in average, you can get most of valid address geocoded in a short time:

.. code-block:: python

    batch.process_this(list_of_address, shuffle=True)


Here's something may helpful. Basically there are two steps in the processing:

1. Insert to-do addresses as primary key into a table, and skip address already in database.
2. Do geocoding.

So you can take advantage of this for more flexible batch geocoding process.

.. code-block:: python

    batch.add_addresses(list_of_address)
    batch.process_all(shuffle=True)
    

.. _lookup:

Lookup the geocoded data
--------------------------------------------------------------------------------
You can easily retrieve the geocoded data by:

.. code-block:: python

    for address in list_of_address:
        data = batch.lookup(address)
        pprint(data)

Of course you can also manually read it from sqlite database.


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
