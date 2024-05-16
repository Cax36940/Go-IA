# Import du fichier d'exemples
import numpy as np
import json

def get_raw_data_go():
    ''' Returns the set of samples from the local file or download it if it does not exists'''
    import gzip, os.path

    raw_samples_file = "samples-8x8.json.gz"

    if not os.path.isfile(raw_samples_file):
        print("File", raw_samples_file, "not found, I am downloading it...", end="")
        import urllib.request
        urllib.request.urlretrieve ("https://www.labri.fr/perso/lsimon/static/inge2-ia/samples-8x8.json.gz", "samples-8x8.json.gz")
        print(" Done")

    with gzip.open("samples-8x8.json.gz") as fz:
        data = json.loads(fz.read().decode("utf-8"))
    return data


def get_processed_data_go():
    ''' Returns the set of samples from the local file or download it if it does not exists'''
    with open('database-8x8.json', 'r') as f:
        return json.load(f)


couples = [(i, j) for i in range(8) for j in range(8)]

def name_to_coord(s):
    assert s != "PASS"
    indexLetters = {'A':0, 'B':1, 'C':2, 'D':3, 'E':4, 'F':5, 'G':6, 'H':7}

    col = indexLetters[s[0]]
    lin = int(s[1:])-1
    return col, lin


# Return only one board for 
def move_to_board(black_stones, white_stones):
    board = np.zeros((8,8))
    for black in black_stones:
        board[name_to_coord(black)] = 1
    for white in white_stones:
        board[name_to_coord(white)] = -1
    return board

def board_to_coords(board):
    black_coord = []
    white_coord = []
    for pos in couples:
        if board[pos] == 1:
            black_coord.append(pos)
        if board[pos] == -1:
            white_coord.append(pos)

    return (black_coord, white_coord)

def new_data_format(player_coords, depth, black_wins, white_wins):
    return {"current_player" : depth%2, "black_coord" : player_coords[0], "white_coord" : player_coords[1], "black_wins" : black_wins, "white_wins" : white_wins}

def boardx16(a_data):
    board = move_to_board(a_data["black_stones"], a_data["white_stones"])

    black_wins = a_data["black_wins"]
    white_wins = a_data["white_wins"]

    boards = []
    for i in range(4):
        boards.append(new_data_format(board_to_coords(board), a_data["depth"], black_wins, white_wins))
        boards.append(new_data_format(board_to_coords(np.transpose(board)), a_data["depth"], black_wins, white_wins))
        board = np.rot90(board)
    
    board = -1 * board

    for i in range(4):
        boards.append(new_data_format(board_to_coords(board), a_data["depth"] + 1, white_wins, black_wins))
        boards.append(new_data_format(board_to_coords(np.transpose(board)), a_data["depth"] + 1, white_wins, black_wins))
        board = np.rot90(board)

    return boards


data = get_raw_data_go()
number_datas = len(data)
print("We have", number_datas,"examples")

new_data = []

for i in range(2):
    new_data += boardx16(data[i])

with open('database-8x8.json', 'w') as f:
    json.dump(new_data,f)


