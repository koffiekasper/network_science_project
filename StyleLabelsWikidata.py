import pandas as pd
from wikidata.client import Client
from tqdm import tqdm  #adds progress bar, to make sure everything is running correctly

#load excel file
df = pd.read_excel('/Users/maggie/Desktop/New Folder With Items/MoMAExhibitionsData.xlsx')

#initialize wikidata client
client = Client()

def fetch_movements(wikidata_ids):
    movements_map = {}
    for wikidata_id in tqdm(wikidata_ids, desc="Fetching Movements"):
        if pd.isna(wikidata_id):
            continue
        try:
            entity = client.get(wikidata_id, load=True)
            movements = entity.data['claims'].get('P135')  #P135 is the 'movement' property on WikiData
            if not movements:
                movements_map[wikidata_id] = []
            else:
                movement_labels = []
                for movement in movements:
                    movement_id = movement['mainsnak']['datavalue']['value']['id']
                    movement_entity = client.get(movement_id, load=True)
                    movement_label = movement_entity.label.get('en')  #make sure label is in english
                    if movement_label:
                        movement_labels.append(movement_label)
                movements_map[wikidata_id] = movement_labels
        except Exception as e:
            print(f"Error fetching movements for {wikidata_id}: {e}")
            movements_map[wikidata_id] = []
    return movements_map

#find movements for all WikidataID's in the dataset
wikidata_ids = df['WikidataID'].tolist()
movements_map = fetch_movements(wikidata_ids)

#process each row
new_rows = []

for _, row in tqdm(df.iterrows(), total=len(df), desc="Processing Rows"):
    wikidata_id = row['WikidataID']
    movements = movements_map.get(wikidata_id, [])
    if movements:
        for movement in movements:
            new_row = row.copy()
            new_row['movement'] = movement
            new_rows.append(new_row)
    else:
        new_row = row.copy()
        new_row['movement'] = None
        new_rows.append(new_row)

#create a new dataframe with new rows
new_df = pd.DataFrame(new_rows)

#save the new dataframe to excel
new_df.to_excel('artist_data_with_movements.xlsx', index=False)

#load dataset from excel
data_path = "/mnt/data/dataset_smaller.xlsx"
data = pd.read_excel(data_path)

#get and save a list of all the movemetns for analysis
movement_list = pd.DataFrame(data['movement'].unique(), columns=['movement'])
movement_list.to_excel('movement_list.xlsx', index=False)

#update movement names
def replace_movement(data, old_value, new_value):
    data['movement'] = data['movement'].replace(old_value, new_value)
    return data

#first set of changes
data_update1 = data.copy()
data_update1 = replace_movement(data_update1, "New Objectivity", "Neues Bauen")
data_update1 = replace_movement(data_update1, "American scene painting", "American Painting")
data_update1 = replace_movement(data_update1, "expressionism", "Expressionism")
data_update1 = replace_movement(data_update1, "degenerate art", "modern art")
data_update1 = replace_movement(data_update1, "Renaissance Revival architecture", "Renaissance architecture")
data_update1 = replace_movement(data_update1, "Greek Revival architecture", "Neoclassical Architecture")
data_update1 = data_update1[data_update1['movement'] != "Section d'Or"]
data_update1 = data_update1[data_update1['movement'] != "Dutch and Flemish Renaissance painting"]
data_update1 = replace_movement(data_update1, "French romanticism", "Romanticism")
data_update1 = replace_movement(data_update1, "Belgian surrealism", "surrealism")
data_update1 = replace_movement(data_update1, "Counter-Reformation", "Protestantism")
data_update1 = replace_movement(data_update1, "Renaissance painting", "Renaissance")
data_update1 = replace_movement(data_update1, "Die Brücke", "Expressionism")
data_update1 = replace_movement(data_update1, "American Impressionism", "Impressionism")
data_update1 = replace_movement(data_update1, "Fuerteventura Airport", "Expressionism")
data_update1 = replace_movement(data_update1, "French New Wave", "New Wave in cinema")
data_update1 = replace_movement(data_update1, "abstraction", "abstract art")
data_update1 = replace_movement(data_update1, "Baroque painting", "Baroque")
data_update1 = replace_movement(data_update1, "neo-fascism", "fascism")
data_update1 = data_update1[data_update1['movement'] != "Fascist mysticism"]
data_update1 = data_update1[data_update1['movement'] != "individualism"]
data_update1 = data_update1[data_update1['movement'] != "modernist literature"]
data_update1 = data_update1[data_update1['movement'] != "20th-century classical music"]
data_update1 = replace_movement(data_update1, "German Expressionism", "Expressionism")
data_update1 = replace_movement(data_update1, "feminist art movement", "feminist art")
data_update1 = replace_movement(data_update1, "New German Cinema", "New Wave in cinema")
data_update1 = data_update1[data_update1['movement'] != "digital art"]
data_update1 = data_update1[data_update1['movement'] != "light art"]
data_update1 = replace_movement(data_update1, "feminism", "feminist art")
data_update1 = replace_movement(data_update1, "No Wave Cinema", "New Wave in cinema")
data_update1 = replace_movement(data_update1, "Hong Kong New Wave", "New Wave in cinema")
data_update1 = replace_movement(data_update1, "literary realism", "realism")
data_update1 = data_update1.drop_duplicates()

