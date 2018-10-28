# -*- coding: utf-8 -*-
import requests
import time,datetime
import hashlib
import base64
import wave
import random, os

URL = "http://api.xfyun.cn/v1/service/v1/tts"
AUE = "raw"
APPID = "5b9395a1"
API_KEY = "2da79c0bc3ac3750c9be4a792474f45b"

audio_save_path = os.path.dirname(__file__)+"/static/front/audio/"


def getHeader():
    curTime = str(int(time.time()))
    param = "{\"aue\":\"" + AUE + "\",\"auf\":\"audio/L16;rate=16000\",\"speed\":\"5\",\"voice_name\":\"xiaoyan\",\"engine_type\":\"intp65\"}"
    paramBase64 = base64.b64encode(param.encode())
    m2 = hashlib.md5()
    m2.update((API_KEY + curTime + str(paramBase64, 'utf-8')).encode())
    checkSum = m2.hexdigest()
    header = {
        'X-CurTime': curTime,
        'X-Param': paramBase64,
        'X-Appid': APPID,
        'X-CheckSum': checkSum,
        'X-Real-Ip': '127.0.0.1',
        'Content-Type': 'application/x-www-form-urlencoded; charset=utf-8',
    }
    return header


def getBody(text):
    data = {'text': text}
    return data


def writeFile(file, content):
    with open(file, 'wb') as f:
        f.write(content)
    f.close()


framerate = 8000  # 8000
NUM_SAMPLES = 2000
channels = 1  # 1
sampwidth = 2
TIME = 2


def save_wave_file(filename, data):
    '''save the date to the wavfile'''
    wf = wave.open(filename, 'wb')
    wf.setnchannels(channels)
    wf.setsampwidth(sampwidth)
    wf.setframerate(framerate)
    wf.writeframes(b"".join(data))
    wf.close()


def create_audio(question,dir):
    r = requests.post(URL, headers=getHeader(), data=getBody(question))
    contentType = r.headers['Content-Type']
    if contentType == "audio/mpeg":
        sid = r.headers['sid']

        path=audio_save_path+dir

        if not os.path.exists(path):
            os.mkdir(path)

        save_path =path+sid

        if AUE == "raw":
            writeFile(save_path + '.wav', r.content)
            return dir+sid + ".wav"
        else:
            writeFile(save_path + ".mp3", r.content)
            return dir+sid + ".mp3"
    else:
        return dir+r.text


# 生成试题
# range:20,50 100 200
def func_two_plus_minus(range, num):
    plus = 0
    minus = 0
    i = 0
    audiofiles = []
    dir=datetime.datetime.fromtimestamp(time.time()).strftime('_%H%M%S/')
    while i < num:
        a = random.randint(1, range)
        b = random.randint(1, range)
        questions = ""
        if plus <= num / 2:
            questions = str(a) + "加" + str(b) + "等于"
            plus = plus + 1
        elif minus <= num / 2:
            if a > b:
                questions = str(a) + "减" + str(b) + "等于"
            else:
                questions = str(b) + "减" + str(a) + "等于"
            minus = minus + 1
        if questions != "":
            i = i + 1
            audiofiles.append(create_audio(questions,dir))
    return audiofiles


def func_three_plus_minus(range, num):
    plus_plus = 0
    minus_minus = 0
    plus_minus = 0
    minus_plus = 0
    i = 0
    audiofiles = []
    dir = datetime.datetime.fromtimestamp(time.time()).strftime('_%H%M%S/')
    while i < num:
        a = random.randint(1, range)
        b = random.randint(1, range)
        c = random.randint(1, range)
        questions = ""
        if plus_plus <= num / 4:
            questions = str(a) + "加" + str(b) + "加" + str(c) + "等于"
            plus_plus += 1
        elif a + b > c and plus_minus <= num / 4:
            questions = str(a) + "加" + str(b) + "减" + str(c) + "等于"
            plus_minus += 1
        elif a + c > b and minus_plus <= num / 4:
            questions = str(a) + "减" + str(b) + "加" + str(c) + "等于"
            minus_plus += 1
        elif a > b + c and minus_minus <= num / 4:
            questions = str(a) + "减" + str(b) + "减" + str(c) + "等于"
            minus_minus += 1
        if questions != "":
            i = i + 1
            audiofiles.append(create_audio(questions,dir))
    return audiofiles


def func_two_times_devided(range, num):
    times = 0
    devided = 0
    i = 0
    audiofiles = []
    dir = datetime.datetime.fromtimestamp(time.time()).strftime('_%H%M%S/')
    while i < num:
        a = random.randint(1, range)
        b = random.randint(1, range)
        questions = ""
        if times <= num / 2:
            questions = str(a) + "乘" + str(b) + "等于"
            times += 1
        elif devided <= num / 2:
            questions = str(a*b) + "除" + str(b) + "等于"
            devided = devided + 1
        if questions != "":
            i = i + 1
            audiofiles.append(create_audio(questions,dir))
    return audiofiles


def func_three_times_devided(range, num):
    # audiofiles = []
    # dir = datetime.datetime.fromtimestamp(time.time()).strftime('_%H%M%S/')
    # questions = "听算练习已全部完成"
    # audiofiles.append(create_audio(questions,dir))
    # return audiofiles
    pass


def func_three_hybird(range, num):
    return 'func_three_hybird'


def init_audio(range, type, num):

    #本地测试
    # return ['_032557/hts002e973a@ch6d3b0f1a0ec5477600.wav','_032557/hts002e973b@ch6d3b0f1a0ec5477600.wav','_032557/hts002e973c@ch6d3b0f1a0ec5477600.wav']


    # 类型选择
    #     type:1-两个数的加减
    #         :2-三个数的加减
    #         :3-两个数的乘除
    #         :4-三个数的乘除
    #         :5-三个数的混合
    switcher = {
        '1': func_two_plus_minus,
        '2': func_three_plus_minus,
        '3': func_two_times_devided,
        '4': func_three_times_devided,
        '5': func_three_hybird,
    }
    return switcher[type](range, num)
