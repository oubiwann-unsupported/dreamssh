from twisted.application.service import ServiceMaker


CustomInterpreter = ServiceMaker(
    "Twisted Manhole with custom interpreter",
    "mypkg.interp",
    ("An interactive remote debugger service accessible via telnet "
     "and ssh and providing syntax coloring and basic line editing "
     "functionality."),
    "interp")
