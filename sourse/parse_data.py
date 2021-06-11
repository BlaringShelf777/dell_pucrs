from sourse.ternary_search_tree import TernarySearchTree
from sourse.taxi_stand import TaxiStand
import pandas

# Faz o parsing das coordenadas para float
def parse_coord(coord):
    return float('.'.join(coord.split(',')))

# Faz o parsing do arquivo csv e constói
# uma árfvore ternária de pesquisa com
# os logradoutros de cada ponto e um
# map de hash com os ids de cada ponto
def parse_file(file_path):
    taxi_data = pandas.read_csv(file_path, ';')
    tree = TernarySearchTree()
    hash_map = {}

    for taxi_stand in taxi_data.iloc: 
        # Insere o ponto de taxi na árvore
        tree.insert_taxi_stand(taxi_stand.logradouro.lower(), taxi_stand.codigo)
        # Insere o ponto de taxi no mapa de hash
        hash_map[taxi_stand.codigo] = TaxiStand(
            taxi_stand.logradouro.lower(),
            taxi_stand.nome,
            taxi_stand.telefone, 
            taxi_stand.numero, 
            parse_coord(taxi_stand.latitude), 
            parse_coord(taxi_stand.longitude)
        )
        
    return tree, hash_map