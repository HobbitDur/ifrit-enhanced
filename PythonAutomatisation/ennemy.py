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
        self.pointer_battle_script_data_start = 0
        self.origin_file_name = ""
        self.origin_file_checksum = ""
        self.text_battle = []
        self.text_subsection_offset = 0

    def __repr__(self):
        return "Name: {} \nData:{}".format(self.name, self.data)

    def __analyze_battle_section(self, game_data):
        # Get sub
        text_subsection_offset_raw_data = self.file_raw_data[self.pointer_battle_script_data_start +
                                                             game_data.DATA_POINTER_SUBSECTION_OFFSET['offset']:
                                                             self.pointer_battle_script_data_start +
                                                             game_data.DATA_POINTER_SUBSECTION_OFFSET['offset'] +
                                                             game_data.DATA_POINTER_SUBSECTION_OFFSET['size']]
        self.text_subsection_offset = int.from_bytes(text_subsection_offset_raw_data, byteorder=game_data.DATA_POINTER_SUBSECTION_OFFSET['byteorder'])
        text_offset_raw_data = self.file_raw_data[self.pointer_battle_script_data_start +
                                                  game_data.DATA_POINTER_TEXT_OFFSET['offset']:
                                                  self.pointer_battle_script_data_start +
                                                  game_data.DATA_POINTER_TEXT_OFFSET['offset'] +
                                                  game_data.DATA_POINTER_TEXT_OFFSET['size']]

        text_offset = int.from_bytes(text_offset_raw_data, byteorder=game_data.DATA_POINTER_TEXT_OFFSET['byteorder'])
        # We estimate that the nb of offset value is the diff between the two section
        nb_text = self.text_subsection_offset - text_offset

        text_list_pointer = []
        for i in range(0, nb_text, 2):
            text_list_raw_data = self.file_raw_data[self.pointer_battle_script_data_start + text_offset + i:
                                                    self.pointer_battle_script_data_start + text_offset +
                                                    game_data.BATTLE_TEXT_OFFSET['size'] + i]
            if i > 0 and text_list_raw_data == b'\x00\x00':  # Weird case where there is several pointer by the diff but several are 0 (which point to the same value)
                break
            text_list_pointer.append(int.from_bytes(text_list_raw_data, byteorder=game_data.BATTLE_TEXT_OFFSET['byteorder']))

        for index, text_pointer in enumerate(text_list_pointer):
            combat_text_raw_data = bytearray()
            for i in range(100):
                if self.pointer_battle_script_data_start + self.text_subsection_offset + text_pointer + i >= len(self.file_raw_data):
                    # Shouldn't happen, only on garbage data
                    pass
                else:
                    raw_value = self.file_raw_data[self.pointer_battle_script_data_start + self.text_subsection_offset + text_pointer + i]
                    if raw_value != 0:
                        combat_text_raw_data.extend(int.to_bytes(raw_value))
                    else:
                        break
            text = game_data.translate_hex_to_str(combat_text_raw_data)
            self.text_battle.append(text)

    def load_file_data(self, file, game_data):
        with open(file, "rb") as f:
            while el := f.read(1):
                self.file_raw_data.extend(el)

        # First we get the "pointer value", which is the pointer at which the file data start.
        if '123' in file:  # Weird case, the 123 file is a garbage anyway but this is to avoid error
            data_pointer = 4
        else:
            data_pointer = game_data.DATA_POINTER_INFO_STAT['offset']
        self.pointer_data_start = int.from_bytes(self.file_raw_data[data_pointer:data_pointer + game_data.DATA_POINTER_INFO_STAT['size']],
                                                 game_data.DATA_POINTER_INFO_STAT["byteorder"])
        data_pointer = game_data.DATA_POINTER_BATTLE_SCRIPT['offset']
        self.pointer_battle_script_data_start = int.from_bytes(self.file_raw_data[data_pointer:data_pointer + game_data.DATA_POINTER_BATTLE_SCRIPT['size']],
                                                               game_data.DATA_POINTER_BATTLE_SCRIPT["byteorder"])
        self.origin_file_name = os.path.basename(file)
        self.origin_file_checksum = get_checksum(file, algorithm='SHA256')

    def load_name(self, game_data):
        # The name is a bit more tricky. A specific conversion needs to happen, that depends on the localization. The translation is done in a text file.
        name_data = self.file_raw_data[
                    self.pointer_data_start + game_data.NAME_DATA['offset']:  self.pointer_data_start + game_data.NAME_DATA['offset'] + game_data.NAME_DATA[
                        'size']]

        self.name += game_data.translate_hex_to_str(name_data)

    def analyse_loaded_data(self, game_data):
        """This is the main function. Here we have several cases.
        So first the based stat. As there is 4 stats for each in order to compute the final stat, they are stored in a list of size 4.
        For card, this is the ID for the different case: DROP, MOD, RARE_MOD
        There is common value of size 1, just raw value.
        % case with specific compute
        Elem and status have specific computation
        Devour is a set of ID for Low, medium, High
        Abilities
        """
        for el in game_data.LIST_DATA:
            raw_data_selected = self.file_raw_data[self.pointer_data_start + el['offset']:  self.pointer_data_start + el['offset'] + el['size']]
            if el['name'] in (game_data.stat_values + ['card', 'devour']):
                value = list(raw_data_selected)

            elif el['name'] in ['med_lvl', 'high_lvl', 'extra_xp', 'xp', 'ap']:
                value = int.from_bytes(raw_data_selected)

            elif el['name'] in ['low_lvl_mag', 'med_lvl_mag', 'high_lvl_mag', 'low_lvl_mug', 'med_lvl_mug', 'high_lvl_mug', 'low_lvl_drop', 'med_lvl_drop',
                                'high_lvl_drop']:  # Case with 4 values linked to 4 IDs
                list_data = list(raw_data_selected)
                value = []
                for i in range(0, el['size'] - 1, 2):
                    value.append({'ID': list_data[i], 'value': list_data[i + 1]})
            elif el['name'] in ['mug_rate', 'drop_rate']:  # Case with %
                value = int.from_bytes(raw_data_selected) * 100 / 255
            elif el['name'] in ['elem_def']:  # Case with elem
                value = list(raw_data_selected)
                for i in range(el['size']):
                    value[i] = 900 - value[i] * 10  # Give percentage
            elif el['name'] in ['abilities_low', 'abilities_med', 'abilities_high']:
                list_data = list(raw_data_selected)
                value = []
                for i in range(0, el['size'] - 1, 4):
                    value.append({'type': list_data[i], 'animation': list_data[i + 1], 'id': int.from_bytes(list_data[i + 2:i + 4], el['byteorder'])})
            elif el['name'] in ['status_def']:  # Case with elem
                value = list(raw_data_selected)
                for i in range(el['size']):
                    value[i] = value[i] - 100  # Give percentage, 155 means immune.
            else:
                value = "ERROR UNEXPECTED VALUE"

            self.data.append({'name': el['name'], 'value': value, 'pretty_name': el['pretty_name']})

        self.__analyze_battle_section(game_data)

    def write_data_to_file(self, game_data, path):
        # First copy original file
        full_dest_path = os.path.join(path, self.origin_file_name)

        # Then load file (python make it difficult to directly modify files)
        self.load_file_data(full_dest_path, game_data)
        self.analyse_loaded_data(game_data)

        # Then modify loaded file
        for el in self.data:
            if el['name'] not in ['combat_text']:  # Combat txt handled differently
                property_elem = [x for ind, x in enumerate(game_data.LIST_DATA) if x['name'] == el['name']][0]
            if el['name'] in (game_data.stat_values + ['card', 'devour']):  # List
                value_to_set = bytes(el['value'])
            elif el['name'] in ['med_lvl', 'high_lvl', 'extra_xp', 'xp', 'ap']:
                value_to_set = el['value'].to_bytes()
            elif el['name'] in ['low_lvl_mag', 'med_lvl_mag', 'high_lvl_mag', 'low_lvl_mug', 'med_lvl_mug', 'high_lvl_mug', 'low_lvl_drop', 'med_lvl_drop',
                                'high_lvl_drop']:  # Case with 4 values linked to 4 IDs
                value_to_set = []
                for el2 in el['value']:
                    value_to_set.append(el2['ID'])
                    value_to_set.append(el2['value'])
                value_to_set = bytes(value_to_set)
            elif el['name'] in ['mug_rate', 'drop_rate']:  # Case with %
                value_to_set = round((el['value'] * 255 / 100)).to_bytes()
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
            elif el['name'] in game_data.ABILITIES_HIGHNESS_ORDER:
                value_to_set = bytearray()
                for el2 in el['value']:
                    value_to_set.extend(el2['type'].to_bytes())
                    value_to_set.extend(el2['animation'].to_bytes())
                    value_to_set.extend(el2['id'].to_bytes(2, property_elem['byteorder']))
                value_to_set = bytes(value_to_set)
            elif el['name'] in ['combat_text']:  # Special case for text as the value change for each text
                value_to_set = None
                value_battle = bytearray()
                for str_battle in el['value']:
                    value_battle.extend(game_data.translate_str_to_hex(str_battle))
                    value_battle.extend([0])
                self.file_raw_data[self.pointer_battle_script_data_start + self.text_subsection_offset:
                                   self.pointer_battle_script_data_start + self.text_subsection_offset + len(value_battle)] = value_battle
            if value_to_set:
                self.file_raw_data[self.pointer_data_start + property_elem['offset']:
                                   self.pointer_data_start + property_elem['offset'] + property_elem['size']] = value_to_set
            value_to_set = None

        # Write back on file
        with open(full_dest_path, "wb") as f:
            f.write(self.file_raw_data)
