import time
from pinpong.board import gboard,I2C,Pin
import math

class MOTOR():
    FORWARD                   = 0
    BACKWARDS                 = 1
    TURNLEFT                  = 2
    TURNRIGHT                 = 3
    M1                        = 1
    M2                        = 2
    def __init__(self, board = None):
        if isinstance(board, int):
            i2c_addr = board
            board = gboard
        elif board is None:
            board = gboard
    
    def begin(self):
        self.dir1 = Pin(4, Pin.OUT)
        self.SPPED1 = Pin(5, Pin.OUT)
        self.dir2 = Pin(7, Pin.OUT)
        self.SPPED2 = Pin(6, Pin.OUT)
        time.sleep(0.02)
        self.dir1.value(0)
        self.SPPED1.value(0)
        self.dir2.value(0)
        self.SPPED2.value(0)
    
    def motor_run(self, index, direction, speed):
        speed = speed*255//100
        if direction == self.FORWARD:
            self.set_motor(index, speed)
        elif direction == self.BACKWARDS:
            self.set_motor(index, -speed)
        else:
            self.motor_stop()
            
    def motor_stop(self):
        self.set_motor(1, 0)
        time.sleep(0.1)
        self.set_motor(2, 0)
        
    def set_motor(self, motorId, speed):
        if motorId == 1:
            speedPin = 5
            directionPin = 4
            if speed == 0:
                try:
                    self.pwm1.write_analog(0)
                except:
                    pass
            else:
                if speed > 0:
                    self.dir1.value(0)
                else:
                    self.dir1.value(1)
                self.pwm1 = Pin(speedPin, Pin.PWM)
                time.sleep(0.01)
                speed = speed if speed > 0 else -speed
                self.pwm1.write_analog(speed)
        elif motorId == 2:
            speedPin = 6
            directionPin = 7
            if speed == 0:
                try:
                    self.pwm2.write_analog(0)
                except:
                    pass
            else:
                if speed > 0:
                    self.dir2.value(0)
                else:
                    self.dir2.value(1)
                self.pwm2 = Pin(speedPin, Pin.PWM)
                time.sleep(0.01)
                speed = speed if speed > 0 else -speed
                self.pwm2.write_analog(speed)
        else:
            return
            
    
    
    
    
    