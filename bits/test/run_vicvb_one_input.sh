#!/bin/bash
#Assuming that you have sourced VICVB.rc
curdir=$(pwd)
#input=/home/atovtchi/work/jcvi_cloud_vir/lib/VICVB/data/test_data/VIGOR/NCBI.one_dir/FluB_one
input=/home/atovtchi/work/jcvi_cloud_vir/test_data_extra/VIGOR_exception_cases/SARS
output_redir_html=$curdir/index_test_out.html
output_dir=$curdir/test_out
$(dirname $VICVB_CONF)/vicvb_galaxy_tool to-jbrowse None None $input $output_redir_html $output_dir

