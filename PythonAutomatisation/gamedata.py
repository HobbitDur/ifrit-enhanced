import os


class GameData():
    USEFUL_DATA_POINTER = {'offset': 0x1C, 'size': 4, 'byteorder': 'little'}
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
    CARD_OBTAIN_ORDER = ['DROP', 'MOD', 'RARE_MOD']
    MISC_ORDER = ['med_lvl', 'high_lvl', 'extra_xp', 'xp', 'mug_rate', 'drop_rate', 'ap']
    RESOURCE_FOLDER = "Resources"

    def __init__(self):
        self.devour_values = []
        self.card_values = []
        self.magic_values = []
        self.item_values = []
        self.status_values = []
        self.magic_type_values = []
        self.stat_values = []

    def load_all(self):
        self.load_card_data(os.path.join(self.RESOURCE_FOLDER, "card.txt"))
        self.load_devour_data(os.path.join(self.RESOURCE_FOLDER, "devour.txt"))
        self.load_magic_data(os.path.join(self.RESOURCE_FOLDER, "magic.txt"))
        self.load_item_data(os.path.join(self.RESOURCE_FOLDER, "item.txt"))
        self.load_status_data(os.path.join(self.RESOURCE_FOLDER, "status.txt"))
        self.load_magic_type_data(os.path.join(self.RESOURCE_FOLDER, "magic_type.txt"))
        self.load_stat_data(os.path.join(self.RESOURCE_FOLDER, "stat.txt"))

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
    def load_status_data(self, file):
        with (open(file, "r") as f):
            self.status_values = f.read().split('\n')
    def load_magic_type_data(self, file):
        with (open(file, "r") as f):
            self.magic_type_values = f.read().split('\n')
    def load_stat_data(self, file):
        with (open(file, "r") as f):
            self.stat_values = f.read().split('\n')

