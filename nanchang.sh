#!/bin/bash
set -x
set -e
#__date__=2016/10/19 0019 16:31
data_line_num=""
function get_data_line_num(){
        data_line_num=$(tail -n9  file   | grep '[[:digit:]]$'  | grep -v Performance  |wc -l)
}
get_data_line_num
#echo $data_line_num
if [ $data_line_num -lt 1 ];then
    echo "data is empty"
    echo $data_line_num # restart program
    sleep 60 # wait 60s
    get_data_line_num
    if [ $data_line_num -lt 1 ];then
        echo "data also is empty please wait 10min"
        echo $data_line_num  # restart program
     else
        conitune
     fi
else
    conitune


fi
