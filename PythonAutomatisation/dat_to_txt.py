import argparse
import os

from ennemy import Ennemy
from gamedata import GameData

if __name__ == '__main__':
    parser = argparse.ArgumentParser(prog="Dat to txt",
                                     description="This program allow you to quickly read a dat file searching for text")
    parser.add_argument("path", help="Path to dat file (with name)", type=str)
    args = parser.parse_args()

    hex_index = 0
    file_raw_data = []
    futur_file_name = args.path.split(os.path.sep)[-1].split('.')[0] + '.txt'
    index = 0
    game_data = GameData()  # For translate table
    with open(args.path, "rb") as f:
        while el := f.read(1):
            file_raw_data.append(int.from_bytes(el))

    translated_data = game_data.translate_hex_to_str(file_raw_data)
    print(file_raw_data)
    with open(os.path.join(os.getcwd(), futur_file_name), "wb") as f:
        for by in translated_data:
            f.write(by.encode('unicode_escape'))
