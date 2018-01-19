__author__ = 'kowalski'
import subprocess
import hashlib

ffmpeg = 'audio/ffmpeg'


def checksum(file_name):
    command = ffmpeg + ' -i "' + file_name + '" -vn' + " -f " +"s24le "+ "-"
    proc = subprocess.Popen(command, stdout=subprocess.PIPE,stderr=subprocess.PIPE,shell=True)
    hash_creator = hashlib.sha1()
    empty = True
    while True:
        data = proc.stdout.read(hash_creator.block_size * 128)
        if not data:
            break
        empty = False
        hash_creator.update(data)
    if empty:
        return None
    proc.stdout.close()
    proc.stderr.close()
    return hash_creator.hexdigest()
