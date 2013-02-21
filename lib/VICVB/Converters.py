from subprocess import check_call
import logging

log = logging.getLogger(__name__)

class galaxy_jbrowse(object):


    def __init__(self,
            jbrowse_url,
            jbrowse_bin_dir,
            jbrowse_galaxy_index_html_tpl,
            tbl_to_asn_tpl,
            tbl_to_asn_exe):
        #the line below should be the first in
        #order to get all parameters into a dict
        self.opt = locals.copy()
        self.opt.pop("self")

    def gff_to_jbrowse(self,
            fasta_file,
            gff_file,
            index_html,
            data_dir_out,
            jbrowse_url=None,
            track_label=None
            ):
        if jbrowse_url is None:
            jbrowse_url = self.opt["jbrowse_url"]
        if track_label is None:
            track_label = os.path.splitext(os.path.basename(gff_file))[0]
        with open(index_html,"w") as f:
            f.write(_jbrowse_dataset_index_html.\
                format(jbrowse_url=jbrowse_url.rstrip("/")))

        env = None
        if self.opt.get("jbrowse_bin_dir",None):
            env = os.environ.copy()
            env["PATH"] = ":".join(self.opt["jbrowse_bin_dir"],env.get("PATH",""))

        check_call(["prepare-refseqs.pl","--fasta",fasta_file],
                cwd=data_dir_out,
                env=env)
        check_call(["flatfile-to-json.pl","--gff",gff_file,
            "--trackLabel",track_label],
            cwd=data_dir_out,
            env=env)

    def genbank_to_gff(self,
            genbank_file):
        check_call(["genbank_to_gff.py",genbank_file])
        dict(gff_file=os.path.join(stripSfx(genbank_file)+".gff"))

    def vicvb_to_genbank(self,
            genome_name,
            annot_inp_fasta,
            annot_out_dir,
            tbl_conv_dir=None,
            tbl_to_asn_tpl=None
            ):
        if tbl_conv_dir is None:
            tbl_conv_dir = os.getcwd()
        else:
            os.makedirs(tbl_conv_dir)
        annot_out_root = os.path.join(annot_out_dir,genome_name)
        shutil.copy(
                annot_inp_fasta,
                os.path.join(
                    tbl_conv_dir,
                    genome_name+".fsa"
                    )
                )
        for ext in (".tbl",".pep"):
            shutil.copy(
                    annot_out_root+ext,
                    tbl_conv_dir
                    )

        if tbl_to_asn_tpl is None:
            tbl_to_asn_tpl = self.opt["tbl_to_asn_tpl"]

        if "tbl_to_asn_exe" in self.opt:
            tbl_to_asn_exe = self.opt["tbl_to_asn_exe"]
        else:
            tbl_to_asn_exe = "tbl2asn"
        
        check_call([tbl_to_asn_exe,
            "-p",tbl_conv_dir,
            "-t",tbl_to_asn_tpl,
            "-a","s",
            "-V","bv",
            "-n",genome_name])
        
        return dict(
                genbank_file=os.path.join(tbl_conv_dir,genome_name+".gbf"),
                )

    def vicvb_to_jbrowse(self,
            genome_name,
            annot_inp_fasta,
            annot_out_dir,
            index_html,
            data_dir_out
            ):
            
            res_gb = vicvb_to_genbank(
                genome_name=genome_name,
                annot_inp_fasta=annot_inp_fasta,
                annot_out_dir=annot_out_dir
                )
            
            res_gff = genbank_to_gff(genbank_file=res_gb["genbank_file"])

            gff_to_jbrowse(
                fasta_file=annot_inp_fasta,
                gff_file=res_gff["gff_file"],
                index_html=index_html,
                data_dir_out=data_dir_out
                )
        

def getProgOptions():
    from optparse import OptionParser, make_option
    option_list = [
        make_option(None, "--config-file",
        action="store", 
        type="string",
        help="Config file",
        dest="config_file"),
        make_option(None, "--genome-name",
        action="store", 
        type="string",
        help="Genome name",
        dest="genome_name"),
        make_option(None, "--annot-inp-fasta",
        action="store", 
        type="string",
        help="",
        dest="annot_inp_fasta"),
    ]
    parser = OptionParser(usage = "usage: %prog [options]",option_list=option_list)
    (options, args) = parser.parse_args()

    return options,args

def main():
    opt,args = getProgOptions()
    assert opt.config_file is not None,"--config is mandatory argument"
    config = ConfigParser.SafeConfigParser()
    config.read(opt.config_file)
    kw = dict(config.items("vicvb"))
    galaxy_jbrowse(**kw).vicvb_to_jbrowse(**opt)

