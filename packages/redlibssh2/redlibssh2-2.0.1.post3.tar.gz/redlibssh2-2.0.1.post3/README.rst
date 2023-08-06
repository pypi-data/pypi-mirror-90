Redlibssh2
============

Super fast SSH2 protocol library. ``redlibssh2`` provides Python bindings for `libssh2`_.
Forked from ssh2-python.

.. image:: https://img.shields.io/badge/License-LGPL%20v2-blue.svg
   :target: https://pypi.python.org/pypi/redlibssh2
   :alt: License
.. image:: https://img.shields.io/pypi/v/redlibssh2.svg
   :target: https://pypi.python.org/pypi/redlibssh2
   :alt: Latest Version
.. image:: https://travis-ci.org/Red-M/redlibssh2.svg?branch=master
   :target: https://travis-ci.org/Red-M/redlibssh2
.. image:: https://img.shields.io/pypi/wheel/redlibssh2.svg
   :target: https://pypi.python.org/pypi/redlibssh2
.. image:: https://img.shields.io/pypi/pyversions/redlibssh2.svg
   :target: https://pypi.python.org/pypi/redlibssh2
.. image:: https://readthedocs.org/projects/redlibssh2/badge/?version=latest
  :target: http://redlibssh2.readthedocs.org/en/latest/
  :alt: Latest documentation


Installation
______________

Binary wheel packages are provided for Linux, OSX and Windows, all Python versions. Wheel packages have **no dependencies**.

``pip`` may need to be updated to be able to install binary wheel packages - ``pip install -U pip``.

.. code-block:: shell

   pip install redlibssh2

For from source installation instructions, including building against system provided libssh2, `see documentation <https://redlibssh2.readthedocs.io/en/latest/installation.html#installation-from-source>`_.

For creating native system packages for Centos/RedHat, Ubuntu, Debian and Fedora, see `instructions in the documentation <http://redlibssh2.readthedocs.io/en/latest/installation.html#system-binary-packages>`_.


Who Should Use This
___________________

Developers of bespoke SSH clients.


Who Should Not Use This
_______________________

Developers looking for ready made SSH clients.

This library is not an SSH client.

Developers looking for high level easy to use clients based on this library should use `RedSSH <https://github.com/Red-M/RedSSH>`_.

This library provides bindings to libssh2 and its API closely matches libssh2.

If the examples seem long, this is not the right library. Use `RedSSH <https://github.com/Red-M/RedSSH>`_.


API Feature Set
________________

At this time all of the `libssh2`_ API has been implemented up to the libssh2 version in the repository. Please report any missing implementation.

Complete example scripts for various operations can be found in the `examples directory`_.

In addition, as ``redlibssh2`` is a thin wrapper of ``libssh2`` with Python semantics, `its code examples <https://libssh2.org/examples/>`_ can be ported straight over to Python with only minimal changes.


Library Features
----------------

The library uses `Cython`_ based native code extensions as wrappers to ``libssh2``.

Extension features:

* Thread safe - GIL is released as much as possible. Note that libssh2 does not support sharing sessions across threads
* Very low overhead
* Super fast as a consequence of the excellent C library it uses and prodigious use of native code
* Object oriented - memory freed automatically and safely as objects are garbage collected by Python
* Use Python semantics where applicable, such as context manager and iterator support for opening and reading from SFTP file handles
* Raise errors as Python exceptions
* Provide access to ``libssh2`` error code definitions


Quick Start
_____________

Both byte and unicode strings are accepted as arguments and encoded appropriately. To change default encoding, ``utf-8``, change the value of ``ssh2.utils.ENCODING``. Output is always in byte strings.

See `Complete Example`_ for an example including socket connect.

Please use either the issue tracker for reporting issues with code.

Contributions are most welcome!


Authentication Methods
-------------------------


Connect and get available authentication methods.


.. code-block:: python

   from __future__ import print_function

   from ssh2.session import Session

   sock = <create and connect socket>

   session = Session()
   session.handshake(sock)
   print(session.userauth_list())


Output will vary depending on SSH server configuration. For example:

.. code-block:: python

   ['publickey', 'password', 'keyboard-interactive']


