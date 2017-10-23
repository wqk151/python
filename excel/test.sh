#!/bin/bash
set -x
set -e
#__date__=2017/3/30 0030 9:55
TripTimesAndMileageStat-201701-zhejiang.tar.gz
while read line
do
    while read sheng
    do
        while read manth
        do
        echo ${line}-${manth}-${sheng}.tar.gz >>/mnt/file
        done </mnt/math
    done </mnt/sheng
done < /mnt/moxing
