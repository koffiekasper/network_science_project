#!/bin/bash

file=$1

docker run project python ./dependencies/dpclus_weighted.py ./dot_files/$file > ./output/$1_dpclus_weighted.txt
docker run project python ./dependencies/graph_entropy_weighted.py ./dot_files/$file > ./output/$1_graph_entropy_weighted.txt
docker run project python ./dependencies/ipca_weighted.py ./dot_files/$file > ./output/$1_ipca_weighted.txt
