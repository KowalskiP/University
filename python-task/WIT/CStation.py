__author__ = 'Антон'


class Station:
    """
    Класс, хранящий информацию о станциии текущем положение транспорта
    """
    def __init__(self, typ, trans, img, page):
        self.typ = typ
        self.trans = trans
        self.img = img
        self.page = page

    def __str__(self):
        return str([self.typ, self.trans, self.img, self.page])