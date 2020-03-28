import os

def sh(command):
    return os.popen(command).read().strip('\n').strip(' ')