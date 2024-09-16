import glob
import os
import shutil
from math import floor

from simple_file_checksum import get_checksum


class Ennemy():

    def __init__(self):
        self.name = ""
        self.file_raw_data = bytearray()
        self.data = []
        self.pointer_data_start = 0
        self.origin_file_name = ""
        self.origin_file_checksum = ""

    def __repr__(self):
        return "Name: {} \nData:{}".format(self.name, self.data)

    def load_file_data(self, file, game_data):
        with open(file, "rb") as f:
            while el := f.read(1):
                self.file_raw_data.extend(el)

        # First we get the "pointer value", which is the pointer at which the file data start.
        if '123' in file:  # Weird case, the 123 file is a garbage anyway but this is to avoid error
            data_pointer = 4
        else:
            data_pointer = game_data.USEFUL_DATA_POINTER['offset']
        self.pointer_data_start = int.from_bytes(self.file_raw_data[data_pointer:data_pointer + game_data.USEFUL_DATA_POINTER['size']], game_data.USEFUL_DATA_POINTER["byteorder"])

        self.origin_file_name = os.path.basename(file)
        self.origin_file_checksum = get_checksum(file, algorithm='SHA256')

    def load_name(self, game_data):
        # The name is a bit more tricky. A specific conversion needs to happen, that depends on the localization. The translation is done in a text file.
        name_data = self.file_raw_data[self.pointer_data_start + game_data.NAME_DATA['offset']:  self.pointer_data_start + game_data.NAME_DATA['offset'] + game_data.NAME_DATA['size']]
        for el in name_data:
            if el < 0x20:
                break
            else:
                self.name += Ennemy.translate_hex_to_str(el - 0x20)

    def translate_hex_to_str(hex):
        with open("Ressources/sysfnt.txt", "r", encoding="utf-8") as localize_file:
            file = localize_file.read()
            file = file.replace('\n', '')
            file = file.split("\",\"")
            file[0] = file[0][1:]  # Special case for the split
            file[-1] = file[-1][:-1]  # Special case for the split

        return file[hex]

    def analyse_loaded_data(self, game_data):
        """This is the main function. Here we have several cases.
        So first the based stat. As there is 4 stats for each in order to compute the final stat, they are stored in a list of size 4.
        For card, this is the ID for the different case: DROP, MOD, RARE_MOD
        There is common value of size 1, just raw value.
        % case with specific compute
        Elem and status have specific computation
        Devour is a set of ID for Low, medium, High
        Abilities TODO
        """
        for el in game_data.LIST_DATA:
            raw_data_selected = self.file_raw_data[self.pointer_data_start + el['offset']:  self.pointer_data_start + el['offset'] + el['size']]
            if el['name'] in (game_data.stat_values + ['card', 'devour', 'abilities']):
                value = list(raw_data_selected)

            elif el['name'] in ['med_lvl', 'high_lvl', 'extra_xp', 'xp', 'ap']:
                value = int.from_bytes(raw_data_selected)

            elif el['name'] in ['low_lvl_mag', 'med_lvl_mag', 'high_lvl_mag', 'low_lvl_mug', 'med_lvl_mug', 'high_lvl_mug', 'low_lvl_drop', 'med_lvl_drop', 'high_lvl_drop']:  # Case with 4 values linked to 4 IDs
                list_data = list(raw_data_selected)
                value = []
                for i in range(0, el['size'] - 1, 2):
                    value.append({'ID': list_data[i], 'value': list_data[i + 1]})

            elif el['name'] in ['mug_rate', 'drop_rate']:  # Case with %
                value = int.from_bytes(raw_data_selected) * 100 / 256

            elif el['name'] in ['elem_def']:  # Case with elem
                value = list(raw_data_selected)
                for i in range(el['size']):
                    value[i] = 900 - value[i] * 10  # Give percentage

            elif el['name'] in ['status_def']:  # Case with elem
                value = list(raw_data_selected)
                for i in range(el['size']):
                    value[i] = value[i] - 100  # Give percentage, 155 means immune.

            else:
                value = "ERROR UNEXPECTED VALUE"

            self.data.append({'name': el['name'], 'value': value, 'pretty_name': el['pretty_name']})

    def write_data_to_file(self, game_data, path):
        # First copy original file
        full_dest_path = os.path.join(path, self.origin_file_name)


        # Then load file (python make it difficult to directly modify files)
        self.load_file_data(full_dest_path, game_data)

        # Then modify loaded file
        for el in self.data:
            property_elem = [x for ind, x in enumerate(game_data.LIST_DATA) if x['name'] == el['name']][0]
            if el['name'] in (game_data.stat_values + ['card', 'devour', 'abilities']):  # List
                value_to_set = bytes(el['value'])
            elif el['name'] in ['med_lvl', 'high_lvl', 'extra_xp', 'xp', 'ap']:
                value_to_set = el['value'].to_bytes()
            elif el['name'] in ['low_lvl_mag', 'med_lvl_mag', 'high_lvl_mag', 'low_lvl_mug', 'med_lvl_mug', 'high_lvl_mug', 'low_lvl_drop', 'med_lvl_drop', 'high_lvl_drop']:  # Case with 4 values linked to 4 IDs
                value_to_set = []
                for el2 in el['value']:
                    value_to_set.append(el2['ID'])
                    value_to_set.append(el2['value'])
                value_to_set = bytes(value_to_set)
            elif el['name'] in ['mug_rate', 'drop_rate']:  # Case with %
                value_to_set = floor(el['value'] * 256 / 100).to_bytes()
            elif el['name'] in ['elem_def']:  # Case with elem
                value_to_set = []
                for i in range(len(el['value'])):
                    value_to_set.append(floor((900 - el['value'][i]) / 10))
                value_to_set = bytes(value_to_set)
            elif el['name'] in ['status_def']:  # Case with elem
                value_to_set = []
                for i in range(len(el['value'])):
                    value_to_set.append(el['value'][i] + 100)
                value_to_set = bytes(value_to_set)

            if value_to_set:
                self.file_raw_data[self.pointer_data_start + property_elem['offset']:
                                   self.pointer_data_start + property_elem['offset'] + property_elem['size']] = value_to_set
            value_to_set = None

        # Write back on file
        with open(full_dest_path, "wb") as f:
            f.write(self.file_raw_data)
