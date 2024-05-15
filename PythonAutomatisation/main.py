import csv
import glob

import xlsxwriter
from xlsxwriter.exceptions import DuplicateWorksheetName

UNPACKED_LENGTH_OFFSET = 0
LOCATION_OFFSET = 4
LZS_OFFSET = 8
BFI_INC = 12
DEFAULT_FILE_COUNT = 853
DEFAULT_INTERNAL_PATH = "c:\\ff8\\data\\eng\\battle\\"
BATTLE_FS = "battle.fs"
BATTLE_FL = "battle.fl"
BATTLE_FI = "battle.fi"
UNPACK_LOC = "Battle Files"

USEFUL_DATA_POINTER = {'offset': 0x1C, 'size': 4, 'byteorder': 'little'}
c0m127pointerOffset = 4
NAME_DATA = {'offset': 0x00, 'size': 24, 'byteorder': 'big', 'name': 'name', 'pretty_name': 'Name'}
HP_DATA = {'offset': 0x18, 'size': 4, 'byteorder': 'big', 'name': 'hp', 'pretty_name': 'HP'}
STR_DATA = {'offset': 0x1C, 'size': 4, 'byteorder': 'big', 'name': 'str', 'pretty_name': 'STR'}
VIT_DATA = {'offset': 0x20, 'size': 4, 'byteorder': 'big', 'name': 'vit', 'pretty_name': 'VIT'}
MAG_DATA = {'offset': 0x24, 'size': 4, 'byteorder': 'big', 'name': 'mag', 'pretty_name': 'MAG'}
SPR_DATA = {'offset': 0x28, 'size': 4, 'byteorder': 'big', 'name': 'spr', 'pretty_name': 'SPR'}
SPD_DATA = {'offset': 0x2C, 'size': 4, 'byteorder': 'big', 'name': 'spd', 'pretty_name': 'SPD'}
EVA_DATA = {'offset': 0x30, 'size': 4, 'byteorder': 'big', 'name': 'eva', 'pretty_name': 'EVA'}
MED_LVL_DATA = {'offset': 0xF4, 'size': 1, 'byteorder': 'big', 'name': 'med_lvl', 'pretty_name': 'Medium level'}
HIGH_LVL_DATA = {'offset': 0xF5, 'size': 1, 'byteorder': 'big', 'name': 'high_lvl', 'pretty_name': 'High Level'}
EXTRA_XP_DATA = {'offset': 0x100, 'size': 1, 'byteorder': 'big', 'name': 'extra_xp', 'pretty_name': 'Extra XP'}  # Seems the size was intended for 2 bytes, but in practice no monster has a value > 255
XP_DATA = {'offset': 0x102, 'size': 1, 'byteorder': 'big', 'name': 'xp', 'pretty_name': 'XP'}  # Seems the size was intended for 2 bytes, but in practice no monster has a value > 255
LOW_LVL_MAG_DATA = {'offset': 0x104, 'size': 8, 'byteorder': 'big', 'name': 'low_lvl_mag', 'pretty_name': 'Low level Mag draw'}
MED_LVL_MAG_DATA = {'offset': 0x10C, 'size': 8, 'byteorder': 'big', 'name': 'med_lvl_mag', 'pretty_name': 'Medium level Mag draw'}
HIGH_LVL_MAG_DATA = {'offset': 0x114, 'size': 8, 'byteorder': 'big', 'name': 'high_lvl_mag', 'pretty_name': 'High level Mag draw'}
LOW_LVL_MUG_DATA = {'offset': 0x11C, 'size': 8, 'byteorder': 'big', 'name': 'low_lvl_mug', 'pretty_name': 'Low level Mug draw'}
MED_LVL_MUG_DATA = {'offset': 0x124, 'size': 8, 'byteorder': 'big', 'name': 'med_lvl_mug', 'pretty_name': 'Medium level Mug draw'}
HIGH_LVL_MUG_DATA = {'offset': 0x12C, 'size': 8, 'byteorder': 'big', 'name': 'high_lvl_mug', 'pretty_name': 'High level Mug draw'}
LOW_LVL_DROP_DATA = {'offset': 0x134, 'size': 8, 'byteorder': 'big', 'name': 'low_lvl_drop', 'pretty_name': 'Low level drop draw'}
MED_LVL_DROP_DATA = {'offset': 0x13C, 'size': 8, 'byteorder': 'big', 'name': 'med_lvl_drop', 'pretty_name': 'Medium level drop draw'}
HIGH_LVL_DROP_DATA = {'offset': 0x144, 'size': 8, 'byteorder': 'big', 'name': 'high_lvl_drop', 'pretty_name': 'High level drop draw'}
MUG_RATE_DATA = {'offset': 0x14C, 'size': 1, 'byteorder': 'big', 'name': 'mug_rate', 'pretty_name': 'Mug rate %'}
DROP_RATE_DATA = {'offset': 0x14D, 'size': 1, 'byteorder': 'big', 'name': 'drop_rate', 'pretty_name': 'Drop rate %'}
AP_DATA = {'offset': 0x14F, 'size': 1, 'byteorder': 'big', 'name': 'ap', 'pretty_name': 'AP'}
ELEM_DEF_DATA = {'offset': 0x160, 'size': 8, 'byteorder': 'big', 'name': 'elem_def', 'pretty_name': 'Elemental def'}
STATUS_DEF_DATA = {'offset': 0x168, 'size': 20, 'byteorder': 'big', 'name': 'status_def', 'pretty_name': 'Status def'}
CARD_DATA = {'offset': 0xF8, 'size': 3, 'byteorder': 'big', 'name': 'card', 'pretty_name': 'Card'}
DEVOUR_DATA = {'offset': 0xFB, 'size': 3, 'byteorder': 'big', 'name': 'devour', 'pretty_name': 'Devour'}
ABILITIES_DATA = {'offset': 0x34, 'size': 48, 'byteorder': 'big', 'name': 'abilities', 'pretty_name': 'Abilities'}

