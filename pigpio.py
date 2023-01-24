class PI:
    def __init__(self,PWM=0,freq=0,dutycycle=0):
        self.PWM=PWM
        self.freq=freq
        self.dutycycle=dutycycle

    def set_PWM_range(self,pin,PWM):
        self.PWM=PWM

    def set_PWM_frequency(self,pin,freq):
        self.freq=freq

    def set_PWM_dutycycle(self,pin,dutycycle):
        self.dutycycle=dutycycle


def pi():
    return PI()