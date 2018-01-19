__author__ = 'kowalski'
import audio.fingerprinting

def check_by_hash(music_file, db, new_files):
    files = db.music_file_list
    db_flag = False
    new_flag = False
    for e in files:
        if music_file.hashes == e.hashes:
            db_flag = True
    for e in new_files:
        if music_file.hashes == e.hashes:
            new_flag = True

    return db_flag or new_flag


def check_by_fp(music_file, db, new_files):
    db_dict = {}
    new_dict = {}
    files = db.music_file_list
    for e in files:
        db_dict[e.file_name] = int(audio.fingerprinting.compare(
            music_file.fingerprints, e.fingerprints)*100)
    for e in new_files:
        new_dict[e.file_name] = int(audio.fingerprinting.compare(
            music_file.fingerprints, e.fingerprints)*100)
    return db_dict, new_dict