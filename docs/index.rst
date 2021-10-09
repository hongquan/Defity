.. Defity documentation master file, created by
   sphinx-quickstart on Wed Aug 25 10:44:55 2021.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Defity
======

Speedy Python library to determine MIME type of file.


Install
-------

.. code-block:: console

  $ pip install defity


Usage
-----

.. code-block:: python

  >>> import defity
  >>> defity.from_file('path/to/landscape.png')
  'image/png'
  >>> with open('path/to/landscape.png', 'rb') as f:
  ...     defity.from_file(f)
  ...
  'image/png'

  >>> defity.from_bytes(b'some-binary-content')
  'image/png'


.. toctree::
   :maxdepth: 2
   :caption: More:

   api-ref
