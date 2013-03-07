import VICVB.converters
import os, sys

inp_vigor_tgz = sys.argv[1]
out_vcb_jbrowse = sys.argv[2]
out_vcb_jbrowse_data = sys.argv[3]

conf = os.environ["VICVB_CONF"]
VICVB.converters.to_jbrowse(conf=conf,
            genome_name=None,
            annot_inp_fasta=None,
            annot_out=inp_vigor_tgz,
            index_html=out_vcb_jbrowse,
            data_dir_out=out_vcb_jbrowse_data)

