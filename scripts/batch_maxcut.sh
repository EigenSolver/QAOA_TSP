#!/bin/bash

for i in $(seq 4 20)
do
python ./MAXCUT_QAOA.py -n $i -N 100 
done