#second set of changes
data_update2 = data_update1.copy()
data_update2 = replace_movement(data_update2, "Cloisonnism", "post-impressionism")
data_update2 = replace_movement(data_update2, "pointillism", "neo-impressionism")
data_update2 = replace_movement(data_update2, "Precisionism", "magic realism")
data_update2 = replace_movement(data_update2, "Catalan modernism", "Art Nouveau")
data_update2 = replace_movement(data_update2, "Ashcan School", "realism")
data_update2 = replace_movement(data_update2, "American modernism", "modernism")
data_update2 = replace_movement(data_update2, "Les Nabis", "post-impressionism")
data_update2 = replace_movement(data_update2, "Orphism", "cubism")
data_update2 = replace_movement(data_update2, "simultanism", "cubism")
data_update2 = replace_movement(data_update2, "divisionism", "neo-impressionism")
data_update2 = replace_movement(data_update2, "Bauhaus", "Neues Bauen")
data_update2 = replace_movement(data_update2, "action painting", "abstract expressionism")
data_update2 = replace_movement(data_update2, "Realism", "realism")
data_update2 = replace_movement(data_update2, "Barbizon school", "realism")
data_update2 = replace_movement(data_update2, "Mexican muralism", "social realism")
data_update2 = replace_movement(data_update2, "Movimento Arte Concreta", "Informalism and Geometric Abstraction")
data_update2 = replace_movement(data_update2, "German Renaissance", "Renaissance")
data_update2 = replace_movement(data_update2, "Early Netherlandish painting", "Renaissance")
data_update2 = replace_movement(data_update2, "Northern Renaissance", "Renaissance")
data_update2 = replace_movement(data_update2, "High Renaissance", "Renaissance")
data_update2 = replace_movement(data_update2, "mannerism", "Renaissance")
data_update2 = replace_movement(data_update2, "Streamline Moderne", "Art Deco")
data_update2 = replace_movement(data_update2, "Venetian school", "Renaissance")
data_update2 = replace_movement(data_update2, "Dutch Golden Age painting", "Baroque")
data_update2 = replace_movement(data_update2, "Spanish Renaissance", "Renaissance")
data_update2 = replace_movement(data_update2, "Luminism", "neo-impressionism")
data_update2 = replace_movement(data_update2, "Salon Cubism", "Cubism")
data_update2 = replace_movement(data_update2, "postmodern architecture", "postmodern art")
data_update2 = replace_movement(data_update2, "Baroque architecture", "Baroque")
data_update2 = replace_movement(data_update2, "baroque architecture", "Baroque")
data_update2 = replace_movement(data_update2, "Renaissance architecture", "Renaissance")
data_update2 = replace_movement(data_update2, "expressionist architecture", "Expressionism")
data_update2 = replace_movement(data_update2, "Neoclassical architecture", "Renaissance")
data_update2 = replace_movement(data_update2, "Angry Penguins", "modernism")
data_update2 = replace_movement(data_update2, "Tachisme", "abstract expressionism")
data_update2 = replace_movement(data_update2, "Viennese Actionism", "performance art")
data_update2 = replace_movement(data_update2, "deconstructivism", "postmodern art")
data_update2 = replace_movement(data_update2, "Rayonism", "Russian avant-garde")
data_update2 = replace_movement(data_update2, "German Renaissance", "Renaissance")
data_update2 = replace_movement(data_update2, "Early Renaissance", "Renaissance")
data_update2 = replace_movement(data_update2, "Italian Renaissance", "Renaissance")
data_update2 = replace_movement(data_update2, "Lyrical Abstraction", "abstract expressionism")
data_update2 = replace_movement(data_update2, "Jugendstil", "Art Nouveau")
data_update2 = replace_movement(data_update2, "concrete art", "geometric abstraction")
data_update2 = replace_movement(data_update2, "high-tech architecture", "modernism")
data_update2 = replace_movement(data_update2, "modern architecture", "modernism")
data_update2 = replace_movement(data_update2, "French Impressionist Cinema", "Impressionism")
data_update2 = data_update2.drop_duplicates()

#save final dataset, only include artists with an associated movement
final_dataset = data_update2.dropna(subset=['movement'])
final_dataset.to_excel('final_dataset.xlsx', index=False)