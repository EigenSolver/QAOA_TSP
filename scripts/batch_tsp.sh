#!/bin/bash

for i in $(seq 3 6)
do
python ./TSP_QAOA.py -n $i -N 100 
done