### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ##
#
#   See COPYING file distributed along with the VICVB package for the
#   copyright and license terms.
#
### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ##


import pytest
import tempfile, os, shutil
from subprocess import check_call
from VICVB import config,util

@pytest.fixture(scope="session")
def get_test_data_dir():
    pkg_test_data = config.get_pkg_data_file("test_data")
    shutil.copytree(pkg_test_data,os.path.join(os.getcwd(),"test_data"))

@pytest.fixture(scope="session")
def goto_cleandir_test():
    root_test_dir = "test_run"
    if not os.path.exists(root_test_dir):
        os.makedirs(root_test_dir)
    newpath = tempfile.mkdtemp(prefix="run.test.",suffix=".tmp",dir=root_test_dir)
    os.chdir(newpath)

@pytest.fixture(scope="session")
def install_jbrowse_cmd():
    check_call(["vicvb_postinstall",
        "install-jbrowse",
        "--rename-to","jbrowse",
        "--conf-file","VICVB.json",
        os.getcwd(),
        "/"])

@pytest.fixture(scope="session")
def collect_vigor_inp_dirs():
    res = []
    curdir = os.getcwd()
    try:
        #I could not figure any way to generate test parameterization AFTER
        #the fixtures (those that unpack test data dir) have been executed.
        #Here I just duplicate test data unpacking to get the list of tests.
        goto_cleandir_test()
        get_test_data_dir()
        for genome_set_dir in ("Exceptions","NCBI.one_arch","NCBI.one_dir","NCBI","ASM"): #("ASM",): #("NCBI",):
            #TMP:
            #genome_set_dir = os.path.join("/home/atovtchi/work/jcvi_cloud_vir/test_data","VIGOR",genome_set_dir)
            genome_set_dir = os.path.join("test_data","VIGOR",genome_set_dir)
            for data_dir in os.listdir(genome_set_dir):
                res.append(os.path.join(genome_set_dir,data_dir))
    finally:
        os.chdir(curdir)
    return res

@pytest.fixture(scope="module",params = collect_vigor_inp_dirs())
def inp_data_dir(request):
    return request.param

