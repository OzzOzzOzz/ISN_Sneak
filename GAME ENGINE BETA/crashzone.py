from os import path

game_folder = path.dirname(__file__)
map_data = []
with open(path.join(game_folder, 'map.txt'), 'rt')as f:
    for line in f:
        map_data.append(line)

print(map_data)

for row, tiles in enumerate(map_data):
    for column, tile in enumerate(tiles):
        if tile == '1':
            print(row, column, tile)
