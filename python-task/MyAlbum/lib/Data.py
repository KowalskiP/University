__author__ = 'kowalski'
import json

from mutagenx.easyid3 import EasyID3

from audio.ffmpeg import checksum
from audio.fingerprinting import calc_fp

class MusicEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, MusicFile):
            return [o.file_name, o.link, o.artist, o.title, o.genre,
                    o.hashes, o.fingerprints]
        return json.JSONEncoder.default(self, o)

class DataBase:
    def __init__(self):
        try:
            self.loadDB()
        except FileNotFoundError:
            self.filenames = []
            self.music_file_list = []
            self.fp_dict = {}


    def saveDB(self):
        with open("lib/filenames.db", 'w') as txt:
            json.dump(self.filenames, txt)
        with open("lib/musicfiles.db", 'w') as txt:
            json.dump(self.music_file_list, txt, cls=MusicEncoder)
        with open("lib/fpdict.db", 'w') as txt:
            json.dump(self.fp_dict, txt)

    def loadDB(self):
        with open("lib/filenames.db") as txt:
            self.filenames = json.load(txt)
            # print(self.filenames)
        with open("lib/musicfiles.db") as txt:
            temp = json.load(txt)
            self.music_file_list = []
            for i in temp:
                self.music_file_list.append(MusicFile(i[0],i[1],i[2],i[3],
                                                i[4],i[5],i[6]))
            # print(self.music_file_list)
        with open("lib/fpdict.db") as txt:
            self.fp_dict = json.load(txt)
            # print(self.fp_dict)


class MusicFile:
    def __init__(self, file_name, link=None, artist=None, title=None,
                 genre=None, hashes=None, fp=None):
        self.file_name = file_name
        self.link = link
        self.artist = artist
        self.title = title
        self.genre = genre
        self.hashes = hashes
        self.fingerprints = fp
        if not (self.artist or self.title or self.genre):
            self.read_mp3_tags()
        if not self.hashes:
            self.get_hashes()
        if not self.fingerprints:
            self.get_fingerprints()

    def read_mp3_tags(self,):
        data = EasyID3(self.file_name)
        try:
            self.artist = data["artist"][0]
        except KeyError:
            self.artist = ''
        try:
            self.title = data["title"][0]
        except KeyError:
            self.title = ''
        try:
            self.genre = data["genre"][0]
        except KeyError:
            self.genre = ''

    def get_hashes(self):
        self.hashes = checksum(self.file_name)

    def get_fingerprints(self):
        self.fingerprints = calc_fp(self.file_name)

    def __str__(self):
        return str([str(self.file_name), str(self.link), str(self.artist),
                    str(self.title), str(self.genre), str(self.hashes),
                    str(self.fingerprints)])

if __name__ == "__main__":
    # a = MusicFile("/home/kowalski/PycharmProjects/TASK/MyAlbum/mp3/ACDC.mp3"
    #               "", 1, 1, 1, 1, 1, 1)
    # print(a)
    d = DataBase()
    print(d.filenames)
    print(d.fp_dict)
    print(type(d.music_file_list[1]))