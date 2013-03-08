Venter Institute Cloud Viral Browser (VICVB)
================================

This package takes the output of VIGOR (JCVI viral annotation pipeline) and generates the input for
[JBrowse](http://jbrowse.org/) genome browser. The primary goal is to use it as a visualization tool
inside [Galaxy] (http://galaxyproject.org/) bioinformatics workbench. The package has an installer
script that installs JBrowse into Galaxy, and the dataset convertion procedure generates files
necessary for launching JBrowse from Galaxy.

Installation
------------

This package uses Python [Distribute](http://pythonhosted.org/distribute/) module. You can use any of
the build/install modes that Distribute supports (e.g. easy_install or python setup.py install).
After the package is installed, you should run vicvb_postinstall script to install JBrowse and create
corresponding config file.

For a one-stop typical installation into Galaxy, a script is provided, which can be executed like this:

    git clone git://github.com/JCVI-Cloud/VICVB.git
    cd VICVB
    lib/VICVB/data/install/install_to_dir_full.sh <PACKAGE_INSTALL_DIR> <GALAXY_HOME> <GALAXY_ROOT_URL>

Replace the references to each bracketed name above with your actual values. Typically, GALAXY_ROOT_URL
is just /.
The command above will install the package using Python's --install-dir scheme - everything will be
placed as eggs into PACKAGE_INSTALL_DIR. VICVB.rc file will be generated in PACKAGE_INSTALL_DIR.
You should source it before using the package. The JBrowse will be installed under GALAXY_HOME/static.

The script above will copy all Python dependencies into PACKAGE_INSTALL_DIR. You can edit the
install script to change that and other subtleties.

The package assumes that NCBI tbl2asn executable is available in system PATH.

Testing
-------

### Conversion to JBrowse and viewing outside of Galaxy

To test the conversion procedure, from the package source dir do:

    python setup.py test
    #replace run.test.OAtT6g.tmp below with the unique directory name that was created by the test run
    cd test_run/run.test.OAtT6g.tmp
    python -m SimpleHTTPServer 8090
    #point your Web browser to localhost:8090 and 
    #click on any of the directory names that look like *.jbrowse.
    #You should see the genome(s)

### Conversion and viewing inside Galaxy

To use this package in Galaxy, exposing it as a separate Galaxy tool is not needed. It can be just executed as part
of any other tool command line, creating an extra output dataset, which can be then viewed in JBrowse.
For testing purposes, we have provided a demonstration tool that takes a VIGOR output as a tarball (it
should also contain nucleotide FASTA input to VIGOR) and generates JBrowse input (as Galaxy compound dataset).
See bits/galaxy-tool/Readme.txt in the source tree (especially the part about switching off HTML sanitization).
After you have installed the sample Galaxy tool, upload lib/VICVB/data/test_data/VIGOR/NCBI.one_arch/Rhinovirus.tgz
into your Galaxy history and run the tool (under section VICVB) on this dataset.
The code of these sample tools can be reviewed as examples of calling the package from Galaxy.

To view the output in JBrowse, click on the Eye icon of the resulting history item. You should see a genome in the central
Galaxy panel.
