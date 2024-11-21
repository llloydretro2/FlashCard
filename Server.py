import os
import sys


def restart_server_local():
    print("Restarting server locally...")
    os.execv(sys.executable, ['python'] + sys.argv)
    return


def restart_server_public():
    print("Restarting server publicly")
    os.execv(sys.executable, ['python'] + sys.argv + ['--share'])
    return
