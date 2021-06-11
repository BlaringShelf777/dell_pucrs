from ternary_search_tree import TernarySearchTree
from haversine import haversine
import pandas



#1. List all 
#2. Set my location
#3. Search near taxi points
#4. Search by 'logradouro'
#5. End Program



def parse_file(file_path):
    taxi_data = pandas.read_csv(file_path, ';')
    tree = TernarySearchTree()
    hash_map = {}

    for taxi_stand in taxi_data.iloc: 
        tree.insert_taxi_stand(
            taxi_stand.logradouro.lower(), 
            taxi_stand.codigo, 
            taxi_stand.nome,
            taxi_stand.telefone, 
            taxi_stand.numero, 
            taxi_stand.latitude, 
            taxi_stand.longitude)
        hash_map[taxi_stand.codigo] = True
    return tree
    

t = parse_file('taxi_data.csv')