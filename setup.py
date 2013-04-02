### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ##
#
#   See COPYING file distributed along with the VICVB package for the
#   copyright and license terms.
#
### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ##
main_pkg_name = "VICVB"
script_pref = "vicvb_"

#activate 'distribute', installing it if necessary
from distribute_setup import use_setuptools
use_setuptools()

from setuptools import setup, find_packages
from setuptools.command.test import test as TestCommand
import os,sys,tempfile
from fnmatch import fnmatch



def _entry_point(script_name,pkg_path):
    return script_pref+script_name+' = '+main_pkg_name+'.'+pkg_path

class PyTest(TestCommand):
    """Integrates pytest as per http://pytest.org/latest/goodpractises.html?highlight=egg
    so that you can run 'python setup.py test'"""
    def finalize_options(self):
        TestCommand.finalize_options(self)
        test_dir = os.path.join("lib",main_pkg_name,"test")
        self.test_args = ["--verbose",test_dir]
        self.test_suite = test_dir
        #print self.test_args
        #print self.test_suite
    def run_tests(self):
        #import here, cause outside the eggs aren't loaded
        import pytest
        errno = pytest.main(self.test_args)
        sys.exit(errno)

def iter_files_tree(dir,to_base=True,patt=None):
    dir_base = os.path.dirname(dir)
    if patt is not None:
        if isinstance(patt,str):
            patt = [ patt ]
    for root,dirs,files in os.walk(dir):
        for f in files:
            if patt:
                match = False
                for p in patt:
                    if fnmatch(f,p):
                        match = True
                        break
                if not match:
                    continue
            path = os.path.join(root,f)
            if to_base:
                path = os.path.relpath(path,dir_base)
            yield path

def _list_pkg_files(dir,patt=None):
    return list(iter_files_tree(os.path.join("lib",main_pkg_name,dir),patt=patt))

#Simply running "python setup.py test" will not work because the test fixture
#uses entry point script to install JBrowse (this is by itself a usefull test).
#setup.py test command does not create entry point scripts.
#Thus, we detect when a command line looks like "* setup.py test" and modify
#it to look like "* setup.py develop --install-dir <tmp_dir> test", also
#adding <tmp_dir> to PATH and PYTHONPATH.
if len(sys.argv) >= 2 and sys.argv[-1] == "test" and sys.argv[-2] == "setup.py":
    pos_test = -1
    test_inst_dir = os.path.abspath(os.path.join("test_run","install"))
    if not os.path.exists(test_inst_dir):
        os.makedirs(test_inst_dir)
    test_inst_dir = tempfile.mkdtemp(prefix="install.test.",suffix=".tmp",dir=test_inst_dir)
    sys.path.insert(0,test_inst_dir)
    PATH = os.environ.get("PATH",test_inst_dir)
    os.environ["PATH"] = os.pathsep.join([test_inst_dir,PATH])
    PYTHONPATH = os.environ.get("PYTHONPATH",test_inst_dir)
    os.environ["PYTHONPATH"] = os.pathsep.join([test_inst_dir,PYTHONPATH])
    sys.argv = sys.argv[:pos_test]+["develop","--install-dir",test_inst_dir]+sys.argv[pos_test:]

setup(
    name = main_pkg_name,
    version = "0.2",
    packages = find_packages("lib"),
    package_dir = {'':'lib'},
    #argh is used to auto-generate command line argument 
    #processing in entry points
    install_requires = ['argh','argcomplete','biopython'],
	#this will install pytest module
    tests_require=['pytest'],
    cmdclass = {'test': PyTest},
    #http://pythonhosted.org/distribute/easy_install.html#editing-and-viewing-source-packages
    #from pkg_resources import load_entry_point
    #load_entry_point('distribute==0.6.35', 'console_scripts', 'easy_install')(argv=sys.argv[1:])
	#full URL could be vcs+proto://host/path@revision#egg=project-version
	#dependency_links=["git+git://github.com/chapmanb/bcbb.git#egg=bcbb"],
    #dependency_links=["file:"+os.path.join(bcbb_src,"gff")+"#egg=bcbio_gff"],
    package_data = {
        main_pkg_name: _list_pkg_files("data") + \
                _list_pkg_files("test",patt="*.py") + \
                _list_pkg_files("BCBio",("*.txt","*.py")),
    },
    entry_points = {
        #'console_scripts' is a fixed group name - it will cause
        #creation of scripts
        'console_scripts': [
            _entry_point('postinstall','postinstall:main'),
            _entry_point('galaxy_tool','converters:main'),
            ]
        },
    # metadata for upload to PyPI
    author = "Andrey Tovchigrechko",
    author_email = "andreyto@gmail.com",
    description = "Package to integrate JBrowse into Galaxy instance of JCVI viral annotation pipeline",
    license = "GPL",
    keywords = "Galaxy JCVI viral annotation JBrowse",
    url = "http://github.com/JCVI-Cloud/VICVB", 
)
