import pyaudio
import wave
from aip import AipSpeech
import time
from tkinter import *


APP_ID = '22632304'
API_KEY = 'zUWDV4UgeRbah3tOYUS7CKUK'
SECRET_KEY = 'jmCuQmlVSWLdIRM9lz3GVcFlYtrUaWpd'


def get_file_content(filePath):
    with open(filePath, 'rb') as fp:
        return fp.read()


def audio_record(out_file, rec_time):
    CHUNK = 1024
    FORMAT = pyaudio.paInt16
    CHANNELS = 1
    RATE = 16000
    p = pyaudio.PyAudio()

    stream = p.open(format=FORMAT,
                    channels=CHANNELS,
                    rate=RATE,
                    input=True,
                    frames_per_buffer=CHUNK)
    print("Start Recording...")
    frames = []

    for i in range(0, int(RATE / CHUNK * rec_time)):
        data = stream.read(CHUNK)
        frames.append(data)

    stream.stop_stream()
    stream.close()
    p.terminate()
    print("Recording Done...")

    wf = wave.open(out_file, 'wb')
    wf.setnchannels(CHANNELS)
    wf.setsampwidth(p.get_sample_size(FORMAT))
    wf.setframerate(RATE)
    wf.writeframes(b''.join(frames))
    wf.close()


# # 控制鼠标滚动
# def mouse_control(dir_tr):
#     MOVE_DX = 5  # 每次滚动行数
#     ms = PyMouse()
#     horizontal = 0
#     vertical = 0
#     if dir_tr.find("上") != -1:  # 向上移动
#         vertical = MOVE_DX
#         ms.move(540, 0)
#         # print("vertical={0}, 向上".format(vertical))
#     elif dir_tr.find("下") != -1:  # 向下移动
#         vertical = 0 - MOVE_DX
#         ms.move(540, 1080)
#         # print("vertical={0}, 向下".format(vertical))
#     elif dir_tr.find("左") != -1:  # 向左移动
#         horizontal = 0 - MOVE_DX
#         ms.move(0, 540)
#         # print("horizontal={0}, 向左".format(horizontal))
#     elif dir_tr.find("右") != -1:  # 向右移动
#         horizontal = MOVE_DX
#         ms.move(1920, 540)
#         # print("horizontal={0}, 向右".format(horizontal))
#
#     # print("horizontal, vertical=[{0},{1}]".format(horizontal, vertical))
#     # 通过scroll(vertical, horizontal)函数控制页面滚动
#     # 另外PyMouse还支持模拟move光标,模拟鼠标click,模拟键盘击键等

def PWM_contral(dir_tr,left_motor,right_motor):
    if dir_tr.find("跑步") != -1:  # 向上移动
        left_motor.set_motion("run")
        right_motor.set_motion("run")
        left_motor.current_state="run"
        right_motor.current_state="run"
        return left_motor.current_state, right_motor.current_state

    # elif dir_tr.find("走路") != -1:  # 向下移动
    #     left_motor.set_motion("walk")
    #     right_motor.set_motion("walk")
    #     left_motor.current_state = "walk"
    #     right_motor.current_state = "walk"
    #     return left_motor.current_state, right_motor.current_state

    elif dir_tr.find("加速") != -1:  # 向左移动
        left_motor.set_motion("accelerate")
        right_motor.set_motion("accelerate")
        left_motor.current_state = "accelerate"
        right_motor.current_state = "accelerate"
        return left_motor.current_state, right_motor.current_state
    elif dir_tr.find("减速") != -1:  # 向左移动
        left_motor.set_motion("decelerate")
        right_motor.set_motion("decelerate")
        left_motor.current_state = "decelerate"
        right_motor.current_state = "decelerate"
        return left_motor.current_state, right_motor.current_state
    elif dir_tr.find("停") != -1:  # 向左移动
        left_motor.set_motion("stop")
        right_motor.set_motion("stop")
        left_motor.current_state = "stop"
        right_motor.current_state = "stop"
        return left_motor.current_state, right_motor.current_state
    else:
        return left_motor.current_state,right_motor.current_state




def aip_get_asrresult(client, afile, afmt):
    result = client.asr(get_file_content(afile), afmt, 16000, {"dev_pid": 1573, })

    if result["err_msg"] == "success.":

        return result["result"]
    else:
        return ""

if __name__ == '__main__':
    client = AipSpeech(APP_ID, API_KEY, SECRET_KEY)

    while (True):

        print("\n\n==================================================")
        print("Please tell me the command(limit within 5 seconds):")

        audio_record('./speak.wav', 5)
        print("Identify On Network...")
        # asr_result = aip_get_asrresult(client, './speak.wav', 'wav')
        a = client.asr(get_file_content('./speak.wav'), 'wav', 16000, {'dev_pid': 1537, })

        if a["err_no"] == 0 and a["result"]!=['']:
            print("Identify Result:", a["result"])
            print("Start Control..")
            #mouse_control(a["result"][0])  # 根据识别结果控制页面滚动
            print("Control End...")
            if a["result"][0].find("停止识别") != -1:
                break;
            time.sleep(1)
