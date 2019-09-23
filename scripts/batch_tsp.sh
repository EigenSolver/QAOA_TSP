#!/bin/bash

for i in $(seq 3 7)
do
python ./QAOA_TSP.py -n $i -N 100 
done