from twisted.application.service import ServiceMaker


DreamSSHService = ServiceMaker(
    "DreamSSH Server",
    "dreamssh.server.service",
    ("A highly flexible pure-Python, Twisted-based SSH Server with custom "
     "account shells"),
    "dreamssh")
