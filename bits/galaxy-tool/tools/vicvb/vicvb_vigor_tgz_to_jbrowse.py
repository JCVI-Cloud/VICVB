import VICVB.converters
import os, sys

inp_vigor_tgz = sys.argv[1]
out_vcb_jbrowse = sys.argv[2]
out_vcb_jbrowse_data = sys.argv[3]

#This line is just to demonstrate
#explicit passing of config file.
#to_jbrowse() will search for VICVB_CONF
#env var itself if conf_file is not provided.
conf_file = os.environ["VICVB_CONF"]

#Here we use the input variant where FASTA
#of the viral genome is packed in the annotation
#tarball. See unit tests of the package for other
#variants (separate FASTA, directory instead of tarball)
VICVB.converters.to_jbrowse(
            genome_name=None,
            annot_inp_fasta=None,
            annot_out=inp_vigor_tgz,
            index_html=out_vcb_jbrowse,
            data_dir_out=out_vcb_jbrowse_data,
            conf_file=conf_file)

