#!/bin/bash

file=$1

docker run project python ./src/dpclus_weighted.py $file > ./output/$1_dpclus_weighted.txt
docker run project python ./src/graph_entropy_weighted.py $file > ./output/$1_graph_entropy_weighted.txt
docker run project python ./src/ipca_weighted.py $file > ./output/$1_ipca_weighted.txt
docker run project python ./src/clique_percolation.py $file > ./output/$1_clique_percolation_no_weights.txt
docker run project python ./src/clique_percolation_weighted_k_3.py $file > ./output/$1_clique_percolation_k3.txt
docker run project python ./src/clique_percolation_weighted_k_4.py $file > ./output/$1_clique_percolation_k4.txt