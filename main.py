from sourse.parse_data import parse_file

#1. List all 
#2. Set my location
#3. Search near taxi points
#4. Search by 'logradouro'
#5. End Program

FILE_PATH = '.\sourse\data\\taxi_data.csv'

tree, hash = parse_file(FILE_PATH)