LIST_DATA = [HP_DATA, STR_DATA, VIT_DATA, MAG_DATA, SPR_DATA, SPD_DATA, EVA_DATA, MED_LVL_DATA, HIGH_LVL_DATA, EXTRA_XP_DATA, XP_DATA, LOW_LVL_MAG_DATA, MED_LVL_MAG_DATA, HIGH_LVL_MAG_DATA, LOW_LVL_MUG_DATA, MED_LVL_MUG_DATA,
             HIGH_LVL_MUG_DATA, LOW_LVL_DROP_DATA, MED_LVL_DROP_DATA, HIGH_LVL_DROP_DATA, MUG_RATE_DATA, DROP_RATE_DATA, AP_DATA, ELEM_DEF_DATA, STATUS_DEF_DATA, CARD_DATA, DEVOUR_DATA, ABILITIES_DATA]
MAGIC_ORDER = ['Fire', 'Ice', 'Thunder', 'Earth', 'Bio', 'Water', 'Wind', 'Holy']
STATUS_ORDER = ['Death', 'Poison', 'Petrify', 'Blind', 'Mute', 'Bersk', 'Zombie', 'Sleep', 'Haste', 'Slow', 'Stop', 'Regen', 'Reflect', 'Doom', 'Sub-petrify', 'float', 'Drain', 'Confu', 'Expulsion', 'Gravity']
CARD_OBTAIN_ORDER = ['DROP', 'MOD', 'RARE_MOD']
FILE_MONSTER = glob.glob("OriginalFiles/*.dat")


class GameData():
    def __init__(self):
        self.devour_values = []
        self.card_values = []
        self.magic_values = []
        self.item_values = []

    def load_devour_data(self, file):
        with (open(file, "r") as f):
            self.devour_values = f.read().split('\n')
            for i in range(len(self.devour_values)):
                self.devour_values[i] = self.devour_values[i].split('<')[1]

    def load_card_data(self, file):
        with (open(file, "r") as f):
            self.card_values = f.read().split('\n')
            for i in range(len(self.card_values)):
                self.card_values[i] = self.card_values[i].split('<')[1]

    def load_magic_data(self, file):
        with (open(file, "r") as f):
            self.magic_values = f.read().split('\n')
            for i in range(len(self.magic_values)):
                self.magic_values[i] = self.magic_values[i].split('<')[1]

    def load_item_data(self, file):
        with (open(file, "r") as f):
            self.item_values = f.read().split('\n')
            for i in range(len(self.item_values)):
                self.item_values[i] = self.item_values[i].split('<')[1]


