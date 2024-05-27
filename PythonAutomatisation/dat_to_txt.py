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
    file_raw_data = "0x00>"
    futur_file_name = args.path.split(os.path.sep)[-1].split('.')[0] + '.txt'
    index = 0
    game_data = GameData() # For translate table
    with open(args.path, "rb") as f:
        while el := f.read(1):
            int_value = int.from_bytes(el)
            file_raw_data += game_data.translate_hex_to_str_table[int_value] # For translate table
            if index > 64:
                file_raw_data +="\r\n0x{}>".format(hex_index)
                index = 0
            else:
                index += 1
            hex_index+=1


    with open(os.path.join(os.getcwd(),futur_file_name) , "w") as f:
        for by in file_raw_data:
            try:
                f.write(by)
            except UnicodeEncodeError:
                f.write("")