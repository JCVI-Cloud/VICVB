from pkg_resources import Requirement, resource_filename
from glob import glob
import os, shutil, zipfile
from argh import *
from subprocess import check_call
import logging

log = logging.getLogger(__name__)

pjoin = os.path.join

pkg_name = "VICVB"
pkg_data_dir = resource_filename(Requirement.parse(pkg_name),"VICVB/data")

def install_jbrowse(install_dir):
    jbrowse_zip = glob(pjoin(pkg_data_dir,"JBrowse*"))
    assert len(jbrowse_zip) == 1, "Expected a single JBrowse archive "+\
            "stored within the package data dir: %s" % (pkg_data_dir,)
    jbrowse_zip = jbrowse_zip[0]
    #context manager only works for zipfile in Python 2.7
    f = zipfile.ZipFile(jbrowse_zip, 'r')
    try:
        f.extractall(path=install_dir)
        install_name = os.path.dirname(f.namelist()[0])
    finally:
        f.close()
    install_home = pjoin(install_dir,install_name)
    check_call(["./setup.sh"],cwd=install_home)
    return install_home
    
def install_tools():
    install_jbrowse(data_dir,install_dir)

def main():
    parser = ArghParser()
    parser.add_commands([install_jbrowse,install_tools])
    parser.dispatch()

