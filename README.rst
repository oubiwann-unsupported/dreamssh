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

  $ twistd dreamssh keygen

Running
-------

Once you have DreamSSH installed, interacting with the server is as easy as the
following::

  $ twistd dreamssh

That will run in daemonized mode. If you'd like to run it in the foreground and
watch the log output to stdout, just do::

  $ twistd dreamssh run

To log into the shell, use this command::

  $ twistd dreamssh shell

If you'd like to try out the alternate "toy" shell::

  $ twistd dreamssh --interpreter=echo

For those who have a ``clone`` of the git repo, there are development
convenience make targets::

  $ make keygen
  $ make daemon
  $ make run
  $ make shell

Configuring
-----------

TBD

Hacking
-------

TBD