class Ennemy():

    def __init__(self, game_data):
        self.name = ""
        self.file_data = []
        self.file_data_byte_array = bytearray()
        self.data = []
        self.pointer_data_start = 0
        self.game_data = game_data

    def __repr__(self):
        return "Name: {} \nData:{}".format(self.name, self.data)

    def load_file_data(self, file):
        with open(file, "rb") as f:
            while el := f.read(1):
                self.file_data.append(el)
                self.file_data_byte_array.extend(el)

        # First we get the "pointer value", which is the pointer at which the file data start.
        if '123' in file: # Weird case, the 123 file is a garbage anyway but this is to avoid error
            data_pointer = 4
        else:
            data_pointer = USEFUL_DATA_POINTER['offset']
        self.pointer_data_start = int.from_bytes(self.file_data_byte_array[data_pointer:data_pointer + USEFUL_DATA_POINTER['size']], USEFUL_DATA_POINTER["byteorder"])

    def load_name(self):
        # The name is a bit more tricky. A specific conversion needs to happen, that depends on the localization. The translation is done in a text file.
        name_data = self.file_data_byte_array[self.pointer_data_start + NAME_DATA['offset']:  self.pointer_data_start + NAME_DATA['offset'] + NAME_DATA['size']]
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

    def get_stat(self):
        """This is the main function. Here we have several cases.
        So first the based stat. As there is 4 stats for each in order to compute the final stat, they are stored in a list of size 4.
        For card, this is the ID for the different case: DROP, MOD, RARE_MOD
        There is common value of size 1, just raw value.
        % case with specific compute
        Elem and status have specific computation
        Devour is a set of ID for Low, medium, High
        Abilities TODO
        """
        for el in LIST_DATA:
            pointer_data_start = self.file_data_byte_array[self.pointer_data_start + el['offset']:  self.pointer_data_start + el['offset'] + el['size']]
            if el['name'] in ['hp', 'str', 'vit', 'mag', 'spr', 'spd', 'eva', 'card', 'devour', 'abilities']:
                value = list(pointer_data_start)

            elif el['name'] in ['med_lvl', 'high_lvl', 'extra_xp', 'xp', 'ap']:
                value = int.from_bytes(pointer_data_start)

            elif el['name'] in ['low_lvl_mag', 'med_lvl_mag', 'high_lvl_mag', 'low_lvl_mug', 'med_lvl_mug', 'high_lvl_mug', 'low_lvl_drop', 'med_lvl_drop', 'high_lvl_drop']:  # Case with 4 values linked to 4 IDs
                list_data = list(pointer_data_start)
                value = []
                for i in range(0, el['size'] - 1, 2):
                    value.append({'ID': list_data[i], 'value': list_data[i + 1]})

            elif el['name'] in ['mug_rate', 'drop_rate']:  # Case with %
                value = int.from_bytes(pointer_data_start) * 100 / 256

            elif el['name'] in ['elem_def']:  # Case with elem
                value = list(pointer_data_start)
                for i in range(el['size']):
                    value[i] = 900 - value[i] * 10  # Give percentage

            elif el['name'] in ['status_def']:  # Case with elem
                value = list(pointer_data_start)
                for i in range(el['size']):
                    value[i] = value[i] - 100  # Give percentage, 155 means immune.

            else:
                value = "ERROR UNEXPECTED VALUE"

            self.data.append({'name': el['name'], 'value': value, 'pretty_name': el['pretty_name']})


