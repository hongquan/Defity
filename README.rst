======
Defity
======

|image love| |image pypi| |doc badge|

Speedy Python library to determine MIME type of file.


.. image:: https://raw.githubusercontent.com/hongquan/Defity/main/skunk.svg
  :alt: logo


Defity (**De**\tect **fi**\le **ty**\pe) is a library for Python application to guess file type in a reliable way, not based on filename extension ( *\*.png*, *\*.pdf*), but on actual file content. It is like what |file|_ command and |libmagic|_ library do, but with different strategy.

📕 Documentation: `defity.readthedocs.io`_


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


How different with libmagic-based ones?
---------------------------------------

There are many Python libraries also do the same thing, most of them are based on wellknown *libmagic*. Defity is based on Rust |tree_magic_mini|_ library, which in turn is a fork of |tree_magic|_ , another Rust library. Quote from ``tree_magic`` to see how it differs from ``libmagic``:

  Unlike the typical approach that libmagic and file(1) uses, this loads all the file types in a tree based on subclasses. (EX: application/vnd.openxmlformats-officedocument.wordprocessingml.document (MS Office 2007) subclasses application/zip which subclasses application/octet-stream) Then, instead of checking the file against every file type, it can traverse down the tree and only check the file types that make sense to check. (After all, the fastest check is the check that never gets run.)

  This library also provides the ability to check if a file is a certain type without going through the process of checking it against every file type.


And what ``tree_magic_mini`` has improved over ``tree_magic``:

  Reduced copying and memory allocation, for a slight increase in speed and decrease in memory use.


So, ``Defity`` should have better performance than other libraries for the same purpose.

Another advantage is that, ``Defity`` is static linked to the underlying Rust library, not depend on discrete *libmagic.so*. It will be easier to deploy to cloud function platforms, where you don't have control over what system libraries is present there.


License
-------

In general, Defity is licensed under Apache-2.0 if it is built without |tree_magic_mini|_ embedded MIME database, and is licensed under GPL-3.0 otherwise. Concretely:

- On Linux, it is licensed under Apache-2.0.
- On Windows and MacOS, it is licensed under GPL-3.0.

It is because, Linux boxes already come with FreeDesktop's `MIME database <mime_db_>`_, Defity just uses it.
Windows and MacOS don't have this database and Defity has to embed with it.


Credit
------


* Author: `Nguyễn Hồng Quân <author_>`_.
* Free icon is made by `Vitaly Gorbachev <vitaly_>`_ from `flaticon.com`_.


.. |image love| image:: https://madewithlove.vercel.app/vn?heart=true&colorA=%23ffcd00&colorB=%23da251d
.. |image pypi| image:: https://badgen.net/pypi/v/defity
   :target: https://pypi.org/project/defity
.. |doc badge| image:: https://readthedocs.org/projects/defity/badge/?version=latest
   :target: https://defity.readthedocs.io/en/latest/?badge=latest
   :alt: Documentation Status
.. _defity.readthedocs.io: https://defity.readthedocs.io/
.. |file| replace:: ``file``
.. _file: https://helpmanual.io/man1/file
.. |libmagic| replace:: ``libmagic``
.. _libmagic: https://helpmanual.io/man3/libmagic
.. |tree_magic_mini| replace:: ``tree_magic_mini``
.. _tree_magic_mini: https://crates.io/crates/tree_magic_mini
.. |tree_magic| replace:: ``tree_magic``
.. _tree_magic: https://crates.io/crates/tree_magic
.. _mime_db: https://www.freedesktop.org/wiki/Specifications/shared-mime-info-spec/
.. _author: https://quan.hoabinh.vn
.. _vitaly: https://www.flaticon.com/authors/vitaly-gorbachev
.. _flaticon.com: https://www.flaticon.com/free-icon/skunk_2301541
