DreamSSH Server
===============

Install
-------

You can install from PyPI, which will give you the latest released (hopefully
stable) version of the software::

  $ sudo pip install dreamssh

If you like living on the edge, you can install from the github ``master``
branch::

  $ sudo pip install https://github.com/dreamhost/dreamssh/zipball/master

Finally, you can just get the code itself::

  $ git clone https://github.com/dreamhost/dreamssh.git


Dependencies
-------------

If you used ``pip`` to install DreamSSH, then you will have the necessary
libraries installed. If you will be running from source code, you'll need to do
the following::

  $ sudo pip install pyasn1
  $ sudo pip install PyCrypto
  $ sudo pip install twisted

Once the dependencies are installed, you'll need to generate the keys for use
by the server::

  $ dreamssh-keygen

Running
-------

If you've ``clone`` d the github repo, all you need to do to start up a
DreamSSH server is this::

  $ make daemon
  $ make shell

That will start up an SSH server and then log you into it, using your keys.

Once you have DreamSSH installed, 

Configuring
-----------

TBD

Hacking
-------

TBD
