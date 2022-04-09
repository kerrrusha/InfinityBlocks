from sys import platform as PLATFORM
from os import environ
from infinityBlocks import InfinityBlocks
__version__ = "0.1"

def platform():
    if 'ANDROID_ARGUMENT' in environ:
        return "android"
    elif PLATFORM in ('linux', 'linux2','linux3'):
        return "linux"
    elif PLATFORM in ('win32', 'cygwin'):
        return 'win'

if platform() == "android":
    path = "/data/data/org.test.pgame/files/app/"
elif platform() == "linux":
    path = "./"

game = InfinityBlocks()
game.run()
