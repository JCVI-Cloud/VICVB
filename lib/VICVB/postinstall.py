from glob import glob
import os, shutil, zipfile, fileinput
from argh import *
from subprocess import check_call
import logging
import urlparse

import config
import util

log = logging.getLogger(__name__)

pjoin = os.path.join


def install_jbrowse(install_dir,
        root_url,
        rename_to=None,
        conf_file=None):
    if not conf_file:
        conf_file = config.get_default_conf_file()
    install_dir = util.abspath(install_dir)
    pkg_data_dir = config.get_pkg_data_dir()
    jbrowse_zip = glob(pjoin(pkg_data_dir,"JBrowse*"))
    assert len(jbrowse_zip) == 1, "Expected a single JBrowse archive "+\
            "stored within the package data dir: %s" % (pkg_data_dir,)
    jbrowse_zip = jbrowse_zip[0]
    util.makedir(install_dir)
    #context manager only works for zipfile in Python 2.7
    f = zipfile.ZipFile(jbrowse_zip, 'r')
    try:
        install_name = os.path.dirname(f.namelist()[0])
        install_home = pjoin(install_dir,install_name)
        #somehow zipfile module wacks executable bits
        #f.extractall(path=install_dir)
        #unsafe:
        check_call(["unzip","-q","-o",jbrowse_zip],cwd=install_dir)
    finally:
        f.close()
    if rename_to:
        install_home_new = pjoin(install_dir,rename_to)
        if os.path.exists(install_home_new):
            shutil.rmtree(install_home_new)
        os.rename(install_home,install_home_new)
        install_home = install_home_new
    check_call(["./setup.sh"],cwd=install_home)
    for line in fileinput.input(pjoin(install_home,"index.html"),inplace=True):
        #Galaxy Web server intercepts 'data' in URL params, we need to use another name
        print line.replace('queryParams.data','queryParams.jbrowse_data'),
    conf = util.load_config_json(conf_file)
    conf["jbrowse_bin_dir"] = util.abspath(pjoin(install_home,"bin"))
    conf["jbrowse_url"] = util.urljoin_path(root_url,
            os.path.basename(install_home))
    util.save_config_json(conf,conf_file)
    return conf_file
    
def install_to_galaxy(galaxy_home,galaxy_root_url="/",conf_file=None):
    galaxy_home = util.abspath(galaxy_home)
    jb_rel_dir = pjoin("static","vicvb")
    jb_install_dir = pjoin(galaxy_home,jb_rel_dir)
    jb_root_url = util.urljoin_path(galaxy_root_url,jb_rel_dir)
    #tool_install_dir = pjoin(galaxy_home,"tools","vicvb")
    #util.makedir(tool_install_dir)
    conf_file = install_jbrowse(jb_install_dir,
            jb_root_url,
            #rename_to="jbrowse",
            conf_file=conf_file)
    #shutil.copy(config.get_pkg_data_file("galaxy_vicvb_browser.xml"),
    #        pjoin(tool_install_dir,"vicvb_browser.xml"))
    return conf_file

def main():
    parser = ArghParser()
    parser.add_commands([install_jbrowse,install_to_galaxy])
    parser.dispatch()

