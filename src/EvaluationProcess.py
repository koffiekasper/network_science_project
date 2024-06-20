import pandas as pd
from itertools import combinations
from numpy import exp
import networkx as nx
import pydot
from cdlib import evaluation, NodeClustering
import statistics
import sys



def run(partition_filename):
    #load the excel file
    path = 'final_dataset.xlsx'
    dataset = pd.read_excel(path)

    #select required columns
    data = dataset[['ExhibitionID', 'ConstituentID']]

    #find pairs of artists exhibited in the same exhibition
    pairs = (
        data.groupby('ExhibitionID')['ConstituentID']
        .apply(lambda x: pd.DataFrame(combinations(x, 2), columns=['artist_a', 'artist_b'])
            .assign(weight=1)
            ))

    #find the weights associated with each pair
    pairs_summed = pairs.groupby(['artist_a', 'artist_b']).agg(['sum', 'count']).reset_index()
    pairs_summed = pairs_summed[pairs_summed.weight['count'] > 0]

    #save the result in the form of a dot file
    output_dot_file = 'input_graph_file.dot'

    with open(output_dot_file, 'w') as f:
        for _, row in pairs_summed.iterrows():
            f.write(f'{row["artist_a"].values[0]} {row["artist_b"].values[0]} {row["weight"]["sum"]}\n')


    #find ground truth communities
    def table_to_communities_txt(df, output_file):
        grouped = df.groupby('movement')['ConstituentID'].apply(lambda x: ' '.join(x.astype(str).unique()))

        #remove duplicates
        unique_communities = grouped.drop_duplicates()

        # Write the unique communities to the output file
        with open(output_file, 'w') as file:
            for community in unique_communities:
                file.write(community + '\n')

    #dataset
    excel_file = './final_dataset.xlsx'
    df = pd.read_excel(excel_file)

    #output file
    output_file = 'final_ground_truth.txt'
    table_to_communities_txt(df, output_file)

    #use a dot file to create a networkX graph object
    def create_graph(dot_file_path, weighted=True):
        df = pd.read_csv(dot_file_path, delimiter=' ')
        df.columns = ['a', 'b', 'weight']
        unique_artists = pd.concat([df.a, df.b], ignore_index=True).astype(str).unique()
        if weighted:
            connections = [(str(r[1].a), str(r[1].b), {'weight': r[1].weight}) for r in df.iterrows()]
        else:
            connections = [(str(r[1].a), str(r[1].b)) for r in df.iterrows()]
        G = nx.Graph()
        
        G.add_nodes_from(unique_artists)
        G.add_edges_from(connections)

        return G

    #use the (output) text file to create communities
    def create_communities(file_path):
        communities = []
        with open(file_path, 'r') as file:
            for line in file:
                nodes = [str(node) for node in line.strip().split()]
                communities.append(nodes)
        return communities

    #select the dot file used to create the graph
    G = create_graph('./input_graph_file.dot')
    G_unweighted = create_graph('./input_graph_file.dot', False)
    #create communities using the ground truth file and the output file from the algorithm
    communitiesOUT = create_communities(f'{partition_filename}')
    communitiesGT = create_communities('final_ground_truth.txt')

    #calculate modularity
    modularityOUT = evaluation.modularity_overlap(G, NodeClustering(communitiesOUT, G, overlap=True)).score
    modularityGT = evaluation.modularity_overlap(G, NodeClustering(communitiesGT, G, overlap=True)).score

    #calculate the f score
    def f_score(predicted, ground_truth):
        intersection = len(set(predicted) & set(ground_truth))
        if intersection == 0:
            return 0
        precision = intersection / len(predicted)
        recall = intersection / len(ground_truth)
        return 2 * (precision * recall) / (precision + recall)

    #find the best match in the ground truth 
    best_matches = {}
    for predicted_community in communitiesOUT:
        max_f1 = -1
        best_match = None
        for gt_community in communitiesGT:
            score = f_score(predicted_community, gt_community)
            if score > max_f1:
                max_f1 = score
                best_match = gt_community
    #    best_matches[tuple(predicted_community)] = tuple(best_match)
        best_matches[tuple(predicted_community)] = max_f1

    #overall f score of the output
    fscoreOUT = sum(max_f for max_f in best_matches.values()) / len(best_matches)


    def weighed_density(G):
        n = nx.number_of_nodes(G)
        m = nx.number_of_edges(G)
        if m == 0 or n <= 1:
            return 0
        weighed_m = sum([w['weight'] for _, __, w in G.edges(data=True)])
        d = 2 * weighed_m / (n * (n - 1))
        return d

    #ground truth stats
    ground_truth_num_communities = len(communitiesGT)
    ground_truth_avg_size = statistics.mean(len(community) for community in communitiesGT)
    ground_truth_std_dev_size = statistics.stdev(len(community) for community in communitiesGT)
    ground_truth_max_size = max(len(community) for community in communitiesGT)

    ground_truth_avg_weighted_density = statistics.mean([weighed_density(G.subgraph(community)) for community in communitiesGT])
    ground_truth_avg_unweighted_density = statistics.mean(evaluation.internal_edge_density(G, NodeClustering(communitiesGT, G_unweighted, overlap=True), summary=False))
    ground_truth_proteins_covered = len(set.union(*(set(community) for community in communitiesGT)))

    predicted_densities = [nx.density(G.subgraph(community)) for community in communitiesOUT]
    #algorithm output stats
    predicted_num_communities = len(communitiesOUT)
    predicted_avg_unweighted_density = statistics.mean(predicted_densities)
    predicted_avg_weighted_density = statistics.mean([weighed_density(G.subgraph(community)) for community in communitiesOUT])
    #

    predicted_avg_size = statistics.mean(len(community) for community in communitiesOUT)
    predicted_std_dev_size = statistics.stdev(len(community) for community in communitiesOUT)
    predicted_max_size = max(len(community) for community in communitiesOUT)

    predicted_avg_unweighted_density = statistics.mean(evaluation.internal_edge_density(G, NodeClustering(communitiesOUT, G_unweighted, overlap=True), summary=False))

    predicted_proteins_covered = len(set.union(*(set(community) for community in communitiesOUT)))

    #make a table out of it
    data = {
        "": ["Predicted Communities", "Ground-Truth Communities"],
        "Number of Communities": [predicted_num_communities, ground_truth_num_communities],
        "Avg. Size (St. Dev.)": [(predicted_avg_size, predicted_std_dev_size), (ground_truth_avg_size, ground_truth_std_dev_size)],
        "Max Size": [predicted_max_size, ground_truth_max_size],
        "Avg. Unweighted Density": [predicted_avg_unweighted_density, ground_truth_avg_unweighted_density],
        "Avg. Weighted Density": [predicted_avg_weighted_density, ground_truth_avg_weighted_density],
        "Communities Covered": [predicted_proteins_covered, ground_truth_proteins_covered],
        "f-score": [fscoreOUT, None]
    }

    return pd.DataFrame(data)

file_name = sys.argv[1]

print(run(file_name))