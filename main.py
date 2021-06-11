from sourse.parse_data import parse_file, parse_coord
from sourse.user import User
from sourse.haversine import haversine
import os
import re

FILE_PATH = '.\sourse\data\\taxi_data.csv'

# Lista todos os pontos de taxi
def list_all(hash):
    for taxi_stand in hash.values():
        print(f'> {taxi_stand}\n')

# Pega as coordenadas do usuário
def user_location():
    get_coord = True
    re_exp = re.compile(r'(-?[0-9]+)|(-?[0-9]+,[0-9]+)')
    input_error = False

    while get_coord:
        if input_error:
            print('> ERRO! Posição inválida.\n')
            input_error = False
        lat = str(input('Digite sua latitude : ')).strip()
        lon = str(input('Digite sua longitude: ')).strip()
        if re_exp.fullmatch(lat) and re_exp.fullmatch(lon):
            get_coord = False
        else: input_error = True

    return User (parse_coord(lat), parse_coord(lon))

# Adiciona variantes de pesquisa
# para uma busca mais custosa,
# mas mais completa
def query_adjust(word):
    base_case = False
    words_arr = list()
    # Rua
    if word.startswith('r '):
        words_arr.append(word)
        words_arr.append(f'r.{word[1:]}')
        words_arr.append(f'rua{word[1:]}')
    elif word.startswith('r. '): 
        words_arr.append(word)
        words_arr.append(f'r{word[2:]}')
        words_arr.append(f'rua{word[2:]}')
    elif word.startswith('r.'):
        words_arr.append(word)
        words_arr.append(f'r {word[2:]}')
        words_arr.append(f'rua{word[2:]}')
    elif word.startswith('rua '): 
        words_arr.append(word)
        words_arr.append(f'r.{word[3:]}')
        words_arr.append(f'r{word[3:]}')
    elif word.startswith('rua'):
        words_arr.append(word)
        words_arr.append(f'r.{word[3:]}')
        words_arr.append(f'r {word[3:]}')

    # Avenida
    elif word.startswith('av '): 
        words_arr.append(word)
        words_arr.append(f'av.{word[2:]}')
        words_arr.append(f'avenida{word[2:]}')
    elif word.startswith('av. '):
        words_arr.append(word)
        words_arr.append(f'av{word[3:]}')
        words_arr.append(f'avenida{word[3:]}')
    elif word.startswith('av.'):
        words_arr.append(word)
        words_arr.append(f'av {word[3:]}')
        words_arr.append(f'avenida{word[3:]}')
    elif word.startswith('avenida '): 
        words_arr.append(word)
        words_arr.append(f'av.{word[7:]}')
        words_arr.append(f'av{word[7:]}')
    elif word.startswith('avenida '): 
        words_arr.append(word)
        words_arr.append(f'av.{word[7:]}')
        words_arr.append(f'av{word[7:]}')
    elif word.startswith('avenida'): 
        words_arr.append(word)
        words_arr.append(f'av.{word[7:]}')
        words_arr.append(f'av {word[7:]}')
    else: base_case = True

    if base_case: return [word]

    return words_arr

# Dado um prefixo, procura pelos logradouros
# com o mesmo prefixo na árvore ternária de pesquisa
def search_public_place(prefix, tree):
    if not len(prefix) or not tree: return

    prefix_list = query_adjust(prefix.lower())
    found = list()

    for pre in prefix_list:
        found += list(filter(lambda id: not id in found, tree.query(pre)))

    return found

# Dado um prefixo, uma árvore ternária de pesquisa
# e um mapa de hash, imprime todos os pontos de taxi
# em que o logradouro inicia com o prefixo dado
def show_taxi_stands(prefix, tree, hash_map):
    if not prefix or not len(prefix) or type(prefix) != str or not tree or not hash_map: return

    stand_ids = search_public_place(prefix, tree)

    if len(stand_ids):
        print(f'> Os pontos de taxi ao longo de {prefix} são:\n')
        for id in stand_ids: 
            print(f'{hash_map[id]}\n')
    else:
        print(f'> Nenhum ponto encontrado ao longo de {prefix}.\n')

# Pega o logradouro do usuário e chama
# as funções de pesquisa
def get_public_place(tree, hash_map):
    if not tree or not hash_map: return
    get_pre = True

    while get_pre:
        prefix = str(input('> Digite todo ou parte do nome do logradouro: ')).strip()
        if len(prefix): get_pre = False
    show_taxi_stands(prefix, tree, hash_map)

# Procura pelo elemento com a maior distância
def max_dist(arr):
    biggest = arr[0]

    for el in arr:
        if el['distance'] > biggest['distance']:
            biggest = el

    return biggest

# Procura os pontos de taxi mais proximos
# da posição do usuário
def closest_taxi_stand(user, hash, max=3):
    if not user or not hash: return

    closest = list()
    
    for taxi_stand in hash.values():
        # Vê a distância entre o usuário e o
        # ponto atual 
        distance_between = haversine(
            user.lat, user.lon, 
            taxi_stand.lat, taxi_stand.lon
        )

        # Preenche a lista de pontos de taxi
        # mais próximos do usuário
        if len(closest) < max:
            closest.append({
                'stand':taxi_stand, 
                'distance':distance_between
            })
        else: 
            swap = False

            # Verfica se o novo ponto está a uma distancia
            # menor do usuário
            for stand in closest:
                if distance_between < stand['distance']:
                    swap = True
                    break
            # Remove o ponto que está mais longe do usuário
            # e adiciona um novo ponto mais próximo 
            if swap:
                i = closest.index(max_dist(closest))

                closest.pop(i)

                closest.append ({
                    'stand':taxi_stand, 
                    'distance':distance_between
                })
    closest.sort(key=lambda stand: stand['distance'])
    print('> Os pontos de taxi mais próximos são:\n')
    for stand in closest:
        print(f'{stand}\n')

def screen_clear():
    input('\n> Precione \'Enter\' para continuar...')
    # mac linux
    if os.name == 'posix':
        _ = os.system('clear')
    else:
    # windows
      _ = os.system('cls')

tree, hash = parse_file(FILE_PATH)
user = None

while True:
    print('=== MENU ===\n1. Listar todos os pontos de taxi\n2. Informar minha localização\n3. Encontrar pontos próximos\n4. Buscar pontos por logradouro\n5. Terminar o programa')
    try:
        option = int(input('\n\n> Escolha uma das opções:\n'))
    except:
        print('> Escolha uma opção válida.')
        screen_clear()
        continue
    if   option == 1: list_all(hash)
    elif option == 2: user = user_location()
    elif option == 3: closest_taxi_stand(user, hash)
    elif option == 4: get_public_place(tree, hash)
    elif option == 5: break
    else: print(f'> Opção {option} não encontrado.\n')
    screen_clear()