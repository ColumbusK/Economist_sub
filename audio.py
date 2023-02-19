import os

from pydub import AudioSegment
import re

audio = AudioSegment.silent(duration=10)


folder_path = r"C:\Users\zkz\Desktop\TEAudio20230128"


def merge_export(ls, path):
    audio = AudioSegment.empty()
    for f in ls:
        print('f', f)
        audio += AudioSegment.from_mp3(f)
    out_f = open(path, 'wb')
    audio.export(out_f, 'mp3')


def merge_audios(folder_path):
    section_name = ""
    f_title = ""
    audio_list = []
    pattern = re.compile(r'([a-z ]+) -', re.I)
    for f in os.listdir(folder_path)[1:]:
        if pattern.search(f):
            f_title = pattern.search(f).group().strip(' -')
        if f_title != section_name:
            if len(audio_list) > 0:
                merge_export(audio_list, os.path.join(
                    folder_path, f"{section_name}.mp3"))
            section_name = f_title
            print(audio_list)
            audio_list.clear()
            audio_list.append(os.path.join(folder_path, f))
        if f_title == section_name:
            audio_list.append(os.path.join(folder_path, f))


# merge_audios(folder_path)

s = './Introduction.mp3'

AudioSegment.from_mp3(s)
