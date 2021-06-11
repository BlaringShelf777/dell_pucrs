
# Classe responsável por armazenar a latitude
# e longitude do usuário

class User:
    def __init__(self, lat, lon):
        self.lat = lat
        self.lon = lon

    def __str__(self):
        return f'User({self.lat}, {self.lon})'
    
    def __repr__(self):
        return self.__str__()