def export_to_xlsx(ennemy_list):

    workbook = xlsxwriter.Workbook("OutputFiles/ifrit.xlsx")
    tab_list = []
    for key, ennemy in ennemy_list.items():
        print(ennemy)
        # Excel preparation

        file_name = ennemy.name
        if file_name == '':
            file_name= "Empty"
        while file_name in tab_list:
            file_name += " dub"

        worksheet = workbook.add_worksheet(file_name)

        tab_list.append(file_name)



        # Column position of different "menu"
        column_index = {}
        column_index['stat'] = 0
        column_index['def'] = 6
        column_index['item'] = 9
        column_index['misc'] = 14

        # Style creation
        column_title_style = workbook.add_format({'bold': True, 'border': 1, 'bg_color': '#b2b2b2'})
        bold_style = workbook.add_format({'bold': True})
        border_style = workbook.add_format({'border': 1})
        row_title_style = workbook.add_format({'border': 1, 'bold': True})
        magic_style = workbook.add_format({'border': 1, 'bg_color': '#b8cce4'})
        status_style = workbook.add_format({'border': 1, 'bg_color': '#b9b085'})
        drop_style = workbook.add_format({'border': 1, 'bg_color': '#ccc0da'})
        mug_style = workbook.add_format({'border': 1, 'bg_color': '#7aeca0'})
        title_magic_style = workbook.add_format({'bold': True, 'border': 1, 'bg_color': '#b8cce4'})
        title_status_style = workbook.add_format({'bold': True, 'border': 1, 'bg_color': '#b9b085'})
        title_drop_style = workbook.add_format({'bold': True, 'border': 1, 'bg_color': '#ccc0da'})
        title_mug_style = workbook.add_format({'bold': True, 'border': 1, 'bg_color': '#7aeca0'})

        # Titles
        worksheet.write_row(0, column_index['stat'] + 1, ["Value 1", "Value 2", "Value 3", "Value 4"], cell_format=column_title_style)
        worksheet.write_row(0, column_index['def'], ["Defense name", "% Resistance"], cell_format=column_title_style)
        worksheet.write_row(0, column_index['item'] + 1, ["Low Level", "Medium Level", "High Level"], cell_format=column_title_style)
        worksheet.write_row(0, column_index['misc'], ["Property name", "Value"], cell_format=column_title_style)

        # Index setting
        row_index = {}
        index = {}
        row_index['stat'] = 1
        row_index['def'] = 1
        row_index['item'] = 1
        row_index['misc'] = 1
        index['elem_def'] = 0
        index['status_def'] = 0
        index['draw'] = 1
        index['mug'] = 1
        index['drop'] = 1

        # Filling the Excel
        for el in ennemy.data:
            try: # Due do garbage data, there is a magic ID 233
                column_index['stat'] = 0
                if el['name'] in ['hp', 'str', 'vit', 'mag', 'spr', 'spd', 'eva']:
                    worksheet.write(row_index['stat'], 0, el['pretty_name'], row_title_style)  # Writing title of row
                    column_index['stat'] += 1
                    for el2 in el['value']:
                        worksheet.write(row_index['stat'], column_index['stat'], el2, border_style)
                        column_index['stat'] += 1
                    row_index['stat'] += 1
                elif el['name'] in ['elem_def', 'status_def']:
                    for el2 in el['value']:
                        if el['name'] == 'elem_def':
                            worksheet.write(row_index['def'], column_index['def'], MAGIC_ORDER[index[el['name']]], title_magic_style)
                            worksheet.write(row_index['def'], column_index['def'] + 1, el2, magic_style)
                        elif el['name'] == 'status_def':
                            worksheet.write(row_index['def'], column_index['def'], STATUS_ORDER[index[el['name']]], title_status_style)
                            worksheet.write(row_index['def'], column_index['def'] + 1, el2, status_style)

                        index[el['name']] += 1
                        row_index['def'] += 1
                elif el['name'] in ['med_lvl', 'high_lvl', 'extra_xp', 'xp', 'mug_rate', 'drop_rate', 'ap']:
                    worksheet.write(row_index['misc'], column_index['misc'], el['pretty_name'], row_title_style)
                    worksheet.write(row_index['misc'], column_index['misc'] + 1, el['value'], border_style)
                    row_index['misc'] += 1
                elif el['name'] in ['low_lvl_mag', 'med_lvl_mag', 'high_lvl_mag', 'low_lvl_mug', 'med_lvl_mug', 'high_lvl_mug', 'low_lvl_drop', 'med_lvl_drop', 'high_lvl_drop']:  # Items
                    if 'mag' in el['name']:
                        row_index['item'] = 1
                    elif 'mug' in el['name']:
                        row_index['item'] = 5
                    elif 'drop' in el['name']:
                        row_index['item'] = 9
                    index['draw'] = 0
                    index['mug'] = 0
                    index['drop'] = 0

                    for el2 in el['value']:
                        if 'low' in el['name']:
                            col_index = column_index['item'] + 1
                        elif 'med' in el['name']:
                            col_index = column_index['item'] + 2
                        elif 'high' in el['name']:
                            col_index = column_index['item'] + 3
                        else:  # Should not happen
                            col_index = column_index['item'] + 4
                        if el['name'] in ['low_lvl_mag', 'med_lvl_mag', 'high_lvl_mag']:
                            worksheet.write(row_index['item'], column_index['item'], "Draw {}".format(index['draw']), title_magic_style)
                            index['draw'] += 1
                            worksheet.write(row_index['item'], col_index, ennemy.game_data.magic_values[el2['ID']], magic_style)
                        elif el['name'] in ['low_lvl_mug', 'med_lvl_mug', 'high_lvl_mug']:
                            worksheet.write(row_index['item'], column_index['item'], "Mug {}".format(index['mug']), title_mug_style)
                            index['mug'] += 1
                            worksheet.write(row_index['item'], col_index, ennemy.game_data.item_values[el2['ID']], mug_style)
                        elif el['name'] in ['low_lvl_drop', 'med_lvl_drop', 'high_lvl_drop']:
                            worksheet.write(row_index['item'], column_index['item'], "Drop {}".format(index['drop']), title_drop_style)
                            index['drop'] += 1
                            worksheet.write(row_index['item'], col_index, ennemy.game_data.item_values[el2['ID']], drop_style)
                        row_index['item'] += 1
            except IndexError:
                print("Error on file : {} for monster name: {}".format(key, file_name))
                continue
        worksheet.autofit()
    workbook.close()


if __name__ == "__main__":
    monster = {}
    game_data = GameData()
    game_data.load_card_data("Ressources/card.txt")
    game_data.load_devour_data("Ressources/devour.txt")
    game_data.load_magic_data("Ressources/magic.txt")
    game_data.load_item_data("Ressources/item.txt")

    for file in FILE_MONSTER:
        monster[file] = Ennemy(game_data)
        monster[file].load_file_data(file)
        monster[file].load_name()
        monster[file].get_stat()
    export_to_xlsx(monster)
