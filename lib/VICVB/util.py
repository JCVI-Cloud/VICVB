import os, tarfile

def abspath(path):
    if not os.path.isabs(path):
        path = os.path.abspath(path)
    return path

def makedir(path):
    if not os.path.isdir(path):
        os.makedirs(path)


def urljoin_path(base,url):
    import urlparse
    #urlparse.urljoin is weird: 
    #In [6]: urljoin(urljoin("/","static/vicvb"),"jbrowse")
    #Out[6]: '/static/jbrowse'
    if not base.endswith(":"):
        if not base.endswith("/"):
            base += "/"
    return urlparse.urljoin(base,url)

def add_to_path(dir,var="PATH",prepend=False,env=None):
    """Add a directory to the PATH environment variable"""
    dir = str(dir)
    if env is None:
        env = os.environ
    if var in env:
        if prepend:
            first = dir
            second = env[var]
        else:
            first = env[var]
            second = dir
        env[var] = os.pathsep.join((first,second))
    else:
        env[var] = dir

def tar_check_safety(tar):
    
    def _tar_info_str(tarinfo):
        return " ; ".join([ "%s : %s" % item for \
                item in sorted(tarinfo.__dict__.items()) \
                if not item[0].startswith('_') \
                and not item[0] == "buf" ])
    
    def _err_msg(tarinfo,msg):
        return "Archive failed safety check - "+\
                    msg+": %s" % (_tar_info_str(tarinfo),)

    for tarinfo in tar:
        if os.path.isabs(tarinfo.name) or \
                os.path.isabs(os.path.normpath(tarinfo.name)):
            raise ValueError(_err_msg(tarinfo,
            "Absolute file name detected"))
        elif ".." in tarinfo.name or ".." \
                in os.path.normpath(tarinfo.name):
            raise ValueError(_err_msg(tarinfo,
                    "Upper directory reference is detected"))
        elif not (tarinfo.isreg() or tarinfo.isdir()):
            #e.g. if archive was artificially manipulated to contain 
            #first A/B where B is a symlink to ../../something,
            #and then A/B/C, then C might be created as ../../something/C 
            #(my guess).
            raise ValueError(_err_msg(tarinfo,
                    "Non-regular files or dirs can lead to exploits"))

def tar_extractall_safe(archive,path=None):
    if path is None:
        path = os.getcwd()
    tar = tarfile.open(archive, "r") #will auto-detect compression
    try:
        tar_check_safety(tar)
        tar.extractall(path=path)
    finally:
        tar.close()


def tar_extractall_safe_single_dir(archive,path=None):
    tar_extractall_safe(archive=archive,path=path)
    subdirs = list(os.listdir(path))
    assert len(subdirs) == 1,\
            "Expected a single directory in archive %s" \
            % (path,)
    return os.path.join(path,subdirs[0])

