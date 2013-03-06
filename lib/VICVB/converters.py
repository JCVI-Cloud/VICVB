from subprocess import check_call
import logging
import config
import util
import os, glob, shutil, tempfile

log = logging.getLogger(__name__)

class galaxy_jbrowse(object):


    def __init__(self,
            jbrowse_url,
            jbrowse_bin_dir,
            jbrowse_galaxy_index_html_tpl=None,
            jbrowse_data_subdir="data",
            tbl_to_asn_tpl=None,
            tbl_to_asn_exe=None):
        #the line below should be the first in
        #order to get all parameters into a dict
        self.opt = locals().copy()
        self.opt.pop("self")
        self.opt["jbrowse_bin_dir"] = util.abspath(self.opt["jbrowse_bin_dir"])
        print self.opt

    def gff_to_jbrowse(self,
            gff_file,
            index_html,
            data_dir_out,
            jbrowse_url=None
            ):
        opt = self.opt
        if jbrowse_url is None:
            jbrowse_url = opt["jbrowse_url"]
        env = None
        if self.opt.get("jbrowse_bin_dir",None):
            env = os.environ.copy()
            util.add_to_path(opt["jbrowse_bin_dir"],
                    prepend=True,
                    env=env)
        if not os.path.exists(data_dir_out):
            os.makedirs(data_dir_out)
        gff_file = util.abspath(gff_file)
        #fasta_file = util.abspath(fasta_file)
        jbrowse_out_dir = os.path.join(data_dir_out,opt["jbrowse_data_subdir"])
        check_call(["prepare-refseqs.pl","--gff",gff_file,"--out",jbrowse_out_dir],
                env=env)
        #@todo use biodb-to-json instead with flat file input, and accept config
        #file as a parameter (provide a default one too). See volvox.json config
        #in the distribution. Also add dropped_features param to load everything
        #unique in field 3 of GFF and check that only dropped_features are missing
        #from the config
        check_call(["flatfile-to-json.pl","--gff",gff_file,"--out",jbrowse_out_dir,
            "--trackLabel","Genes",
            "--cssClass","feature5",
            "--type","gene",
            "--autocomplete","all"
            "--getLabel",
            "--getType"
            ],
            env=env)
        check_call(["flatfile-to-json.pl","--gff",gff_file,"--out",jbrowse_out_dir,
            "--trackLabel","CDS",
            "--cssClass","cds",
            "--type","CDS",
            "--type","mat_peptide",
            "--autocomplete","all"
            "--getLabel",
            "--getType",
            "--getSubs",
            "--getPhase"
            ],
            env=env)
        check_call(["generate-names.pl","--out",jbrowse_out_dir],
            env=env)

        tracks_conf_file = os.path.join(jbrowse_out_dir,"trackList.json")
        tracks_conf = util.load_config_json(tracks_conf_file)
        tracks_conf["refSeqDropdown"] = True #show pull-down even for very many sequences
        util.save_config_json(tracks_conf,tracks_conf_file)
        #create index.html that redirects to JBrowse index.html with correct data param etc
        _jbrowse_dataset_index_html = \
                config.get_data_string(self.opt["jbrowse_galaxy_index_html_tpl"],
                    "galaxy.index.html")
        jbrowse_url_params = util.to_url_params(dict(
            tracks=",".join(("DNA","Genes","CDS")),
            tracklist=0
            ))
        with open(index_html,"w") as f:
            f.write(_jbrowse_dataset_index_html.\
                format(jbrowse_url=jbrowse_url.rstrip("/"),
                    jbrowse_data_subdir=opt["jbrowse_data_subdir"],
                    jbrowse_url_params=jbrowse_url_params))


    def genbank_to_gff(self,
            genbank_file):
        from Bio import SeqIO
        from BCBio import GFF
        gff_file = "%s.gff" % (os.path.splitext(genbank_file)[0],)
        with open(gff_file, "w") as out_handle:
            GFF.write(SeqIO.parse(genbank_file, "genbank"), out_handle, include_fasta=True)
        return dict(gff_file=gff_file)

    def vicvb_to_genbank(self,
            genome_name,
            annot_out,
            annot_inp_fasta=None,
            tbl_conv_dir=None,
            tbl_to_asn_tpl=None
            ):
        if tbl_conv_dir is None:
            tbl_conv_dir = tempfile.mkdtemp(prefix="tbl_conv.",
                    suffix=".tmp",
                    dir=os.getcwd())
        else:
            os.makedirs(tbl_conv_dir)
        if os.path.isdir(annot_out):
            annot_out_dir = annot_out
        else:
            #if not a dir, annot_out is presumed to be tarball [compressed]
            #of a single directory (not a tar-bomb)
            annot_out_dir = os.path.join(tbl_conv_dir,"annot_out")
            os.makedirs(annot_out_dir)
            annot_out_dir = util.tar_extractall_safe_single_dir(
                    annot_out,annot_out_dir)

        if not genome_name:
            #try to figure it out
            tbl_files = glob.glob(os.path.join(annot_out_dir,"*.tbl"))
            assert len(tbl_files) == 1, "Expected in single .tbl file, found %s" % (tbl_files,)
            genome_name = os.path.splitext(os.path.basename(tbl_files[0]))[0]
        annot_out_root = os.path.join(annot_out_dir,genome_name)
        # If fasta is provided, copy that, otherwise it should be
        # already inside annotation dir
        if annot_inp_fasta:
            shutil.copy(
                    annot_inp_fasta,
                    os.path.join(
                    tbl_conv_dir,
                    genome_name+".fsa"
                    )
                )
            fsa_ext = []
        else:
            fsa_ext = [".fsa"]

        for ext in [".tbl",".pep"] + fsa_ext:
            shutil.copy(
                    annot_out_root+ext,
                    tbl_conv_dir
                    )

        if tbl_to_asn_tpl is None:
            tbl_to_asn_tpl = config.get_data_file(self.opt["tbl_to_asn_tpl"],
                    "sequin.tpl")

        if self.opt.get("tbl_to_asn_exe",None):
            tbl_to_asn_exe = self.opt["tbl_to_asn_exe"]
        else:
            tbl_to_asn_exe = "tbl2asn"
        
        #tbl2ans prints warning and progress into stderr spooking Galaxy.
        #Redirect stderr to a file.
        with open(os.path.join(
            tbl_conv_dir,"tbl2asn.%s.stderr" % (genome_name,)),
            "w") as stderr:
            check_call([tbl_to_asn_exe,
                "-p",tbl_conv_dir,
                #"-t",tbl_to_asn_tpl,
                "-a","s",
                "-V","bv",
                "-n",genome_name],
                stderr=stderr)
        
        return dict(
                genbank_file=os.path.join(tbl_conv_dir,genome_name+".gbf"),
                genome_name=genome_name
                )

    def vicvb_to_jbrowse(self,
            genome_name,
            annot_inp_fasta,
            annot_out,
            index_html,
            data_dir_out
            ):
            annot_out = util.abspath(annot_out)
            index_html = util.abspath(index_html)
            data_dir_out = util.abspath(data_dir_out)
            if annot_inp_fasta:
                annot_inp_fasta = util.abspath(annot_inp_fasta)
            res_gb = self.vicvb_to_genbank(
                genome_name=genome_name,
                annot_out=annot_out,
                annot_inp_fasta=annot_inp_fasta
                )
            
            res_gff = self.genbank_to_gff(genbank_file=res_gb["genbank_file"])

            self.gff_to_jbrowse(
                gff_file=res_gff["gff_file"],
                index_html=index_html,
                data_dir_out=data_dir_out
                )
        

def to_jbrowse(conf,
        genome_name,
        annot_inp_fasta,
        annot_out,
        index_html,
        data_dir_out):
    args = locals()
    args.pop("conf")
    opt = util.load_config_json(conf)
    args["annot_inp_fasta"] = util.none_from_str(args["annot_inp_fasta"])
    args["genome_name"] = util.none_from_str(args["genome_name"])
    return galaxy_jbrowse(**opt).vicvb_to_jbrowse(**args)

def main():
    from argh import ArghParser
    parser = ArghParser()
    parser.add_commands([to_jbrowse])
    parser.dispatch()

