import os


class GameData():
    DATA_POINTER_INFO_STAT = {'offset': 0x1C, 'size': 4, 'byteorder': 'little'}
    COM127_POINTER_OFFSET = 4
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
    EXTRA_XP_DATA = {'offset': 0x100, 'size': 1, 'byteorder': 'big', 'name': 'extra_xp',
                     'pretty_name': 'Extra XP'}  # Seems the size was intended for 2 bytes, but in practice no monster has a value > 255
    XP_DATA = {'offset': 0x102, 'size': 1, 'byteorder': 'big', 'name': 'xp',
               'pretty_name': 'XP'}  # Seems the size was intended for 2 bytes, but in practice no monster has a value > 255
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
    ABILITIES_LOW_DATA = {'offset': 0x34, 'size': 64, 'byteorder': 'little', 'name': 'abilities_low', 'pretty_name': 'Abilities Low Level'}
    ABILITIES_MED_DATA = {'offset': 0x74, 'size': 64, 'byteorder': 'little', 'name': 'abilities_med', 'pretty_name': 'Abilities Medium Level'}
    ABILITIES_HIGH_DATA = {'offset': 0xB4, 'size': 64, 'byteorder': 'little', 'name': 'abilities_high', 'pretty_name': 'Abilities High Level'}

    DATA_POINTER_BATTLE_SCRIPT = {'offset': 0x20, 'size': 4, 'byteorder': 'little'}
    DATA_POINTER_SUBSECTION_OFFSET = {'offset': 0x0C, 'size': 4, 'byteorder': 'little'}
    DATA_POINTER_TEXT_OFFSET = {'offset': 0x08, 'size': 4, 'byteorder': 'little'}
    BATTLE_TEXT_OFFSET = {'offset': 0x00, 'size': 2, 'byteorder': 'little'}

    LIST_DATA = [HP_DATA, STR_DATA, VIT_DATA, MAG_DATA, SPR_DATA, SPD_DATA, EVA_DATA, MED_LVL_DATA, HIGH_LVL_DATA, EXTRA_XP_DATA, XP_DATA, LOW_LVL_MAG_DATA,
                 MED_LVL_MAG_DATA, HIGH_LVL_MAG_DATA, LOW_LVL_MUG_DATA, MED_LVL_MUG_DATA,
                 HIGH_LVL_MUG_DATA, LOW_LVL_DROP_DATA, MED_LVL_DROP_DATA, HIGH_LVL_DROP_DATA, MUG_RATE_DATA, DROP_RATE_DATA, AP_DATA, ELEM_DEF_DATA,
                 STATUS_DEF_DATA, CARD_DATA, DEVOUR_DATA, ABILITIES_LOW_DATA, ABILITIES_MED_DATA, ABILITIES_HIGH_DATA]
    CARD_OBTAIN_ORDER = ['DROP', 'MOD', 'RARE_MOD']
    MISC_ORDER = ['med_lvl', 'high_lvl', 'extra_xp', 'xp', 'mug_rate', 'drop_rate', 'ap']
    ABILITIES_HIGHNESS_ORDER = ['abilities_low', 'abilities_med', 'abilities_high']
    RESOURCE_FOLDER = "Resources"
    CHARACTER_LIST = ["Squall", "Zell", "Irvine", "Quistis", "Rinoa", "Selphie", "Seifer", "Edea", "Laguna", "Kiros", "Ward", "Angelo",
                      "Griever", "Boko"]
    COLOR_LIST = ["Darkgrey", "Grey", "Yellow", "Red", "Green", "Blue", "Purple", "White",
                  "DarkgreyBlink", "GreyBlink", "YellowBlink", "RedBlink", "GreenBlink", "BlueBlink", "PurpleBlink", "WhiteBlink"]
    LOCATION_LIST = ["Galbadia", "Esthar", "Balamb", "Dollet", "Timber", "Trabia", "Centra", "Horizon"]

    def __init__(self):
        self.devour_values = []
        self.card_values = []
        self.magic_values = {}
        self.item_values = {}
        self.status_values = []
        self.magic_type_values = []
        self.stat_values = []
        self.ennemy_abilities_values = {}
        self.ennemy_abilities_type_values = {}
        self.translate_hex_to_str_table = []
        self.__init_hex_to_str_table()

    def __init_hex_to_str_table(self):
        with open("Resources/sysfnt.txt", "r", encoding="utf-8") as localize_file:
            self.translate_hex_to_str_table = localize_file.read()
            self.translate_hex_to_str_table = self.translate_hex_to_str_table.replace(',",",',
                                                                                      ',";;;",')  # Handling the unique case of a "," character (which is also a separator)
            self.translate_hex_to_str_table = self.translate_hex_to_str_table.replace('\n', '')
            self.translate_hex_to_str_table = self.translate_hex_to_str_table.split(',')
            for i in range(len(self.translate_hex_to_str_table)):
                self.translate_hex_to_str_table[i] = self.translate_hex_to_str_table[i].replace(';;;', ',')
                if self.translate_hex_to_str_table[i].count('"') == 2:
                    self.translate_hex_to_str_table[i] = self.translate_hex_to_str_table[i].replace('"', '')

    def translate_str_to_hex(self, string):
        c = 0
        str_size = len(string)
        encode_list = []
        while c < str_size:
            char = string[c]
            if char == '\n':  # \n{NewPage}\n,\n
                if '{NewPage}' in string[c + 1:c + 10]:
                    encode_list.append(0x01)
                    c += 10
                else:
                    encode_list.append(0x02)
                    c += 1
                continue
            elif char == '{':
                rest = string[c+1:]
                index_next_bracket = rest.find('}')
                if index_next_bracket != -1:
                    substring = rest[:index_next_bracket]
                    if substring in self.CHARACTER_LIST:  # {name}
                        index_list = self.CHARACTER_LIST.index(substring)
                        if index_list < 11:
                            encode_list.extend([0x03, 0x30 + index_list])
                        elif index_list == 11:
                            encode_list.extend([0x03, 0x40])
                        elif index_list == 12:
                            encode_list.extend([0x03, 0x50])
                        elif index_list == 13:
                            encode_list.extend([0x03, 0x60])
                    elif substring in self.COLOR_LIST:  # {Color}
                        index_list = self.COLOR_LIST.index(substring)
                        encode_list.extend([0x06, 0x20 + index_list])
                    elif substring in self.LOCATION_LIST:  # {Location}
                        index_list = self.LOCATION_LIST.index(substring)
                        encode_list.extend([0x0e, 0x20 + index_list])
                    elif 'Var' in substring:
                        if len(substring) == 5:
                            if 'b' in substring:  # {Varb0}
                                encode_list.extend([0x04, int(substring[-1]) + 0x40])
                            else:  # {Var00}
                                encode_list.extend([0x04, int(substring[-1]) + 0x30])
                        else:  # {Var0}
                            encode_list.extend([0x04, int(substring[-1]) + 0x20])
                    elif 'Wait' in substring:  # {Wait000}
                        encode_list.extend([0x09, int(substring[-1]) + 0x20])
                    elif 'Jp' in substring:  # {Jp000}
                        encode_list.extend([0x1c, int(substring[-1]) + 0x20])
                    elif '{' + substring + '}' in self.translate_hex_to_str_table:  # {} at end of sysfnt
                        encode_list.append(self.translate_hex_to_str_table[self.translate_hex_to_str_table.index('{' + substring + '}')])
                    elif 'x' in substring and len(substring) == 5:  # {xffff}
                        encode_list.extend([int(substring[1:3], 16), int(substring[3:5], 16)])
                    elif 'x' in substring and len(substring) == 3:  # {xff}
                        encode_list.append(int(substring[1:3], 16))
                    c += len(substring) + 2
                    continue
            encode_list.append(self.translate_hex_to_str_table.index(char))
            c += 1
            # Jp ?
        return encode_list



    def translate_hex_to_str(self, hex_list):
        str = ""
        i = 0
        hex_size = len(hex_list)
        while i < hex_size:
            hex_val = hex_list[i]

            if hex_val == 0x00:
                pass
            elif hex_val in [0x01, 0x02]:
                str += self.translate_hex_to_str_table[hex_val]
            elif hex_val == 0x03:  # {Name}
                i += 1
                if i < hex_size:
                    hex_val = hex_list[i]
                    if hex_val >= 0x30 and hex_val <= 0x3a:
                        str += '{' + self.CHARACTER_LIST[hex_val - 0x30] + '}'
                    elif hex_val == 0x40:
                        str += '{' + self.CHARACTER_LIST[11] + '}'
                    elif hex_val == 0x50:
                        str += '{' + self.CHARACTER_LIST[12] + '}'
                    elif hex_val == 0x60:
                        str += '{' + self.CHARACTER_LIST[13] + '}'
                    else:
                        str += "{{x03{:02x}}}".format(hex_val)
                else:
                    str += "{x03}"
            elif hex_val == 0x04:  # {Var0}, {Var00} et {Varb0}
                i += 1
                if hex_val < hex_size:
                    hex_val = hex_list[i]
                    if hex_val >= 0x20 and i <= 0x27:
                        str += "{{Var{:02x}}}".format(hex_val - 0x20)
                    elif hex_val >= 0x30 and i <= 0x37:
                        str += "{{Var0{:02x}}}".format(hex_val - 0x30)
                    elif hex_val >= 0x40 and i <= 0x47:
                        str += "{{Varb{:02x}}}".format(hex_val - 0x40)
                    else:
                        str += "{{x04{:02x}}}".format(hex_val)

                else:
                    str += "{x04}"
            elif hex_val == 0x06:  # {Color}
                i += 1
                if i < hex_size:
                    hex_val = hex_list[i]
                    if hex_val >= 0x20 and hex_val <= 0x2f:
                        str += '{' + self.COLOR_LIST[hex_val - 0x20] + '}'
                    else:
                        str += "{{x06{:02x}}}".format(hex_val)
                else:
                    str += "{x06}"
            elif hex_val == 0x09:  # {Wait000}
                i += 1
                if i < hex_size:
                    hex_val = hex_list[i]
                    if hex_val >= 0x20:
                        str += "{{Wait{:03}}}".format(hex_val - 0x20)
                    else:
                        str += "{{x09{:02x}}}".format(hex_val)
                else:
                    str += "{x06}"
            elif hex_val == 0x0e:  # {Location}
                i += 1
                if i < hex_size:
                    hex_val = hex_list[i]
                    if hex_val >= 0x20 and hex_val <= 0x27:
                        str += '{' + self.LOCATION_LIST[hex_val - 0x20] + '}'
                    else:
                        str += "{{x0e{:02x}}}".format(hex_val)
                else:
                    str += "{x0e}"
            elif hex_val >= 0x019 and hex_val <= 0x1b:  # jp19, jp1a, jp1b
                i += 1
                if i < len(hex_list):
                    old_hex_val = hex_val
                    hex_val = hex_list[i]
                    if hex_val >= 0x20:
                        character = None  # To be changed, caract(index, oldIndex-0x18);
                    else:
                        character = None
                    if not character:
                        character = "{{x{:02x}{:02x}}}".format(old_hex_val, hex_val)
                    str += character
                else:
                    str += "{{x{:02x}}}".format(hex_val)
            elif hex_val == 0x1c:  # addJp
                i += 1
                if i < hex_size:
                    hex_val = hex_list[i]
                    if hex_val >= 0x20:
                        str += "{{Jp{:03}}}".format(hex_val - 0x20)
                    else:
                        str += "{{x1c{:02x}}}".format(hex_val)
                else:
                    str += "{x1c}"
            elif hex_val >= 0x05 and hex_val <= 0x1f:
                i += 1
                if i < hex_size:
                    str += "{{x{:02x}{:02x}}}".format(hex_val, hex_list[i])
                else:
                    str += "{{x{:02x}}}".format(hex_val)
            else:
                character = self.translate_hex_to_str_table[hex_val]  # To be done
                if not character:
                    character = "{{x{:02x}}}".format(hex_val)
                str += character
            i += 1
        return str

    def load_all(self):
        self.load_card_data(os.path.join(self.RESOURCE_FOLDER, "card.txt"))
        self.load_devour_data(os.path.join(self.RESOURCE_FOLDER, "devour.txt"))
        self.load_magic_data(os.path.join(self.RESOURCE_FOLDER, "magic.txt"))
        self.load_item_data(os.path.join(self.RESOURCE_FOLDER, "item.txt"))
        self.load_status_data(os.path.join(self.RESOURCE_FOLDER, "status.txt"))
        self.load_magic_type_data(os.path.join(self.RESOURCE_FOLDER, "magic_type.txt"))
        self.load_stat_data(os.path.join(self.RESOURCE_FOLDER, "stat.txt"))
        self.load_ennemy_abilities_data(os.path.join(self.RESOURCE_FOLDER, "ennemy_abilities.txt"))
        self.load_ennemy_abilities_type_data(os.path.join(self.RESOURCE_FOLDER, "ennemy_abilities_type.txt"))

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
            file_split = f.read().split('\n')
            for el_split in file_split:
                self.magic_values[int(el_split.split('<')[0], 16)] = {'name': el_split.split('<')[1],
                                                                      'ref': str(int(el_split.split('<')[0], 16)) + ":" + el_split.split('<')[1]}

    def load_item_data(self, file):
        with (open(file, "r") as f):
            file_split = f.read().split('\n')
            for el_split in file_split:
                self.item_values[int(el_split.split('<')[0], 16)] = {'name': el_split.split('<')[1],
                                                                     'ref': str(int(el_split.split('<')[0], 16)) + ":" + el_split.split('<')[1]}

    def load_status_data(self, file):
        with (open(file, "r") as f):
            self.status_values = f.read().split('\n')

    def load_magic_type_data(self, file):
        with (open(file, "r") as f):
            self.magic_type_values = f.read().split('\n')

    def load_stat_data(self, file):
        with (open(file, "r") as f):
            self.stat_values = f.read().split('\n')

    def load_ennemy_abilities_data(self, file):
        with (open(file, "r") as f):
            file_split = f.read().split('\n')
            for el_split in file_split:
                self.ennemy_abilities_values[int(el_split.split('>')[0])] = {'name': el_split.split('>')[1],
                                                                             'ref': el_split.split('>')[0] + ":" + el_split.split('>')[1]}

    def load_ennemy_abilities_type_data(self, file):
        with (open(file, "r") as f):
            file_split = f.read().split('\n')
            for el_split in file_split:
                self.ennemy_abilities_type_values[int(el_split.split('>')[0])] = {'name': el_split.split('>')[1],
                                                                                  'ref': el_split.split('>')[0] + ":" + el_split.split('>')[1]}
