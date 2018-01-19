__author__ = 'Антон'
import json

import stations

ROOT = "http://online.ettu.ru"


class Data:
    """
    База данных, хранящяя список остановок
    """
    def __init__(self):
        try:
            self.load()
        except FileNotFoundError:
            self.files = []

    def save(self):
        with open("data.db", "w") as txt:
            txt.writelines(json.dumps(self.files))

    def load(self):
        with open("data.db") as txt:
            self.files = json.load(txt)

    def update(self):
        self.files = stations.get_stations(ROOT)