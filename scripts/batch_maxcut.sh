#!/bin/bash

for i in $(seq 4 20)
do
python ./QAOA_MAXCUT.py -n $i -N 100 
done