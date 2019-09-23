#!/bin/bash

for i in $(seq 3 7)
do
python ./TSP_QAOA.py -n $i -N 100 
done