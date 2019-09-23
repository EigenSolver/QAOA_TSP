#!/bin/bash

for i in $(seq 4 20)
do
python ./MAXCUT_QAOA.py -n $i -N 100 
done

for j in $(seq 2 10)
do
python ./MAXCUT_QAOA.py -n 15 -N 100 -p $j
done
