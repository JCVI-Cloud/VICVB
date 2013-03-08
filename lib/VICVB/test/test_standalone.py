### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ##
#
#   See COPYING file distributed along with the VICVB package for the
#   copyright and license terms.
#
### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ##


import pytest
from subprocess import check_call
import os, glob
from os.path import join as pjoin


pytestmark = pytest.mark.usefixtures("goto_cleandir_test",
        "get_test_data_dir",
        "install_jbrowse_cmd")

#def test_set02():
#    check_call("vicvb_galaxy_tool to-jbrowse VICVB.json giv3_H2EU_39497 test_data/set02/input/giv3_H2EU_39497_consensus.fasta test_data/set02/output giv3_H2EU_39497.html giv3_H2EU_39497.jbrowse".split())

#def test_set01_01():
#    check_call("vicvb_galaxy_tool to-jbrowse VICVB.json  FluB test_data/set01/input/Flu/FluB.fasta test_data/set01/output FluB.html FluB.jbrowse".split())


#def test_set01_02():
#    check_call("vicvb_galaxy_tool to-jbrowse VICVB.json  Rhinovirus_genomes test_data/set01/input/Rhinovirus/Rhinovirus_genomes.fasta test_data/set01/output Rhinovirus_genomes.html Rhinovirus_genomes.jbrowse".split())

def test_vigor(inp_data_dir):
    input_dir = pjoin(inp_data_dir,"input")
    if os.path.isdir(input_dir):
        fasta = os.listdir(input_dir)
        assert len(fasta) == 1, "One FASTA file is expected in %s" % (input_dir,)
        fasta = pjoin(input_dir,fasta[0])
        genome_name = os.path.splitext(os.path.basename(fasta))[0]
        out_base = genome_name
        vigor_out = pjoin(inp_data_dir,"output")
    else:
        fasta = None
        vigor_out = inp_data_dir
        out_base = os.path.basename(os.path.dirname(inp_data_dir))+\
                "_"+\
                os.path.splitext(os.path.basename(inp_data_dir))[0]
        genome_name = None
        
    jbrowse_out = out_base + ".jbrowse"
    html_index = pjoin(jbrowse_out,"index.html")
    #TMP:
    #print ("vicvb_galaxy_tool to-jbrowse VICVB.json {genome_name} "+\
    #                    "{fasta} {vigor_out} {html_index} {jbrowse_out}").format(**locals())
    check_call(("vicvb_galaxy_tool to-jbrowse --conf-file VICVB.json {genome_name} "+\
            "{fasta} {vigor_out} {html_index} {jbrowse_out}").format(**locals()).split())



