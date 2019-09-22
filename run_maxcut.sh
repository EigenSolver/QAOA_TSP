#!/bin/bash
####################################
#
# Backup to NFS mount script.
#
####################################
for i in $(seq 4 20)
do
python ./MAXCUT_solution.py -n $i -N 100 
done