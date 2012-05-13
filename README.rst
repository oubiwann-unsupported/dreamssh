DreamSSH Server
===============

Features
--------

*What does this give me, over and above the default ``manhole`` capabilities of
``twistd``?*

DreamSSH provides, out of the box, the following:

* configurable banner/MOTD

* the ability to templatize your banner (e.g., changing the "help" based on
   interpreter type)

* it provides an easy means of generating keys (and then uses them
  automatically)

* by default, uses the local filesystems SSH keys for authenticating users

* provides an easy mechanism for creating your own shell


And there's more coming:

* shared sessions (multiple uses in a single space)

* multiple filesystem locations for user ssh keys

* user roles

* a status bar (maybe)

* automated sign-up functionality 


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

    $ twistd -n dreamssh

To log into the shell, use this command::

    $ twistd dreamssh shell

If you'd like to try out the alternate "toy" shell::

    $ twistd dreamssh --interpreter=echo

When you're ready to shut it down::

    $ twistd dreamssh stop

For those who have a ``clone`` of the git repo, there are development
convenience make targets::

    $ make keygen
    $ make daemon
    $ make run
    $ make shell
    $ make stop


Using
-----

When you log into the Python shell::

    $ twistd dreamssh shell

You are greeted with something that looks like this::

    :>> 
    :
    : Welcome to
    :
    :________                              ____________________  __
    :___  __ \_________________ _______ _____  ___/_  ___/__  / / /
    :__  / / /_  ___/  _ \  __ `/_  __ `__ \____ \_____ \__  /_/ /
    :_  /_/ /_  /   /  __/ /_/ /_  / / / / /___/ /____/ /_  __  /
    :/_____/ /_/    \___/\__,_/ /_/ /_/ /_//____/ /____/ /_/ /_/
    :
    :
    : You have logged into a DreamSSH Server.
    : Type 'ls()' or 'dir()' to see the objects in the current namespace.
    :
    : Enjoy!
    :
    :>>

If you follow the hints given in the banner, you can get a listing of available
objects with the following command::

    :>> ls()
        __builtins__ - data
        app          - dreamssh.shell.pythonshell.CommandAPI.app
        banner       - dreamssh.shell.pythonshell.CommandAPI.banner
        clear        - dreamssh.shell.pythonshell.CommandAPI.clear
        config       - dreamssh.config
        exit         - dreamssh.shell.pythonshell.CommandAPI.exit
        info         - dreamssh.shell.pythonshell.CommandAPI.info
        ls           - dreamssh.shell.pythonshell.CommandAPI.ls
        os           - os
        pprint       - pprint.pprint
        quit         - dreamssh.shell.pythonshell.CommandAPI.quit
        services     - data
        sys          - sys

If you opt for the 'echo' shell::

    $ twistd dreamssh --interpreter=echo

Then executing any command will looks something like this::

    :>> execute any command
    input = execute any command, filename = <console>

The echo shell is intended to provide insight or a starting point for
developers who want to implement their own shell their users can ssh into.

Configuring
-----------

TBD


Hacking
-------

TBD
