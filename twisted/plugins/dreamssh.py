from twisted.application.service import ServiceMaker

#from dreamssh import service


DreamSSHService = ServiceMaker(
    "DreamSSH Server",
    "dreamssh.service",
    ("A highly flexible pure-Python, Twisted-based SSH Server with custom "
     "account shells"),
    "dreamssh")
