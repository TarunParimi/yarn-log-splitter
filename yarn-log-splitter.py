import sys
from os import path, makedirs, symlink, chdir, mkdir
from shutil import rmtree

CONTAINER_PREFIX = 'Container: '
LOGTYPE_PREFIX = 'LogType:'
LOGTYPE_SEPARATOR = ':'
LOGTYPE_END = 'End of LogType:'
def remove_and_create(dir):
    try:
        mkdir(dir)
    except OSError:
        rmtree(dir)
        mkdir(dir)
        
def split_logs(log, outputdir):
    outputdir = path.abspath(outputdir)
    try:
        makedirs(outputdir)
    except OSError:
        pass

    containers_base = path.join(outputdir, 'containers')
    hosts_base = path.join(outputdir, 'hosts')
    remove_and_create(containers_base)
    remove_and_create(hosts_base)
    
    containers = set()
    hosts = set()
    container = None
    split_file = None
    container_dir = None
    logtype = None
    container_header = None
    with open(log) as log_file:
        for line in log_file:
            if line.startswith(CONTAINER_PREFIX):
                container_header = line
                container = line.split()[1].strip()
                if container not in containers:
                    containers.add(container)
                    container_dir = path.join(containers_base, container)
                    mkdir(container_dir)
                    host = line.split()[3].strip()
                    hostdir = path.join(hosts_base, host)
                    if host not in hosts:
                        hosts.add(host)
                        mkdir(hostdir)
                    symlink(container_dir, path.join(hostdir,container))
                    
            elif line.startswith(LOGTYPE_PREFIX):
                logtype = line.split(LOGTYPE_SEPARATOR)[1].strip()
                split_file = open(path.join(container_dir, logtype), 'w+')
                split_file.write(container_header)
            
            elif line.startswith(LOGTYPE_END):
                if line.split(LOGTYPE_SEPARATOR)[1].strip() == logtype:
                    if split_file is not None:
                        split_file.close()
                    split_file = None
                else:
                    pass #Ignore empty log type

            if split_file is not None:
                split_file.write(line)

    if split_file is not None:
        split_file.close()


def usage():
    print ('Usage: python ' + sys.argv[0] + ' <application log> <output dir>')

if __name__ == '__main__':
    if len(sys.argv) != 3:
        usage()
    else:
        split_logs(sys.argv[1], sys.argv[2])

