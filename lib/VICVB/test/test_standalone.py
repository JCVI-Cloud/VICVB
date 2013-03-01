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

def run_vigor(data_dir):
    input_dir = pjoin(data_dir,"input")
    fasta = os.listdir(input_dir)
    assert len(fasta) == 1, "One FASTA file is expected in %s" % (input_dir,)
    fasta = pjoin(input_dir,fasta[0])
    genome_name = os.path.splitext(os.path.basename(fasta))[0]
    vigor_out = pjoin(data_dir,"output")
    jbrowse_out = genome_name + ".jbrowse"
    html_index = pjoin(jbrowse_out,"index.html")
    #TMP:
    #print ("vicvb_galaxy_tool to-jbrowse VICVB.json {genome_name} "+\
    #                    "{fasta} {vigor_out} {html_index} {jbrowse_out}").format(**locals())
    check_call(("vicvb_galaxy_tool to-jbrowse VICVB.json {genome_name} "+\
            "{fasta} {vigor_out} {html_index} {jbrowse_out}").format(**locals()).split())

def test_vigor():
    for genome_set_dir in ("NCBI","ASM"): #("ASM",): #("NCBI",):
        #TMP:
        #genome_set_dir = pjoin("/home/atovtchi/work/jcvi_cloud_vir/test_data","VIGOR",genome_set_dir)
        genome_set_dir = pjoin("test_data","VIGOR",genome_set_dir)
        for data_dir in os.listdir(genome_set_dir):
            run_vigor(pjoin(genome_set_dir,data_dir))


