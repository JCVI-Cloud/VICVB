import pytest
from subprocess import check_call

pytestmark = pytest.mark.usefixtures("goto_cleandir",
        "get_test_data_dir",
        "install_jbrowse_cmd")

def test_set02():
    check_call("vicvb_galaxy_tool to-jbrowse VICVB.json giv3_H2EU_39497 test_data/set02/input/giv3_H2EU_39497_consensus.fasta test_data/set02/output giv3_H2EU_39497.html giv3_H2EU_39497.jbrowse".split())

#def test_set01_01():
#    check_call("vicvb_galaxy_tool to-jbrowse VICVB.json  FluB test_data/set01/input/Flu/FluB.fasta test_data/set01/output FluB.html FluB.jbrowse".split())


def test_set01_02():
    check_call("vicvb_galaxy_tool to-jbrowse VICVB.json  Rhinovirus_genomes test_data/set01/input/Rhinovirus/Rhinovirus_genomes.fasta test_data/set01/output Rhinovirus_genomes.html Rhinovirus_genomes.jbrowse".split())

