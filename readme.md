# Installation
The installation of this app consists of two dinstinct steps: First, you will generate the artificially weighed .DOT files used in the experiments. After that, you will build the Docker project. 

## Usage - Generate DOT files
To generate the .DOT files that implement the weights we used in our experiments, 
run `populate_dot_files.py`.  This populates the `/dot_files/` folder:
	``python3 ./data_manipulation/populate_dot_files.py``

## Building the project
To build the Docker project, open a terminal / PowerShell from the project's root and type in the following command:
	```docker build -t project . ```

# Using the app
The Python script `run_all_experiments.py` will scan the `./dot_files/` folder for .DOT files, and apply Graph Entropy, DPClus and IPCA on every one detected. The resulting community layouts will be found in the `/output/` folder, and their respective quality metrics within `./output_metrics/`. The code used to obtain the style lables for the ground truth is available in `StyleLabelsWikidata.py`

``python3 ./run_all_experiments.py

``python3 ./StyleLabelsWikidata.py

#### Dependencies:
- Python 3
- Docker
- pandas
- numpy
- networkx
- cdlib
To install the Python packages, use the provided `requirements.txt` file like so:
`pip install -r requirements.txt`
