import wave
import pyaudio
import os
import tkinter.filedialog
import subprocess
import chardet

def getencoding(dat:bytes):
    return chardet.detect(dat)["encoding"]

def select_file():
    iDir = os.path.abspath(os.path.dirname(__file__))  # スクリプトのディレクトリを取得
    file_path = tkinter.filedialog.askopenfilename(initialdir=iDir)  # ファイル選択ダイアログを表示
    print(f"選択されたファイル: {file_path}")
    return file_path

filename=f"{os.getcwd()}\\output.wav"

CHUNK = 1024

def play_wav():
    w = wave.open(filename, 'rb')
    p = pyaudio.PyAudio()
    stream = p.open(format=p.get_format_from_width(w.getsampwidth()),
                    channels=w.getnchannels(),
                    rate=w.getframerate(),
                    output=True)
    data = w.readframes(CHUNK)
    while len(data) > 0:
      stream.write(data)
      data = w.readframes(CHUNK)
    stream.stop_stream()
    stream.close()
    p.terminate()

target = select_file()
with open(target, "rb") as f:
    enc = getencoding(f.read())

read_txt = open(target,"r",encoding=enc).read().split("\n")
read_txt = [tr for tr in read_txt if tr!=""]

for rt in read_txt:
    subprocess.run([r"C:\Program Files\VOICEPEAK\voicepeak.exe",'-s',rt,'--speed 100','--pitch 30'])
    play_wav()

