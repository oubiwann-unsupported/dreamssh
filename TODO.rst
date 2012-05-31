TODO
====


Bugs
----

* When executing the "clear" shell command, the new screen has a newline at the
  top

* Received unhandled keyID: '\x01' (^a) doesn't return cursor to the beginning
  of the line

* Received unhandled keyID: '\x05' (^e) doesn't send the cursor to the end of
  the line


Tasks
-----

* Add a twistd dreamssh subcommand for generating the config

* Add support for things like:
  * who - all logged in users
  * whois - info about a user
  * sending messages to all logged in users

* Add support for tab-completion

* Create an admin role
 * only those in the admin role have permission to see and use sys and os
   modules
 * only allow admins to see the various sensitive functions (e.g., sending
   messages to all users)

* Add generic support for roles
  * provide a mechanism whereby admins can create roles, and
  * assign different APIs or limited APIs to roles
  * support role persistence
    * when a role is created, it needs to be stored somewhere
      so that it's available when the server restarts
    * make MongoDB and txMongo dependencies

* Add support for storing additional keys in MongoDB
  * this will allow users the ability to update their keys and not have to
    write to the filesystem

* Add support for dynamic prompts

* Add support for a status bar on the screen somewhere

* Add phased login
  * a login to create an account
  * provide a user name
  * provide a URL for SSH keys
  * keep a global cache of ssh keys and don't allow new user-creation if ssh
    keys are already present
  * allow for this code to be extendable
  * if anonymous, do phase 1 login
  * if not anonymous, do a full login
  * provide for the ability to define what the anonymous user name is
    * make the default anonymous user "signup"
