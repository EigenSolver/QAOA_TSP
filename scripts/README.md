# How to run the simulation

1. install the `optimizeq` library
```
git clone https://github.com/Neuromancer43/QAOA_LIB
cd QAOA_LIB
pip install .
```

2. download QAOA_TSP repo and run scripts
```
git clone https://github.com/Neuromancer43/QAOA_TSP
cd QAOA_TSP
```
activate execution & run
```
chmod u+x ./scripts/batch_tsp.sh && chmod u+x ./scripts/batch_maxcut.sh
./scripts/batch_maxcut.sh && ./scripts/batch_tsp.sh
```
3. run the final 7x7 tsp
this may take lot of time, so run it at last
```
chmod u+x ./scripts/7x7_tsp.sh
./scripts/7x7_tsp.sh
```
