from twisted.application.service import ServiceMaker

#from dreamssh import meta
print __file__


DreamSSHService = ServiceMaker(
    "DreamSSH Server",
    "dreamssh.service",
    "A highly flexible pure-Python, Twisted-based SSH Server",
    "dreamssh")
