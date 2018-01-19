__author__ = 'kowalski'
import os
import shutil
import configparser

import lib.magic as magic
from lib.Data import MusicFile, DataBase
import lib.compare as compare

def magic_determiner(file_name):
        """
        It uses magic module for determine file type
        :param file_name: name of file
        :return: mime type
        """
        try:
            mimetype = str(magic.from_file(file_name))
            return mimetype
        except OSError:
            print("File " + file_name + " not exist.")
            return None


def check_audio_type(mtype):
        """
        Determination of only two types - mp3 and flac
        :param mtype: mime type string
        :return: simplified form of type
        """
        if mtype is not None:
            if str.find(str.lower(mtype), "audio") >= 0:
                if str.find(mtype, "ID3") >= 0:
                    return "mp3"
        else:
            return None


def check_db(db):
    removed_list = []
    for i in db.filenames:
        if not os.path.exists(i):
            removed_list.append(i)
    return removed_list


def get_file_from_dirs(paths, db):
    new_file_list = []
    for p in paths:
        for root, dirs, files in os.walk(p):

            for f in files:
                current_name = os.path.join(root, f)
                # print(current_name)
                if current_name not in db.filenames:
                    try:
                        file_type = check_audio_type(magic_determiner(current_name))
                    except UnicodeEncodeError:
                        continue

                    if file_type == "mp3":
                        db.filenames.append(current_name)
                        aud = MusicFile(current_name)

                        if not compare.check_by_hash(aud, db, new_file_list):
                            db_dict, music_dict = compare.check_by_fp(aud, db,
                                                                     new_file_list)

                            db.fp_dict[aud.file_name] = {}
                            db.fp_dict[aud.file_name].update(db_dict)
                            db.fp_dict[aud.file_name].update(music_dict)

                            for k in db.fp_dict.keys():
                                if k != aud.file_name:
                                    # print(k)
                                    # print(db.fp_dict[k])
                                    db.fp_dict[k].update({aud.file_name:
                                              db.fp_dict[aud.file_name][k]})

                            new_file_list.append(aud)
    return new_file_list

def make_link(current_file_name, new_file_name):
    try:
        os.link(current_file_name, new_file_name)
    except FileNotFoundError:
        if not os.path.exists(os.path.split(new_file_name)[0]):
                os.mkdir(os.path.split(new_file_name)[0])
                os.link(current_file_name, new_file_name)
        elif not os.path.exists(current_file_name):
            print(current_file_name + " removed")
    except FileExistsError as er:
        print("File already exist: "+ er.filename2)

def get_link_name(m_path, prefix, file_name):
    name =''
    for i in prefix:
        if i == "/":
           name += ""
        else:
            name +=i
    return os.path.join(m_path, name, os.path.split(file_name)[1])

def clean_link(db):
    for i in db.music_file_list:
        if os.path.exists(i.link):
            os.remove(i.link)

"""
# def check_with_db(file_list, db):
#     add_files = []
#     for i in file_list:
#         if i not in db.filenames:
#             add_files.append(i)
#     return add_files


# def create_music_file_list(file_list):
#     music_file_list = []
#     for f in file_list:
#         print(f)
#         audio_file = MusicFile(f)
#         music_file_list.append(audio_file)
#     return music_file_list


# def append_music_files(music_list, db):
#     app_list = []
#     l = len(music_list)
#     for i in range(l):
#         m = music_list[i]
#
#
#         if not compare.check_by_hash(m, db, music_list):
#             db_dict, music_dict = compare.check_by_fp(m, db, music_list)
#
#             db.fp_dict[m.file_name] = {}
#             db.fp_dict[m.file_name].update(db_dict)
#             db.fp_dict[m.file_name].update(music_dict)
#             print(db.fp_dict[m.file_name])
#
#             for k in db.fp_dict.keys():
#                 if k != m.file_name:
#                     print('m' + m.file_name)
#                     print('k' + k)
#                     db.fp_dict[k].update({m.file_name:
#                                               db.fp_dict[m.file_name][k]})
#
#             app_list.append(m)
#     return app_list
"""

def clustering(db, m_path, sort_type):
    prefix = []
    for i in db.music_file_list:
        if sort_type == 'Artist':
            i.link = get_link_name(m_path, i.artist, i.file_name)
        elif sort_type == 'Genre':
            i.link = get_link_name(m_path, i.genre, i.file_name)
        elif sort_type == 'None':
            i.link = get_link_name(m_path, '', i.file_name)
        elif sort_type == 'Sim':
            i.link = sim_clust(m_path, i,db,prefix)




def sim_clust(m_path, music_file, db, prefixes):
    add_flag = False
    for add_set in prefixes:

        for file_name in add_set:

            if db.fp_dict[music_file.file_name][file_name] > 50:
                add_set.add(music_file.file_name)
                add_flag = True

                return get_link_name(m_path, str(prefixes.index(add_set)),
                                     music_file.file_name)

    if not add_flag:

        for e in db.fp_dict[music_file.file_name]:
            if db.fp_dict[music_file.file_name][e] > 50:
                prefixes.append({music_file.file_name})

                return get_link_name(m_path, str(len(prefixes)-1),
                                             music_file.file_name)
        return get_link_name(m_path, '', music_file.file_name)



def start(db):
    con = configparser.ConfigParser()
    con.read('config.ini')
    music_path = con.get("paths", "music_path")
    search_path = con.get("paths", "search_path")
    search_path = [p for p in str(search_path).rsplit(';')]
    sort_type = con.get("general", "sort")

    if not os.path.exists(music_path):
        os.mkdir(music_path)
    else:
        clean_link(db)
        shutil.rmtree(music_path)

        os.mkdir(music_path)

    audio_files = get_file_from_dirs(search_path, db)
    removed_list = check_db(db)
    for e in removed_list:
        db.filenames.remove(e)
        for i in db.fp_dict:
            if i != e:
                db.fp_dict[i].pop(e)
            db.fp_dict.pop(e)
        for i in db.music_file_list:
            if i.file_name == e:
                db.music_file_list.pop(i)
    db.music_file_list.extend(audio_files)
    clustering(db, music_path, sort_type)
    for a in db.music_file_list:
        make_link(a.file_name, a.link)
    db.saveDB()

    # print(files)
    # audio_files = create_music_file_list(files)
    # new_list = append_music_files(audio_files, db)
    # for i in audio_files:
    #     print(i.file_name)
    # for i in db.fp_dict.keys():
    #     print(i)
    #     print(db.fp_dict[i])
    # for a in audio_files:
    #     link = os.path.join(config.music_path, os.path.split(a.file_name)[1])
    #     make_link(a.file_name, link)



if __name__ == "__main__":
    d = DataBase()
    start(d)