# Ternary Search Tree
class TernarySearchTree:
    def __init__(self):
        self.root = None
    
    def insert_taxi_stand(self, public_place, stand_id):
        new_node = Node (
            public_place[-1], 
            public_place, 
            stand_id
        )

        if len(public_place) <= 0:
            return
        self.root = self.__insert_taxi_stand(self.root, public_place, new_node)
    
    def __insert_taxi_stand(self, node, public_place, taxi_stand):
        # Primeiro caracter do logradouro
        letter = public_place[0]
        # Node atual não existe
        if node == None:
            node = Node(letter)
        # Nodo atual maior que o a ser inserido verificar esquerda
        elif node.key > letter:
            node.child[0] = self.__insert_taxi_stand(node.child[0], public_place, taxi_stand)
            return node
        # Nodo atual menor que o a ser inserido verificar direita
        elif node.key < letter:
            node.child[2] = self.__insert_taxi_stand(node.child[2], public_place, taxi_stand)
            return node            
        # Verifica se chegou ao fim do logradouro
        if len(public_place) == 1:
            # Cria ponto de taxi caso ele já não exista
            if node.public_place == None:
                node = taxi_stand
            return node
        node.child[1] = self.__insert_taxi_stand(node.child[1], public_place[1:], taxi_stand)
        return node

    def query(self, public_place, prefix=True):
        if public_place == '':
            return 
        global taxi_stands
        taxi_stands = list()
        self.__query(public_place.lower(), self.root, prefix)
        return taxi_stands
    
    def __query(self, public_place, node, prefix):
        # Nodo não encontrado
        if node == None:
            return
        # Percore a árvore árvore enquanto o prefixo do logradouro
        # informado pelo usuário não for vazio 
        if public_place != '':
            letter = public_place[0]
            if node.key == letter:
                if len(public_place) == 1 and node.public_place != None:
                    taxi_stands.append(node.id)
                    if not prefix:
                        return
                self.__query(public_place[1:], node.child[1], prefix)
            elif node.key > letter:
                self.__query(public_place, node.child[0], prefix)
            else:
                self.__query(public_place, node.child[2], prefix)
            return
        else:
            if node.public_place != None:
                taxi_stands.append(node.id)
            if node.child[1] != None:
                self.__query(public_place, node.child[1], prefix)
            self.__query(public_place, node.child[0], prefix)
            self.__query(public_place, node.child[2], prefix)

class Node:
    def __init__(self, key, public_place=None, stand_id=None):
        self.key = key
        self.public_place = public_place
        self.id = stand_id
        self.child = [None, None, None]