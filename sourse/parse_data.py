from sourse.ternary_search_tree import TernarySearchTree
from sourse.taxi_stand import TaxiStand
import pandas

def parse_file(file_path):
    taxi_data = pandas.read_csv(file_path, ';')
    tree = TernarySearchTree()
    hash_map = {}

    for taxi_stand in taxi_data.iloc: 
        tree.insert_taxi_stand(taxi_stand.logradouro.lower(), taxi_stand.codigo)
        hash_map[taxi_stand.codigo] = TaxiStand(
            taxi_stand.logradouro.lower(),
            taxi_stand.nome,
            taxi_stand.telefone, 
            taxi_stand.numero, 
            taxi_stand.latitude, 
            taxi_stand.longitude)
    return tree, hash_map