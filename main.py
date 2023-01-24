from tkinter import *
from tkinter import messagebox
from servo import Servo
from gui import Application
from yy_control import *


if __name__ == '__main__':
    root = Tk()
    # root.geometry("700x400+200+300")
    root.attributes("-fullscreen",True)
    left_motor=Servo(12,"left")
    right_motor=Servo(16,"right")
    frame1=Frame(root)
    frame1.pack(pady=50)
    app = Application(root,left_motor,right_motor)
    root.mainloop()

    # print(left_motor.run_position,left_motor.walk_position,left_motor.walk_position)
    # print(right_motor.run_position,right_motor.walk_position,right_motor.stop_position)
    #
    # client = AipSpeech(APP_ID, API_KEY, SECRET_KEY)
    #
    # while (True):
    #
    #     print("\n\n==================================================")
    #     print("Please tell me the command(limit within 5 seconds):")
    #
    #     audio_record('./speak.wav', 5)
    #     print("Identify On Network...")
    #     # asr_result = aip_get_asrresult(client, './speak.wav', 'wav')
    #     a = client.asr(get_file_content('./speak.wav'), 'wav', 16000, {'dev_pid': 1537, })
    #
    #     if a["err_no"] == 0 and a["result"] != ['']:
    #         print("Identify Result:", a["result"])
    #         print("Start Control..")
    #         current_state=PWM_contral(a["result"][0],left_motor,right_motor)  # 根据识别结果控制页面滚动
    #         print("current state",current_state)
    #         print("Control End...")
    #         if a["result"][0].find("退出") != -1:
    #             break;
    #         time.sleep(1)

    print("end")