import os
import re

def make_root_folders():
    try:
        os.mkdir('videos')
    except FileExistsError:
        pass
    try:
        os.mkdir('audios')
    except FileExistsError:
        pass
    try:
        os.mkdir('transcriptions')
    except FileExistsError:
        pass
    try:
        os.mkdir('screenshots')
    except FileExistsError:
        pass

def clean_everything():
    try:
        os.rmdir('videos')
    except:
        pass
    try:
        os.rmdir("audios")
    except:
        pass
    try:
        os.rmdir("transcriptions")
    except:
        pass

def find_longest_sequence(s):
    sequences = re.findall(r'\d+', s)
    if sequences:
        return max(sequences, key=len)
    else:
        return None
    
def rename_videos(streamer_name):
    directory = f"videos/{streamer_name}/"
    for filename in os.listdir(directory):
        longest_sequence = find_longest_sequence(filename)
        if longest_sequence:
            new_filename = longest_sequence + os.path.splitext(filename)[1]
            os.rename(os.path.join(directory, filename),
                    os.path.join(directory, new_filename))

if __name__ == '__main__':
    make_root_folders()