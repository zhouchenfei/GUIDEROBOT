from tkinter import *
from tkinter import messagebox
from servo import Servo
from yy_control import *
from multiprocessing import Process
import threading
import ctypes
import inspect


class Application(Frame):

    def __init__(self, master=None,left_motor=None,right_motor=None):
        super().__init__(master)        # super()代表的是父类的定义，而不是父类对象
        self.master = master
        self.pack()
        self.createWidget()
        self.current_select_motion=""

        self.deactivate()

        self.left_motor=left_motor
        self.right_motor=right_motor
        self.flag=True



    def createWidget(self):
        """创建界面的组件"""
        self.username = Label(self,text="用户名:")
        self.username.grid(row=4,column=0)

        v1 = StringVar()
        self.entry01 = Entry(self,textvariable=v1)
        self.entry01.grid(row=4,column=1)

        self.password = Label(self,text="密码:")
        self.password.grid(row=4,column=2,sticky="w")

        v2 = StringVar()
        self.entry02 = Entry(self, textvariable=v2)
        self.entry02.grid(row=4, column=2,padx=50)

        self.v=StringVar()
        self.v.set("")
        self.bt_login=Button(self,text="登陆",width=6,height=1,command=self.login)
        self.bt_logout=Button(self,text="退出",width=6,height=1,command=self.logout)
        self.bt_set=Button(self,text="开始录入",width=6,height=1,command=self.set)
        self.bt_set_finish=Button(self,text="完成",width=6,height=1,command=self.set_finish)
        self.bt_begin_recgnize=Button(self,text="开始识别",width=6,height=1,command=self.begin_recgnize)
        # self.bt_stop_recgnize = Button(self, text="停止识别", width=6, height=1, command=self.stop_recgnize)

        self.bt_login.grid(row=4, column=3,sticky="e")
        self.bt_logout.grid(row=10, column=3)
        self.bt_set.grid(row=5, column=0)
        self.bt_set_finish.grid(row=5, column=1)
        self.bt_begin_recgnize.grid(row=10,column=0)
        # self.bt_stop_recgnize.grid(row=10,column=1)


        self.run=Radiobutton(self,text="跑步",value="run",variable=self.v)
        self.run.bind("<Button-1>",self.click_run)
        # self.walk=Radiobutton(self,text="慢走",value="walk",variable=self.v)
        # self.walk.bind("<Button-1>", self.click_walk)
        self.accelerate=Radiobutton(self,text="加速",value="accelerate",variable=self.v)
        self.accelerate.bind("<Button-1>", self.click_accelerate)
        self.decelerate = Radiobutton(self, text="减速", value="decelerate", variable=self.v)
        self.decelerate.bind("<Button-1>", self.click_decelerate)
        self.stop=Radiobutton(self,text="停",value="stop",variable=self.v)
        self.stop.bind("<Button-1>", self.click_stop)

        self.run.grid(row=6,column=0)
        self.accelerate.grid(row=7,column=0)
        self.decelerate.grid(row=8,column=0)
        # self.walk.grid(row=3,column=0)
        self.stop.grid(row=9,column=0)

        self.run_left_motor=Scale(self,from_=0,to=90,length=200,tickinterval=30,orient=HORIZONTAL,command=self.set_run_left_motor)
        self.run_right_motor=Scale(self,from_=0,to=90,length=200,tickinterval=30,orient=HORIZONTAL,command=self.set_run_right_motor)

        self.accelerate_left_motor=Scale(self,from_=0,to=90,length=200,tickinterval=30,orient=HORIZONTAL,command=self.set_accelerate_left_motor)
        self.accelerate_right_motor=Scale(self,from_=0,to=90,length=200,tickinterval=30,orient=HORIZONTAL,command=self.set_accelerate_right_motor)

        self.decelerate_left_motor=Scale(self,from_=0,to=90,length=200,tickinterval=30,orient=HORIZONTAL,command=self.set_decelerate_left_motor)
        self.decelerate_right_motor=Scale(self,from_=0,to=90,length=200,tickinterval=30,orient=HORIZONTAL,command=self.set_decelerate_right_motor)

        # self.walk_left_motor=Scale(self,from_=0,to=90,length=200,tickinterval=30,orient=HORIZONTAL,command=self.set_walk_left_motor)
        # self.walk_right_motor=Scale(self,from_=0,to=90,length=200,tickinterval=30,orient=HORIZONTAL,command=self.set_walk_right_motor)
        self.stop_left_motor=Scale(self,from_=0,to=90,length=200,tickinterval=30,orient=HORIZONTAL,command=self.set_stop_left_motor)
        self.stop_right_motor=Scale(self,from_=0,to=90,length=200,tickinterval=30,orient=HORIZONTAL,command=self.set_stop_right_motor)

        self.run_left_motor.grid(row=6,column=1)
        self.run_right_motor.grid(row=6,column=2)
        self.accelerate_left_motor.grid(row=7,column=1)
        self.accelerate_right_motor.grid(row=7,column=2)
        self.decelerate_left_motor.grid(row=8,column=1)
        self.decelerate_right_motor.grid(row=8,column=2)
        # self.walk_left_motor.grid(row=3,column=1)
        # self.walk_right_motor.grid(row=3,column=2)
        self.stop_left_motor.grid(row=9,column=1)
        self.stop_right_motor.grid(row=9,column=2)

        # self.v_message = StringVar()
        # self.v_message.set("当前状态:空")
        # self.current_message=Label(self,textvariable=self.v_message,font=("",20))
        # self.current_message.grid(row=11,column=0,columnspan=3)


    # def _async_raise(self,tid, exctype):
    #     """raises the exception, performs cleanup if needed"""
    #     tid = ctypes.c_long(tid)
    #     if not inspect.isclass(exctype):
    #         exctype = type(exctype)
    #     res = ctypes.pythonapi.PyThreadState_SetAsyncExc(tid, ctypes.py_object(exctype))
    #     if res == 0:
    #         raise ValueError("invalid thread id")
    #     elif res != 1:
    #         # """if it returns a number greater than one, you're in trouble,
    #         # and you should call it again with exc=NULL to revert the effect"""
    #         ctypes.pythonapi.PyThreadState_SetAsyncExc(tid, None)
    #         raise SystemError("PyThreadState_SetAsyncExc failed")
    #
    # def stop_thread(self,thread):
    #     self._async_raise(thread.ident, SystemExit)

    def begin_recgnize(self):
        # self.v_message.set("当前状态:正在识别")
        # self.bt_stop_recgnize["state"] = "normal"
        # self.v_message.set("正在识别")
        time.sleep(0.3)
        # self.T = threading.Thread(target=self._begin_recgnize)
        # self.T=Process(target=self._begin_recgnize)
        # self.T.start()
        self._begin_recgnize()

    def _begin_recgnize(self):
        print(self.left_motor.run_position, self.left_motor.accelerate_position,self.left_motor.decelerate_position, self.left_motor.stop_position)
        print(self.right_motor.run_position, self.right_motor.accelerate_position,self.right_motor.decelerate_position, self.right_motor.stop_position)
        self.flag =True
        client = AipSpeech(APP_ID, API_KEY, SECRET_KEY)

        while self.flag==True:

            print("\n\n==================================================")
            print("self.flag:",self.flag)
            print("Please tell me the command(limit within 5 seconds):")

            audio_record('./speak.wav', 4.5)
            print("Identify On Network...")
            # asr_result = aip_get_asrresult(client, './speak.wav', 'wav')
            a = client.asr(get_file_content('./speak.wav'), 'wav', 16000, {'dev_pid': 1537, })

            if a["err_no"] == 0 and a["result"] != ['']:
                print("Identify Result:", a["result"])
                print("Start Control..")
                current_state = PWM_contral(a["result"][0], self.left_motor, self.right_motor)
                print("current state", current_state)
                print("Control End...")
                # if a["result"][0].find("跑步")!= -1:
                #     self.v_message.set("当前状态:跑步")
                # if a["result"][0].find("加速")!= -1:
                #     self.v_message.set("当前状态:加速")
                # if a["result"][0].find("减速")!= -1:
                #     self.v_message.set("当前状态:减速")
                # if a["result"][0].find("停")!= -1:
                #     self.v_message.set("当前状态:停")
                if a["result"][0].find("结束") != -1:
                    # self.v_message.set("当前状态:已停止识别")
                    break;

                # time.sleep(0.5)
        messagebox.showinfo("当前状态","已停止识别")

    def stop_recgnize(self):
        self.flag=False
        self.v_message.set("当前状态:已停止识别")
        print("self.flag",self.flag)


    def click_accelerate(self,event):
        self.current_select_motion = "accelerate"
        self.set_scale_state(self.current_select_motion)

        self.left_motor.current_position = self.left_motor.accelerate_position
        self.right_motor.current_position = self.right_motor.accelerate_position
        self.left_motor.set_angle(self.left_motor.current_position)
        self.right_motor.set_angle(self.right_motor.current_position)

    def click_decelerate(self,event):
        self.current_select_motion = "decelerate"
        self.set_scale_state(self.current_select_motion)

        self.left_motor.current_position = self.left_motor.run_position
        self.right_motor.current_position = self.right_motor.run_position
        self.left_motor.set_angle(self.left_motor.current_position)
        self.right_motor.set_angle(self.right_motor.current_position)

    def click_run(self,event):
        self.current_select_motion="run"
        self.set_scale_state(self.current_select_motion)

        self.left_motor.current_position=self.left_motor.run_position
        self.right_motor.current_position=self.right_motor.run_position
        self.left_motor.set_angle(self.left_motor.current_position)
        self.right_motor.set_angle(self.right_motor.current_position)


    # def click_walk(self,event):
    #     self.current_select_motion = "walk"
    #     self.set_scale_state(self.current_select_motion)
    #
    #     self.left_motor.current_position = self.left_motor.walk_position
    #     self.right_motor.current_position = self.right_motor.walk_position
    #     self.left_motor.set_angle("left",self.left_motor.current_position)
    #     self.right_motor.set_angle("right",self.right_motor.current_position)


    def click_stop(self,event):
        self.current_select_motion = "stop"
        self.set_scale_state(self.current_select_motion)

        self.left_motor.current_position = self.left_motor.stop_position
        self.right_motor.current_position = self.right_motor.stop_position
        self.left_motor.set_angle(self.left_motor.current_position)
        self.right_motor.set_angle(self.right_motor.current_position)




    def set_run_left_motor(self,value):
        self.left_motor.current_position=value
        self.left_motor.run_position=value
        self.left_motor.set_angle(self.left_motor.current_position)

        self.print_current_motor_position()
        self.print_run_motor_posiition()

    def set_run_right_motor(self,value):
        self.right_motor.current_position = value
        self.right_motor.run_position = value
        self.right_motor.set_angle(self.right_motor.current_position)

        self.print_current_motor_position()
        self.print_run_motor_posiition()

    def set_accelerate_left_motor(self,value):
        self.left_motor.current_position = value
        self.left_motor.accelerate_position = value
        self.left_motor.set_angle(self.left_motor.current_position)

        self.print_current_motor_position()
        self.print_accelerate_motor_posiition()

    def set_accelerate_right_motor(self,value):
        self.right_motor.current_position = value
        self.right_motor.accelerate_position = value
        self.right_motor.set_angle(self.right_motor.current_position)

        self.print_current_motor_position()
        self.print_accelerate_motor_posiition()

    def set_decelerate_left_motor(self, value):
        self.left_motor.current_position = value
        self.left_motor.decelerate_position = value
        self.left_motor.set_angle(self.left_motor.current_position)

        self.print_current_motor_position()
        self.print_decelerate_motor_posiition()

    def set_decelerate_right_motor(self, value):
        self.right_motor.current_position = value
        self.right_motor.decelerate_position = value
        self.right_motor.set_angle(self.right_motor.current_position)

        self.print_current_motor_position()
        self.print_decelerate_motor_posiition()

    # def set_walk_left_motor(self,value):
    #     self.left_motor.current_position = value
    #     self.left_motor.walk_position = value
    #     self.left_motor.set_angle("left",self.left_motor.current_position)
    #
    #     self.print_current_motor_position()
    #     self.print_walk_motor_posiition()
    #
    # def set_walk_right_motor(self,value):
    #     self.right_motor.current_position = value
    #     self.right_motor.walk_position = value
    #     self.right_motor.set_angle("right",self.right_motor.current_position)
    #
    #     self.print_current_motor_position()
    #     self.print_walk_motor_posiition()

    def set_stop_left_motor(self,value):
        self.left_motor.current_position = value
        self.left_motor.stop_position = value
        self.left_motor.set_angle(self.left_motor.current_position)

        self.print_current_motor_position()
        self.print_stop_motor_posiition()

    def set_stop_right_motor(self,value):
        self.right_motor.current_position = value
        self.right_motor.stop_position = value
        self.right_motor.set_angle(self.right_motor.current_position)

        self.print_current_motor_position()
        self.print_stop_motor_posiition()

    def set_scale_state(self,motion):
        if motion=="run":
            self.run_left_motor["state"]="normal"
            self.run_right_motor["state"]="normal"

            self.accelerate_left_motor["state"]="disabled"
            self.accelerate_right_motor["state"]="disabled"

            self.decelerate_left_motor["state"]="disabled"
            self.decelerate_right_motor["state"]="disabled"

            # self.walk_left_motor["state"]="disabled"
            # self.walk_right_motor["state"]="disabled"

            self.stop_left_motor["state"]="disabled"
            self.stop_right_motor["state"]="disabled"

        elif motion=="accelerate":
            self.run_left_motor["state"] = "disabled"
            self.run_right_motor["state"] = "disabled"

            self.accelerate_left_motor["state"] = "normal"
            self.accelerate_right_motor["state"] = "normal"

            self.decelerate_left_motor["state"] = "disabled"
            self.decelerate_right_motor["state"] = "disabled"

            # self.walk_left_motor["state"]="disabled"
            # self.walk_right_motor["state"]="disabled"

            self.stop_left_motor["state"] = "disabled"
            self.stop_right_motor["state"] = "disabled"

        elif motion=="decelerate":
            self.run_left_motor["state"] = "disabled"
            self.run_right_motor["state"] = "disabled"

            self.accelerate_left_motor["state"] = "disabled"
            self.accelerate_right_motor["state"] = "disabled"

            self.decelerate_left_motor["state"] = "normal"
            self.decelerate_right_motor["state"] = "normal"

            # self.walk_left_motor["state"]="disabled"
            # self.walk_right_motor["state"]="disabled"

            self.stop_left_motor["state"] = "disabled"
            self.stop_right_motor["state"] = "disabled"

        # elif motion=="walk":
        #     self.run_left_motor["state"]="disabled"
        #     self.run_right_motor["state"]="disabled"
        #
        #     self.walk_left_motor["state"]="normal"
        #     self.walk_right_motor["state"]="normal"
        #
        #     self.stop_left_motor["state"]="disabled"
        #     self.stop_right_motor["state"]="disabled"

        elif motion=="stop":
            self.run_left_motor["state"]="disabled"
            self.run_right_motor["state"]="disabled"

            self.accelerate_left_motor["state"] = "disabled"
            self.accelerate_right_motor["state"] = "disabled"

            self.decelerate_left_motor["state"] = "disabled"
            self.decelerate_right_motor["state"] = "disabled"

            # self.walk_left_motor["state"]="disabled"
            # self.walk_right_motor["state"]="disabled"

            self.stop_left_motor["state"]="normal"
            self.stop_right_motor["state"]="normal"



    def deactivate(self):

        self.bt_set["state"] = "disabled"
        self.bt_set_finish["state"] = "disabled"

        self.run["state"] = "disabled"
        self.accelerate["state"]="disabled"
        self.decelerate["state"]="disabled"
        # self.walk["state"] = "disabled"
        self.stop["state"] = "disabled"

        self.run_left_motor["state"] = "disabled"
        self.run_right_motor["state"] = "disabled"

        self.accelerate_left_motor["state"] = "disabled"
        self.accelerate_right_motor["state"] = "disabled"
        self.decelerate_left_motor["state"] = "disabled"
        self.decelerate_right_motor["state"] = "disabled"
        # self.walk_left_motor["state"] = "disabled"
        # self.walk_right_motor["state"] = "disabled"
        self.stop_left_motor["state"] = "disabled"
        self.stop_right_motor["state"] = "disabled"

        self.bt_begin_recgnize["state"] = "disabled"
        # self.bt_stop_recgnize["state"] = "disabled"

    def activate(self):
        self.bt_set["state"] = "normal"
        # self.bt_set_finish["state"] = "normal"
        self.bt_begin_recgnize["state"] = "normal"



    def login(self):
        username = self.entry01.get()
        pwd = self.entry02.get()
        if username=="admin" and pwd == "zhou":
            self.activate()
            self.entry01.delete(0,"end")
            self.entry02.delete(0,"end")


    def logout(self):
        self.master.destroy()

    def set(self):
        # self.v_message.set("正在录入")
        self.bt_set["state"]="disabled"
        self.bt_set_finish["state"]="normal"

        self.run["state"] = "normal"
        self.accelerate["state"] = "normal"
        self.decelerate["state"] = "normal"
        # self.walk["state"] = "normal"
        self.stop["state"] = "normal"

        self.bt_begin_recgnize["state"]="disabled"

        self.run_left_motor["state"] = "disabled"
        self.run_right_motor["state"] = "disabled"
        self.accelerate_left_motor["state"] = "disabled"
        self.accelerate_right_motor["state"] = "disabled"
        self.decelerate_left_motor["state"] = "disabled"
        self.decelerate_right_motor["state"] = "disabled"
        # self.walk_left_motor["state"] = "disabled"
        # self.walk_right_motor["state"] = "disabled"
        self.stop_left_motor["state"] = "disabled"
        self.stop_right_motor["state"] = "disabled"


    def set_finish(self):
        # self.v_message.set("完成录入")
        self.bt_set["state"]="normal"
        self.bt_set_finish["state"]="disabled"

        self.run["state"] = "disabled"
        self.accelerate["state"] = "disabled"
        self.decelerate["state"] = "disabled"
        # self.walk["state"] = "disabled"
        self.stop["state"] = "disabled"

        self.bt_begin_recgnize["state"]="normal"

        self.run_left_motor["state"] = "disabled"
        self.run_right_motor["state"] = "disabled"
        self.accelerate_left_motor["state"] = "disabled"
        self.accelerate_right_motor["state"] = "disabled"
        self.decelerate_left_motor["state"] = "disabled"
        self.decelerate_right_motor["state"] = "disabled"
        # self.walk_left_motor["state"] = "disabled"
        # self.walk_right_motor["state"] = "disabled"
        self.stop_left_motor["state"] = "disabled"
        self.stop_right_motor["state"] = "disabled"

    def print_current_motor_position(self):
        print("current motor position:left:",self.left_motor.current_position,"right:",self.right_motor.current_position)

    def print_run_motor_posiition(self):
        print("run motor posiition:left:",self.left_motor.run_position,"right:",self.right_motor.run_position)

    def print_accelerate_motor_posiition(self):
        print("accelerate motor posiition:left:",self.left_motor.accelerate_position,"right:",self.right_motor.accelerate_position)

    def print_decelerate_motor_posiition(self):
        print("decelerate motor posiition:left:",self.left_motor.decelerate_position,"right:",self.right_motor.decelerate_position)

    # def print_walk_motor_posiition(self):
    #     print("walk motor posiition:left:",self.left_motor.walk_position,"right:",self.right_motor.walk_position)

    def print_stop_motor_posiition(self):
         print("stop motor posiition:left:", self.left_motor.stop_position,"right:",self.right_motor.stop_position)



if __name__ == '__main__':
    root = Tk()
    root.geometry("700x400+200+300")
    app = Application(master=root)
    root.mainloop()
    print("end")