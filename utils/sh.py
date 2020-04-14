def path(path):
    # return path.replace(' ', '\\ ')
    return '\'' + path + '\''

def sh(cmd):
    import subprocess
    
    print(cmd)

    return subprocess.getoutput(cmd)

def pwd():
    return sh('pwd')

def mkdir(p):
    return sh('mkdir ' + path(p))

def rmrf(p):
    return sh('rm -rf ' + path(p))

def cp(from_path, to_path):
    return sh('cp ' + path(from_path) + ' ' + path(to_path))