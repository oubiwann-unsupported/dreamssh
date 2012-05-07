# Copyright (c) Twisted Matrix Laboratories.
# See LICENSE for details.

from twisted.application.service import ServiceMaker

MOTDManhole = ServiceMaker(
    "Twisted MOTD Manhole (new)",
    "twisted.conch.manhole_tap",
    ("An interactive remote debugger service accessible via telnet "
     "and ssh and providing syntax coloring and basic line editing "
     "functionality."),
    "motd_manhole")
