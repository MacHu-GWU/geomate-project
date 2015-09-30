Welcome to geomate Documentation
================================================================================

- `GitHub <https://github.com/MacHu-GWU/geomate-project>`_
- `PyPI Homepage <https://pypi.python.org/pypi/geomate>`_
- `Document <https://pypi.python.org/pypi/geomate>`_
- `Install <install_>`_
- `Bug and feature request <https://github.com/MacHu-GWU/geomate-project/issues>`_

Why geomate is so cool?
--------------------------------------------------------------------------------

Let's imaging this:

- We applied multiple API keys. And the program automatically use the available one and stop when none is available.
- The process engine automatically store everything we got into a database, so we can access the result later via ``address``
- The engine automatically handle the errors and exception. And auto retry it later.
- The engine takes address string and also decimal lat, lng tuple, and work smartly.
- The task engine automatically find out those addresses we have done and only work on new one.

That is ``geomate``


Usage Example
--------------------------------------------------------------------------------

Basically, you only need to do three things, and geomate will take care of everything else for you:

1. give me your API keys.
2. name a database file.
3. give me all the address you want to do.

Don't believe? Let's see an real example.

.. code-block:: python

    import geomate
    import pprint

    # put your google map API key here, what you see here is all fake
    api_keys = [ 
        "AIzaSzAuzs8xdbysdYZO1wNV3vVw1Ad3bL_Dnpk", # user1
        "AIzaSyBfgV3y5z_od63NdoTSdu9wgEdg5D_slnk", # user2
        "AIzaSyDsaepgzV7qoczqTW7P2fMmvigxnzg-ZdE", # user3
        "AIzdSyBqgiVid6V2xPZoADqv7dobIfvbhvGhEZA", # ...
        "AIzaSyBtbvGyyAwiywSdsk8-okThcN3qp15GDZQ",
        "AIzbSyC5XmaneaaRYLr4H0h7HMRoFPgjW9xcu2w",
        "AIz3SyDgM5xmKIjS_nooN_TBRLxrFDypVyON9bU",
        "AIzdSyCl95-wDqhxM1CtU3XjvirsAxCU_c1ihu8",   
    ]

    # create a google geocode API client
    googlegeocoder = geomate.GoogleGeocoder(api_keys=api_keys)
    googlegeocoder.check_usable() # show you which keys are available

    # bind to a geocoder and database
    batch = geomate.BatchGeocoder(googlegeocoder, db_file="geocode.sqlite3")

    list_of_address = [ # construct your todo address list anyway you want
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
