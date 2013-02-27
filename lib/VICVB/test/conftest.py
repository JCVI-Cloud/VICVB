import pytest
import tempfile, os, shutil
from subprocess import check_call
from VICVB import config,util

@pytest.fixture(scope="session")
def get_test_data_dir(request):
    pkg_test_data_arch = config.get_pkg_data_file("test_data.tgz")
    assert os.path.basename(util.tar_extractall_safe_single_dir(
            pkg_test_data_arch,
            os.getcwd()
            )) == "test_data",\
                    "Archive should contain a directory 'test_data'"

@pytest.fixture(scope="session")
def goto_cleandir(request):
    newpath = tempfile.mkdtemp(prefix="run.test.",suffix=".tmp",dir=os.getcwd())
    os.chdir(newpath)

@pytest.fixture(scope="session")
def install_jbrowse_cmd(request):
    check_call(["vicvb_postinstall",
        "install-jbrowse",
        "--rename-to","jbrowse",
        os.getcwd(),
        "/"])