#!/bin/bash
set -ex
#bp_genbank2gff3.pl NC_001617.1.gb
genbank_to_gff.py NC_001617.1.gb
mv NC_001617.1.gff NC_001617.1.gb.gff
rm -rf data
jbrowse/bin/prepare-refseqs.pl --fasta NC_001617.1.fa
jbrowse/bin/flatfile-to-json.pl --gff NC_001617.1.gb.gff --trackLabel NC_001617.1
pushd data/tracks/NC_001617.1/
mv NC_001617* "gi|9627730|ref|NC_001617.1|"
popd
jbrowse/bin/generate-names.pl --out data

