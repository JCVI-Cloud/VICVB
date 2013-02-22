from glob import glob
import os, shutil, zipfile, fileinput
from argh import *
from subprocess import check_call
import logging

import config
import util

log = logging.getLogger(__name__)

pjoin = os.path.join


def install_jbrowse(install_dir,root_url,conf_file=config.pkg_name+".json"):
    pkg_data_dir = config.get_pkg_data_dir()
    jbrowse_zip = glob(pjoin(pkg_data_dir,"JBrowse*"))
    assert len(jbrowse_zip) == 1, "Expected a single JBrowse archive "+\
            "stored within the package data dir: %s" % (pkg_data_dir,)
    jbrowse_zip = jbrowse_zip[0]
    util.makedir(install_dir)
    #context manager only works for zipfile in Python 2.7
    f = zipfile.ZipFile(jbrowse_zip, 'r')
    try:
        f.extractall(path=install_dir)
        install_name = os.path.dirname(f.namelist()[0])
    finally:
        f.close()
    install_home = pjoin(install_dir,install_name)
    check_call(["./setup.sh"],cwd=install_home)
    for line in fileinput.input(pjoin(install_home,"index.html"),inplace=True):
        #Galaxy Web server intercepts 'data' in URL params, we need to use another name
        print line.replace('queryParams.data','queryParams.jbrowse_data'),
    conf = config.load_config_json(conf_file)
    conf["jbrowse_bin_dir"] = util.abspath(pjoin(install_home,"bin"))
    conf["jbrowse_url"] = root_url+'/'+os.path.basename(install_home)
    config.save_config_json(conf,conf_file)
    return install_home
    
def install_tools():
    install_jbrowse(data_dir,install_dir)

def main():
    parser = ArghParser()
    parser.add_commands([install_jbrowse,install_tools])
    parser.dispatch()

