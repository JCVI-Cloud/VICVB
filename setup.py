#activate 'distribute', installing it if necessary
from distribute_setup import use_setuptools
use_setuptools()

from setuptools import setup, find_packages
import os

vendor_src = "vendor"
bcbb_src = os.path.join(vendor_src,"bcbb")

main_pkg_name = "VICVB"
script_pref = "vicvb_"

def _entry_point(script_name,pkg_path):
    return script_pref+script_name+' = '+main_pkg_name+'.'+pkg_path

setup(
    name = main_pkg_name,
    version = "0.2",
    packages = find_packages("lib"),
    package_dir = {'':'lib'},
    #scripts = ['say_hello.py'],
    #argh is used to auto-generate command line argument 
    #processing in entry points
    install_requires = ['argh','argcomplete','biopython','bcbio_gff'],
    #http://pythonhosted.org/distribute/easy_install.html#editing-and-viewing-source-packages
    #from pkg_resources import load_entry_point
    #load_entry_point('distribute==0.6.35', 'console_scripts', 'easy_install')(argv=sys.argv[1:])
	#full URL could be vcs+proto://host/path@revision#egg=project-version
	#dependency_links=["git+git://github.com/chapmanb/bcbb.git#egg=bcbb"],
    dependency_links=["file:"+os.path.join(bcbb_src,"gff")+"#egg=bcbio_gff"],
    package_data = {
        main_pkg_name: ["data/*"],
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
    url = "http://github.com/JCVI-Cloud", 
)