Agent Authentication
------------------------

.. code-block:: python

   session.agent_auth(user)


Command Execution
------------------------

.. code-block:: python

   channel = session.open_session()
   channel.execute('echo Hello')


Reading Output
---------------

.. code-block:: python

   size, data = channel.read()
   while(size > 0):
       print(data)
       size, data = channel.read()

.. code-block:: python

   Hello


Exit Code
--------------

.. code-block:: python

   print("Exit status: %s" % (channel.get_exit_status()))


.. code-block:: python

   Exit status: 0


Public Key Authentication
----------------------------

.. code-block:: python

   session.userauth_publickey_fromfile(
       username, 'private_key_file')


Passphrase can be provided with the ``passphrase`` keyword param - see `API documentation <https://redlibssh2.readthedocs.io/en/latest/session.html#ssh2.session.Session.userauth_publickey_fromfile>`_.


Password Authentication
----------------------------

.. code-block:: python

   session.userauth_password(
       username, '<my password>')

SFTP Read
-----------

.. code-block:: python

   from ssh2.sftp import LIBSSH2_FXF_READ, LIBSSH2_SFTP_S_IRUSR

   sftp = session.sftp_init()
   with sftp.open(<remote file to read>,
		  LIBSSH2_FXF_READ, LIBSSH2_SFTP_S_IRUSR) as remote_fh, \
           open(<local file to write>, 'wb') as local_fh:
       for size, data in remote_fh:
           local_fh.write(data)


Complete Example
__________________

A simple usage example looks very similar to ``libssh2`` `usage examples <https://www.libssh2.org/examples/>`_.

See `examples directory <https://github.com/Red-M/redlibssh2/tree/master/examples>`_ for more complete example scripts.

As mentioned, ``redlibssh2`` is intentionally a thin wrapper over ``libssh2`` and directly maps most of its API.

Clients using this library can be much simpler to use than interfacing with the ``libssh2`` API directly.

.. code-block:: python

   from __future__ import print_function

   import os
   import socket

   from ssh2.session import Session

   host = 'localhost'
   user = os.getlogin()

   sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
   sock.connect((host, 22))

   session = Session()
   session.handshake(sock)
   session.agent_auth(user)

   channel = session.open_session()
   channel.execute('echo me; exit 2')
   size, data = channel.read()
   while size > 0:
       print(data)
       size, data = channel.read()
   channel.close()
   print("Exit status: %s" % channel.get_exit_status())


:Output:

   me

   Exit status: 2


SSH Functionality currently implemented
________________________________________


* SSH channel operations (exec,shell,subsystem) and methods
* SSH agent functionality
* Public key authentication and management
* SFTP operations
* SFTP file handles and attributes
* SSH port forwarding and tunnelling
* Non-blocking mode
* SCP send and receive
* Listener for port forwarding
* Subsystem support
* Host key checking and manipulation

And more, as per `libssh2`_ functionality.


Comparison with other Python SSH libraries
-------------------------------------------

Performance of above example, compared with Paramiko.

.. code-block:: shell

   time python examples/example_echo.py
   time python examples/paramiko_comparison.py

:Output:

   ``redlibssh2``::

     real	0m0.141s
     user	0m0.037s
     sys	0m0.008s

   ``paramiko``::

     real	0m0.592s
     user	0m0.351s
     sys	0m0.021s

Why did you drop manylinux1 wheels?
___________________________________

Because frankly the manylinux1 docker containers won't run on my build hosts because I run up to date software and kernels.
The manylinux1 docker images are also full of extremely old package versions that will not receive updates or security fixes. The way that ParallelSSH handled this was to bundle their own versions of libssh2, OpenSSL and zlib in the repository.

Why did you drop Windows and OSX wheels?
________________________________________
I don't have build infrastructure for them and I don't use these platforms anywhere.
If someone would like these wheels to be built you can open an issue and it'll be reviewed based on what can be provided to get such builds running.



.. _libssh2: https://www.libssh2.org
.. _Cython: https://www.cython.org
.. _`examples directory`: https://github.com/Red-M/redlibssh2/tree/master/examples
