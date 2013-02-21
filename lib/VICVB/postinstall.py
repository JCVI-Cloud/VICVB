from pkg_resources import Requirement, resource_filename
from glob import glob
import os, shutil, zipfile
from argh import *

pjoin = os.path.join

def install_jbrowse(data_dir,install_dir):
    jbrowse_zip = glob(pjoin(data_dir,"JBrowse*"))
    assert len(jbrowse_zip) == 1, "Expected a single JBrowse archive "+\
            "stored within the package data dir: %s" % (data_dir,)
    jbrowse_zip = jbrowse_zip[0]
    #context manager only works for zipfile in Python 2.7
    with zipfile.ZipFile(jbrowse_zip, 'r') as f:
        f.extractall(path=install_dir)
    
def install_tools():
    pkg_name = "VICVB"
    data_dir = resource_filename(Requirement.parse(pkg_name),"data")
    install_jbrowse(data_dir,install_dir)

def main():
    parser = ArghParser()
    parser.add_commands([install_jbrowse,install_tools])
    parser.dispatch()

