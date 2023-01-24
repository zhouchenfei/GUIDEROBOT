#!/usr/bin/python3
# encoding: utf-8
import pigpio
import time
import os
open_io="sudo pigpiod"
os.system(open_io)
time.sleep(1)


class Servo:
    def __init__(self,pin,motor,PWM=20000,frequency=50):
        self.pin=pin
        self.motor=motor
        self.pi = pigpio.pi()
        self.pi.set_PWM_range(self.pin,PWM)
        self.pi.set_PWM_frequency(self.pin,frequency)
        if self.motor=="left":
            self.pi.set_PWM_dutycycle(self.pin, self.trans(0))
        if self.motor=="right":
            self.pi.set_PWM_dutycycle(self.pin, self.trans(180))

        self.current_state=""

        self.current_position=0.0
        self.run_position = 0.0
        # self.walk_position = 0.0
        self.stop_position = 0.0
        self.accelerate_position=0.0
        self.decelerate_position=0.0

    def trans(self,a):
        return (100 * a / 9 + 500)

    def set_angle(self,angle):
        if self.motor=="left":
            self.pi.set_PWM_dutycycle(self.pin,self.trans(float(angle)))
        if self.motor=="right":
            angle=180-float(angle)
            self.pi.set_PWM_dutycycle(self.pin, self.trans(float(angle)))

    def set_motion(self,motion):
        if motion=="run":
            self.set_angle(self.run_position)
        elif motion=="accelerate":
            self.set_angle(self.accelerate_position)
        elif motion=="decelerate":
            self.set_angle(self.decelerate_position)
        # elif motion=="walk":
        #     self.set_angle(self.motor,self.walk_position)
        elif motion=="stop":
            self.set_angle(self.stop_position)
