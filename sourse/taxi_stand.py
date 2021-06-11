

class TaxiStand:
    def __init__(self, public_place, name, phone, number, lat, lon):
       self.public_place = public_place
       self.name = name
       self.phone = phone
       self.number = number
       self.lat = lat
       self.lon = lon
    
    def __str__(self):
        return f'PontoDeTaxi(Logradouro:"{self.public_place}", Nome:"{self.name}", Telefone:"{self.phone}", Nº:"{self.number}", Coord.:"({self.lat}, {self.lon})")'
    
    def __repr__(self):
        return self.__str__()