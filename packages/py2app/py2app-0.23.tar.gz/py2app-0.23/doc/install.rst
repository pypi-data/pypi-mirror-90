Installation
============


Installing with pip
-------------------

To install py2app using `pip`_, or to upgrade to the latest released version
of py2app:

.. code-block:: sh

  $ pip install -U py2app

If you install into a system installation of Python, you might need additional
privileges; you can use the `sudo`_ commando to get those:

.. code-block:: sh

    $ sudo pip install -U py2app


Installing from source
----------------------

To install py2app from source, simply use the normal procedure for
installing any Python package. Since py2app uses `distribute`_,
all dependencies (including `distribute`_ itself) will be automatically
acquired and installed for you as appropriate:

.. code-block:: sh

    $ python setup.py install

Upgrade Notes
-------------

The ``setup.py`` template has changed slightly in py2app 0.3 in order
to accommodate the enhancements brought on by `setuptools`_. Old ``setup.py``
scripts look like this::

    from distutils.core import setup
    import py2app

    setup(
        app=["myscript.py"],
    )

New py2app scripts should look like this::

    from setuptools import setup
    setup(
        app=["myscript.py"],
	setup_requires=["py2app"],
    )

.. _`setuptools`: http://pypi.python.org/pypi/setuptools/
.. _`pip`: http://www.pip-installer.org/en/latest/
.. _`sudo`: http://www.sudo.ws/sudo/intro.html
