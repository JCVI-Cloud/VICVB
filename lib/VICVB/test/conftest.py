import pytest
import tempfile, os, shutil
from subprocess import check_call
from VICVB import config,util

@pytest.fixture(scope="session")
def get_test_data_dir(request):
    pkg_test_data = config.get_pkg_data_file("test_data")
    shutil.copytree(pkg_test_data,os.path.join(os.getcwd(),"test_data"))

@pytest.fixture(scope="session")
def goto_cleandir_test(request):
    root_test_dir = "test_run"
    if not os.path.exists(root_test_dir):
        os.makedirs(root_test_dir)
    newpath = tempfile.mkdtemp(prefix="run.test.",suffix=".tmp",dir=root_test_dir)
    os.chdir(newpath)

@pytest.fixture(scope="session")
def install_jbrowse_cmd(request):
    check_call(["vicvb_postinstall",
        "install-jbrowse",
        "--rename-to","jbrowse",
        os.getcwd(),
        "/"])
