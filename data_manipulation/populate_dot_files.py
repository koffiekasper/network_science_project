import pandas as pd
import numpy as np
from itertools import combinations


class DatasetManipulator:
    def __init__(self, excel_path):
        self.excel_path = excel_path
        self.data = pd.read_excel(self.excel_path)
        self.data = self.data[['ExhibitionID', 'ConstituentID']]

        self.pairs = (
            self.data.groupby(['ExhibitionID'])['ConstituentID']
            .apply(lambda x: pd.DataFrame(combinations(x, 2), columns=['artist_a', 'artist_b'])
            .assign(weighed_sum=1/len(x)))
            .reset_index(drop=True)
        )
        self.pairs['weight'] = 1
        
    def write_dot_files(self):
        result = self.pairs.groupby(['artist_a', 'artist_b']).agg({'weight': 'sum', 'weighed_sum': 'sum'}).reset_index()
        filters = [
            (result[result['weight'] > 0], "0"),
            (result[result['weight'] > 1], "1"),
            (result[result['weight'] > 5], "5"),
            (result[result['weight'] < 250], "250"),
            (result[(result['weight'] < 250) & (result['weight'] > 1)], "1_250"),
            (result[(result['weight'] < 250) & (result['weight'] > 5)], "5_250")
         ]
        
        for filter_tuple in filters:
            output_dot_file = f'./dot_files/artist_pairs_with_weights{filter_tuple[1]}.dot'
            output_exp_dot_file = f'./dot_files/artist_pairs_with_weights_exp_{filter_tuple[1]}.dot'
            output_partial_weights_dot_file = f'./dot_files/artist_pairs_with_weights_partial_weights_{filter_tuple[1]}.dot'

            with open(output_dot_file, 'w') as f:
                with open(output_exp_dot_file, 'w') as f_exp:
                    with open(output_partial_weights_dot_file, 'w') as f_p:
                        for _, row in filter_tuple[0].iterrows():
                            f.write(f'{row["artist_a"]} {row["artist_b"]} {row["weight"]}\n')
                            f_exp.write(f'{row["artist_a"]} {row["artist_b"]} {np.exp(row["weight"])}\n')
                            f_p.write(f'{row["artist_a"]} {row["artist_b"]} {row["weighed_sum"]}\n')
        

dm = DatasetManipulator("./final_dataset.xlsx")
dm.write_dot_files()

