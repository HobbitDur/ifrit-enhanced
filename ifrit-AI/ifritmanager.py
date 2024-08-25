from dataclasses import dataclass
from enum import Enum

from ennemy import Ennemy
from gamedata import GameData

@dataclass
class Condition:
    subject_id: int
    left_subject: str
    left_param: list
    comparator: str
    right_subject: str
    right_param: list
    jump: list
    debug: int

class IfritManager():
    COMPARATOR_LIST = ['⩵', '<', '>', '≠', '≤', '≥']
    def __init__(self):
        self.game_data = GameData()
        self.game_data.load_all()
        self.ennemy = Ennemy(self.game_data)
        self.ai_data = []
    def add_condition(self, index):
        pass
        #op_code = [0, 0, 0, 0, 0, 0, 0]
        #data = self.ennemy.__op_02_analysis(op_code, self.game_data)
        #self.ai_lines.insert(index, Condition(data[1], data[2], data[6], data[3], data[4], data[7], data[8], data[9]))

    def init_from_file(self, file_path):
        self.ennemy.load_file_data(file_path, self.game_data)
        self.ennemy.analyse_loaded_data(self.game_data, True)
        self.ai_data = self.ennemy.battle_script_data['ia_data']

