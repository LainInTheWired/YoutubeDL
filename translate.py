import whisper
from datetime import timedelta
from srt import Subtitle
import srt
import ffmpeg
from deep_translator import GoogleTranslator
from yt_dlp import YoutubeDL
import os
import torch
from whisper.audio import N_FRAMES, pad_or_trim, log_mel_spectrogram
import torch
from janome.tokenizer import Tokenizer



t = Tokenizer()



file_name = "tkinker2"
file_path = file_name + ".mp4"

output_file = "out" + file_name + ".mp4"

subtitle_file = file_name + ".srt"

subs = []

preIndex = []
preStart = []
preEnd = []
preTexts = []

index = 1




def translate(url ,path,booltrans):

    if not url:
        return 2
    if not path:
        return 3

    file_path = path
    file_name = os.path.splitext(path)[0]
    output_file = file_name + "out.mp4"
    subtitle_file = file_name + ".srt"
    try:
        youtubeDL(url,file_name)
    except:
        return 4
    if not booltrans:
        return 0

    model = whisper.load_model("large")
    result = model.transcribe(file_path, verbose=True)
    segments = result["segments"]

    #言語判別

    # model = whisper.load_model("small")

    # result = model.transcribe(file_path, verbose=True)
    # segments = result["segments"]

    mel = log_mel_spectrogram(file_path)

    segment = pad_or_trim(mel, N_FRAMES).to(model.device).to(torch.float32)

    # 判定
    _, probs = model.detect_language(segment)
    sim = 0
    lang = ""
    for prob in probs:
        if sim < probs[prob]:
            sim = probs[prob]
            lang = prob

    index = 1
    temp = ""
    for data in segments:
        start = data["start"]
        end = data["end"]
        for d in data:
            print(d)
        # text = data["text"]
        print("index:" + str(index))

        preIndex.append(index)
        preStart.append(start)
        preEnd.append(end)
        preTexts.append(temp + data["text"])
        temp = ""
        print(preTexts[-1])
        if preTexts[-1][-1] != ".":
            words = preTexts[-1]
            # words = words.split("?", 1)
            if "." in preTexts[-1]:
                words = words.split(".", 1)
                preTexts[-1] = preTexts[-1].replace(words[-1], '')
                temp = words[-1]
            print(preTexts[-1])
            print(temp)




        if lang == "en":
            if preTexts[-1][-1] != ".":
                print("false")
                continue



        index = index + 1
        text = ""

        for pretext in preTexts:
            text = text + pretext

        start = preStart[0]
        text = GoogleTranslator(source='auto', target='ja').translate(text)

        text = add_line(text)

        sub = Subtitle(index=1, start=timedelta(seconds=timedelta(seconds=start).seconds,
                                                microseconds=timedelta(seconds=start).microseconds),
                       end=timedelta(seconds=timedelta(seconds=end).seconds,
                                     microseconds=timedelta(seconds=end).microseconds), content=text, proprietary='')
        print(sub)
        subs.append(sub)

        preEnd.clear()
        preTexts.clear()
        preStart.clear()
        preIndex.clear()

    print(subs)

    with open(subtitle_file, mode="w", encoding="utf-8") as f:
        f.write(srt.compose(subs))

    video = ffmpeg.input(file_path)
    audio = video.audio
    print(subtitle_file)
    print(output_file)
    ffmpeg.concat(video.filter("subtitles", subtitle_file), audio, v=1, a=1).output(output_file).run(overwrite_output=True)
    subs.clear()
    return 0



def add_line(s):
    new_s = s
    s_count = len(s)
    s_max_count = 22
    count = 1
    buff = 0
    while s_count >= s_max_count * count:
        count_in = 22 * count + buff
        buff = 0
        # if (s_count - s_max_count) >= 3:
        print("counter" + str(count))
            # 15文字以上、かつ、2行目が3文字以上あれば、改行する
            # つまり、18文字以上であれば、15文字で改行する
        for token in t.tokenize(s[count_in:]):
            # print(token)
            buff += len(token.surface)
            count_in += len(token.surface)
            if token.part_of_speech.split(',')[1] == "格助詞" or token.part_of_speech.split(',')[1] == "係助詞":
                print(s[count_in ])
                if s[count_in ] == '、' or s[count_in] == '。':
                    count_in += 1
                print("word_count:" + str(count_in))
                s = s[:count_in] + "\n" + s[count_in:]
                break
            if count_in > 35:
                print("word_count:" + str(count_in))
                s = s[:count_in] + "\n" + s[count_in:]
                break
        count += 1
    # print(repr(s))
    print("\n" + s + "\n")
    return s



def includeSubtitle(subtitle_file,output_file):
    video = ffmpeg.input(file_path)
    audio = video.audio
    print(subtitle_file)
    ffmpeg.concat(video.filter("subtitles", subtitle_file), audio, v=1, a=1).output(output_file).run()

def youtubeDL(url,file_name):
    ydl_opts = {'format': 'best',
                'outtmpl': file_name + '.%(ext)s'
                }
    with YoutubeDL(ydl_opts) as ydl:
        result = ydl.download([url])
        print(result)