# -*- coding: utf-8 -*-

import os
import sys, getopt
import json
import time
import serial
import platform
import serial.tools.list_ports
import subprocess

from pinpong.base.avrdude import *
from pinpong.base import pymata4
from pinpong.base.comm import *
try:
  from PIL import Image
except:
  pass
try:
  import smbus
  import spidev
  import RPi.GPIO as GPIO
except:
  pass

gboard = None

def get_pin(board,vpin):
  if board.boardname == "UNO" or board.boardname == "LEONARDO" or board.boardname == "MEGA2560":
    dpin = vpin if vpin<20 else (vpin-100+14) if vpin >= 100 else -1
    apin = vpin-100 if vpin >= 100 else -1
  else:
    dpin=apin=vpin
  return dpin,apin

class DuinoPin:
  def __init__(self, board=None, pin=None, mode=None):
    self.pin = pin
    self.mode = mode
    self.board = board
    self.pin,self.apin = get_pin(self.board, pin)

    if(mode == Pin.OUT):
      self.board.board.set_pin_mode_digital_output(self.pin)
    elif(mode == Pin.IN):
      self.board.board.set_pin_mode_digital_input(self.pin, callback=None)
    elif(mode == Pin.PWM):#为了支持面向过程的4个API而设计的此选项，尽量避免使用,使用PWM类代替
      self.board.board.set_pin_mode_pwm_output(self.pin)
    elif(mode == Pin.ANALOG):#为了支持面向过程的4个API而设计的此选项，尽量避免使用，使用ADC类代替
      self.board.board.set_pin_mode_analog_input(self.apin,None)

  def value(self, v = None):
    if v is None:  #Read
      if self.mode == Pin.OUT:
        return self.val
      else:
        if self.pin is None:
          return
        self.val = self.board.board.digital_read(self.pin)
        return self.val
    else:  #Write
      self.val = v
      if(self.pin == None):
        return
      self.board.board.digital_pin_write(self.pin, v)
      time.sleep(0.001)

  def on(self):
    self.val = 1
    if self.pin is None:
      return
    self.board.board.digital_pin_write(self.pin, 1)

  def off(self):
    self.val = 0
    if(self.pin == None):
      return
    self.board.board.digital_pin_write(self.pin, 0)

  def irq(self, trigger, handler):
    self.board.board.set_pin_mode_digital_input(self.pin, None)
    self.board.board.set_digital_pin_params(self.pin, trigger, handler)
  
  #这5个函数将打破原有的面向对象规则，请慎用
  #建议使用value方法 PWM和ADC类来替代这5个函数 
  def write_analog(self, duty):
    self.duty=duty
    self.freq=100
    if self.board.boardname == "UNO" or self.board.boardname == "LEONARDO":
      real_duty = int(self.duty / 255 * 100)
      self.board.board.pwm_write(self.pin, self.freq, real_duty)
    else:
      self.board.board.dfrobot_pwm_write(self.pin, self.freq, self.duty)

  def write_digital(self, value):
    self.val = value
    if(self.pin == None):
      return
    self.board.board.digital_pin_write(self.pin, value)

  def read_digital(self):
    if(self.pin == None):
      return
    self.val = self.board.board.digital_read(self.pin)
    return self.val

  def read_analog(self):
    return self.board.board.analog_read(self.apin)

  def pin_mode(self, mode):
    if(mode == Pin.OUT):
      self.board.board.set_pin_mode_digital_output(self.pin)
    elif(mode == Pin.IN):
      self.board.board.set_pin_mode_digital_input(self.pin, callback=None)

class RPiPin:
  def __init__(self, board=None, pin=None, mode=None):
    self.board = board
    if(pin == None):
      self.pin = None
      return

    self.pin = pin
    self.mode = mode
    if(mode == Pin.OUT):
      GPIO.setup(self.pin, GPIO.OUT)
    elif(mode == Pin.IN):
      GPIO.setup(self.pin, GPIO.IN)
    elif(mode == Pin.PWM):#为了支持面向过程的4个API而设计的此选项，尽量避免使用,使用PWM类代替
      GPIO.setup(self.pin, GPIO.OUT)
      self.pwm=GPIO.PWM(self.pin, 1000)

  def value(self, v = None):
    if v is None:  #Read
      if self.mode == Pin.OUT:
        return self.val
      else:
        if self.pin is None:
          return
        self.val = GPIO.input(self.pin)
        return self.val
    else:  #Write
      self.val = v
      if(self.pin == None):
        return
      GPIO.output(self.pin,v)

  def on(self):
    self.val = 1
    if self.pin is None:
      return
    GPIO.output(self.pin, GPIO.HIGH)

  def off(self):
    self.val = 0
    if(self.pin == None):
      return
    GPIO.output(self.pin, GPIO.LOW)

  def irq(self, trigger, handler):
    GPIO.add_event_detect(self.pin, 30+trigger)
    GPIO.add_event_callback(self.pin, handler)
    #GPIO.add_event_detect(self.pin, 30+trigger, callback=handler)
  
  #这5个函数将打破原有的面向对象规则，请慎用
  #建议使用value方法 PWM和ADC类来替代这5个函数 
  def write_analog(self, duty):
    self.duty=duty
    self.pwm.start(duty)

  def write_digital(self, value):
    self.val = value
    if(self.pin == None):
      return
    GPIO.output(self.pin, value)

  def read_digital(self):
    if(self.pin == None):
      return
    self.val = GPIO.input(self.pin)
    return self.val

  def pin_mode(self, mode):
    if(mode == Pin.OUT):
      GPIO.setup(self.pin, GPIO.OUT)
    elif(mode == Pin.IN):
      GPIO.setup(self.pin, GPIO.IN)

class Pin:
  D0 = 0
  D1 = 1
  D2 = 2
  D3 = 3
  D4 = 4
  D5 = 5
  D6 = 6
  D7 = 7
  D8 = 8
  D9 = 9
  D10 = 10
  D11 = 11
  D12 = 12
  D13 = 13
  D14 = 14
  D15 = 15
  D16 = 16
  D17 = 17
  D18 = 18
  D19 = 19
  D20 = 20
  D21 = 21
  D22 = 22
  D23 = 23
  D24 = 24
  D25 = 25
  D26 = 26
  D27 = 27
  D28 = 28
  D29 = 29
  D30 = 30
  D31 = 31
  D32 = 32
  D33 = 33
  D34 = 34
  D35 = 35
  D36 = 36
  D37 = 37
  D38 = 38
  D39 = 39
  D40 = 40
  D41 = 41
  D42 = 42
  D43 = 43
  D44 = 44
  D45 = 45
  D46 = 46
  D47 = 47
  D48 = 48
  D49 = 49
  D50 = 50
  D51 = 51
  D52 = 52
  
  A0 = 100
  A1 = 101
  A2 = 102
  A3 = 103
  A4 = 104
  A5 = 105
  A6 = 106
  A7 = 107

  P0 = 0
  P1 = 1
  P2 = 2
  P3 = 3
  P4 = 4
  P5 = 5
  P6 = 6
  P7 = 7
  P8 = 8
  P9 = 9
  P10 = 10
  P11 = 11
  P12 = 12
  P13 = 13
  P14 = 14
  P15 = 15
  P16 = 16
  P17 = 17
  P18 = 18
  P19 = 19
  P20 = 20
  
  OUT = 0
  IN = 1
  IRQ_FALLING = 2
  IRQ_RISING = 1
  IRQ_DRAIN = 7
  PULL_DOWN = 1
  PULL_UP = 2
  PWM     = 0x10
  ANALOG  = 0x11

  def __init__(self, board=None, pin=None, mode=None):
    if isinstance(board, int):#兼容面向过程的4个api
      mode = pin
      pin = board
      board = gboard

    if board is None:
      board = gboard

    self.board = board
    if(pin == None):
      self.pin = None
      return

    self.pin,self.apin = get_pin(self.board, pin)
    self.mode = mode
    if self.board.boardname == "RPI":#RPi
      self.obj = RPiPin(board, pin, mode)
    else:
      self.obj = DuinoPin(board, pin,mode)

  def value(self, v = None):
    if v is None:  #Read
      return self.obj.value(v)
    else:  #Write
      self.obj.value(v)
      time.sleep(0.001)

  def on(self):
    self.val = 1
    if self.pin is None:
      return
    self.obj.on()

  def off(self):
    self.val = 0
    if(self.pin == None):
      return
    self.obj.off()

  def irq(self, trigger, handler):
    self.obj.irq(trigger, handler)

  #这5个函数将打破原有的面向对象规则，请慎用
  #建议使用value方法 PWM和ADC类来替代这5个函数
  def write_analog(self, duty):
    self.obj.write_analog(duty)

  def write_digital(self, value):
    self.obj.write_digital(value)

  def read_digital(self):
    return self.obj.read_digital()

  def read_analog(self):
    return self.obj.read_analog()

  def pin_mode(self, mode):
    self.obj.pin_mode(mode)


class HandpyMicrobitADC:
  def __init__(self, board=None, pin_obj=None):
    if isinstance(board, Pin):
      pin_obj = board
      board = gboard
    elif board is None:
      board = gboard
    
    self.board = board
    self.pin_obj = pin_obj
    self.board.board.set_pin_analog_input(self.pin_obj.apin, None)

  def read(self):
    return self.board.board.analog_read(self.pin_obj.apin)

class DuinoADC:
  def __init__(self, board=None, pin_obj=None):
    if isinstance(board, Pin):
      pin_obj = board
      board = gboard
    elif board is None:
      board = gboard
    
    self.board = board
    self.pin_obj = pin_obj
    self.board.board.set_pin_mode_analog_input(self.pin_obj.apin, None)

  def read(self):
    return self.board.board.analog_read(self.pin_obj.apin)
    
class ADC:
  def __init__(self, board=None, pin_obj=None):
    if isinstance(board, Pin):
      pin_obj = board
      board = gboard
    elif board is None:
      board = gboard
    
    self.board = board
    self.pin_obj = pin_obj
    if board.boardname == "HANDPY" or board.boardname == "MICROBIT":
      self.obj = HandpyMicrobitADC(board, pin_obj)
    else:
      self.obj = DuinoADC(board, pin_obj)

  def read(self):
    return self.obj.read()
'''
class ADC:
  def __init__(self, board=None, pin_obj=None):
    if isinstance(board, Pin):
      pin_obj = board
      board = gboard
    elif board is None:
      board = gboard
    
    self.board = board
    self.pin_obj = pin_obj
    self.board.board.set_pin_mode_analog_input(self.pin_obj.apin, None)

  def read(self):
    return self.board.board.analog_read(self.pin_obj.apin)
'''
class DuinoPWM:
  def __init__(self, board, pin_obj):
    self.board = board
    self.pin_obj = pin_obj
    self.freq_value = 100
    self.duty_value = 50
    self.board.board.set_pin_mode_pwm_output(self.pin_obj.pin)

  def freq(self, v=None):
    if v is None:
      return self.freq_value
    else:
      self.freq_value = v
    #f4（设置引脚模式） 04（引脚） 03（设置引脚模式为PWM模式）
    #e4（设置4号引脚的信息） 10（占空比：16%） 01（频率7~9位） 7f（频率0~6位） 
    if self.board.boardname == "UNO" or self.board.boardname == "LEONARDO":
      real_duty = int(self.duty_value / 255 * 100)
      self.board.board.pwm_write(self.pin_obj.pin, self.freq_value, real_duty)
    else:
      self.board.board.dfrobot_pwm_write(self.pin_obj.pin, self.freq_value, self.duty_value)

  def duty(self, v=None):
    if v == None:
      return self.duty_value
    else:
      self.duty_value = v
    if self.board.boardname == "UNO" or self.board.boardname == "LEONARDO":
      real_duty = int(self.duty_value / 255 * 100)
      self.board.board.pwm_write(self.pin_obj.pin, self.freq_value, real_duty)
    else:
      self.board.board.dfrobot_pwm_write(self.pin_obj.pin, self.freq_value, self.duty_value)

  def deinit(self):
    self.board.pin_obj.pin_mode(Pin.IN)

class RPiPWM:
  def __init__(self, board, pin_obj):
    self.pin_obj = pin_obj
    self.freq_value = 100
    self.duty_value = 50

    GPIO.setup(self.pin_obj.pin, GPIO.OUT)
    self.pwm = GPIO.PWM(self.pin_obj.pin, self.freq_value)
    #self.pwm.start(duty)
    self.isStart = False

  def freq(self, v=None):
    if v is None:
      return self.freq_value
    else:
      self.freq_value = v
      if v == 0:
        self.pwm.stop()
        self.isStart = False
      else:
        self.pwm.start(self.duty_value)
        self.pwm.ChangeFrequency(self.freq_value)
        self.isStart = True

  def duty(self, v=None):
    if v == None:
      return self.duty_value
    else:
      self.duty_value = v
    self.pwm.ChangeDutyCycle(self.duty_value)

  def deinit(self):
    self.pwm.stop()

class PWM:
  def __init__(self, board=None, pin_obj=None):
    if isinstance(board, Pin):
      pin_obj = board
      board = gboard
    elif board is None:
      board = gboard

    self.board = board
    self.pin_obj = pin_obj

    if self.board.boardname == "RPI":#RPi
      self.obj = RPiPWM(board, pin_obj)
    else:
      self.obj = DuinoPWM(board, pin_obj)

  def freq(self, v=None):
    if v is None:
      return self.obj.freq(v)
    else:
      self.obj.freq(v)

  def duty(self, v=None):
    if v == None:
      return self.obj.duty(v)
    else:
      self.obj.duty(v)

  def deinit(self):
    self.obj.deinit()

class DuinoSPI:
  def __init__(self, board, device_num=0, baudrate=10000):
    self.board = board
    self.device_num = device_num
    self.board.board.set_pin_mode_spi(device_num)

  def read(self, length, default_value=0xff):
    ret = self.board.board.spi_readbytes(self.device_num, length)
    return ret

  def readinto(self, buf):
    length = len(buf)
    buf=self.board.spi_read(self.device_num, length)

  def write(self, buf): #write some bytes on MOSI
    self.board.board.xfer3(buf)

  def write_readinto(self, wbuf, rbuf): # write to MOSI and read from MISO into the buffer
    rbuf=self.board.board.xfer3(wbuf)

class SoftSPI:
  def __init__(self, board, sck, mosi, miso, baudrate=100000, polarity=0, phase=0, bits=8):
    self.board = board
    self.mosi = mosi
    self.miso = miso
    self.sck = sck
    self.phase = phase
    self.mosi.value(0)
    self.sck.value(polarity)

  def read(self, num, default_value=0xff):
    ret = bytearray(num)
    for i in range (num):
      ret[i] = self._transfer(default_value)
    return ret

  def readinto(self, buf):
    num = len(buf)
    buf=self.read(num)

  def write(self, buf): #write some bytes on MOSI
    num = len(buf)
    for i in range (num):
      self._transfer(buf[i])

  def write_readinto(self, wbuf, rbuf): # write to MOSI and read from MISO into the buffer
    num = len(wbuf)
    for i in range (num):
      rbuf[i] = self._transfer(wbuf[i])

  def _transfer(self,data):
    ret = 0
    for i in range(8):
      self.mosi.value(1 if data&0x80 else 0)
      self.sck.value(0 if self.sck.value() else 1) #这样书写兼容了MODE0 和 MODE3
      self.sck.value(0 if self.sck.value() else 1)
      if self.miso:
        ret= ret<<1 + self.miso.value()
      data <<= 1
    return ret

class RPiSPI:
  def __init__(self, device_num=0, baudrate=31200000):
    self.spi = spidev.SpiDev(0, device_num)
    self.spi.open(0, device_num)
    self.spi.max_speed_hz = baudrate

  def read(self, num, default_value=0xff):
    ret = self.spi.readbytes(num)
    return ret

  def readinto(self, buf):
    num = len(buf)
    buf=self.read(num)

  def write(self, buf): #write some bytes on MOSI
    self.spi.xfer3(buf)

  def write_readinto(self, wbuf, rbuf): # write to MOSI and read from MISO into the buffer
    num = len(wbuf)

class SPI:
  # spi四种模式SPI的相位(CPHA)和极性(CPOL)分别可以为0或1，对应的4种组合构成了SPI的4种模式(mode)
  # Mode 0 CPOL=0, CPHA=0  ->  第一个跳变，即上升沿采样
  # Mode 1 CPOL=0, CPHA=1  ->  第二个跳变，即下降沿采样
  # Mode 2 CPOL=1, CPHA=0  ->  第一个跳变，即下降沿采样
  # Mode 3 CPOL=1, CPHA=1  ->  第二个跳变，即上升沿采样
  # 时钟极性CPOL: 即SPI空闲时，时钟信号SCLK的电平 (1:空闲时高电平; 0:空闲时低电平)
  # 时钟相位CPHA: 即SPI在SCLK第几个边沿开始采样 (0:第一个边沿开始; 1:第二个边沿开始)
  # 默认设置为MODE 0 因为大部分的外设使用的是MODE 0
  def __init__(self, board=None, device_num=0, sck=None, mosi=None, miso=None, cs=None, baudrate=100000, polarity=0, phase=0, bits=8):
    if isinstance(board, int):
      device_num = board
      board = gboard
    elif board is None:
      board = gboard
    self.board = board

    if self.board.spi[device_num] is None:
      if mosi:  #SoftSPI
        self.board.spi[device_num] = SoftSPI(board, sck, mosi, miso, cs, baudrate, polarity, phase, bits)
      elif self.board.boardname == "RPI":  #RPiSPI
        self.board.spi[device_num] = RPiSPI(device_num)
      else:  #DuinoSPI
        self.board.spi[device_num] = DuinoSPI(self, device_num)
    self.obj = self.board.spi[device_num]

  def read(self, num, default_value=0xff):
    return self.obj.read(num, default_value)

  def readinto(self, buf):
    self.obj.readinto(buf)

  def write(self, buf): #write some bytes on MOSI
    self.obj.write(buf)

  def write_readinto(self, wbuf, rbuf): # write to MOSI and read from MISO into the buffer
    self.obj.writeinto(wbuf, rbuf)

class DuinoI2C:
  def __init__(self, board, bus_num):
    self.board = board
    self.board.board.set_pin_mode_i2c()

  def scan(self):
    plist = self.board.board.i2c_scan()
    return plist

  def writeto(self, i2c_addr, value):
    self.board.board.i2c_write(i2c_addr, value)

  def readfrom(self, i2c_addr, read_byte):
    return self.board.board.i2c_addr_read(i2c_addr, read_byte)

  def readfrom_mem(self, i2c_addr, reg, read_byte):
    return self.board.board.i2c_read(i2c_addr, reg, read_byte, None)

  def readfrom_mem_restart_transmission(self, i2c_addr, reg, read_byte):
    return self.board.board.i2c_read_restart_transmission(i2c_addr, reg, read_byte, None)

  def writeto_mem(self, i2c_addr, reg, value):
    self.board.board.i2c_write(i2c_addr, [reg]+list(value))

class RPiI2C:
  def __init__(self, board, bus_num):
    self.bus_num = bus_num
    self.i2c = smbus.SMBus(bus_num)

  def scan(self):
    plist=[]
    for i in range(127):
      try:
        self.i2c.write_quick(i)
        plist.append(i)
      except Exception as e:
        pass
    return plist

  def writeto(self, i2c_addr, value):
    self.i2c.write_i2c_block_data(i2c_addr, value[0], list(value[1:]))

  def readfrom(self, i2c_addr, read_byte):
    pass

  def readfrom_mem(self, i2c_addr, reg, read_byte):
    return self.i2c.read_i2c_block_data(i2c_addr, reg, read_byte)

  def readfrom_mem_restart_transmission(self, i2c_addr, reg, read_byte):
    return self.i2c.read_i2c_block_data(i2c_addr, reg, read_byte)

  def writeto_mem(self, i2c_addr, reg, value):
    self.i2c.write_i2c_block_data(i2c_addr, reg, list(value))

class I2C:
  def __init__(self, board=None, bus_num=0):
    if isinstance(board, int):
      bus_num = board
      board = gboard
    elif board is None:
      board = gboard
    
    self.board = board
    if self.board.i2c[bus_num] is None:
      self.bus_num = bus_num
      if self.board.boardname == "RPI":
        self.board.i2c[bus_num] = RPiI2C(board, bus_num)
      else:
        self.board.i2c[bus_num] = DuinoI2C(board, bus_num)
    self.obj = self.board.i2c[bus_num]

  def scan(self):
    return self.obj.scan()

  def writeto(self, i2c_addr, value):
    self.obj.writeto(i2c_addr, value)

  def readfrom(self, i2c_addr, read_byte):
    return self.obj.readfrom(i2c_addr, read_byte)

  def readfrom_mem(self, i2c_addr, reg, read_byte):
    return self.obj.readfrom_mem(i2c_addr, reg, read_byte)

  def readfrom_mem_restart_transmission(self, i2c_addr, reg, read_byte):
    return self.obj.readfrom_mem_restart_transmission(i2c_addr, reg, read_byte)

  def writeto_mem(self, i2c_addr, reg, value):
    return self.obj.writeto_mem(i2c_addr, reg, value)

class RPiIRRecv:
  def __init__(self, board, pin_obj):
    self.pin_obj = pin_obj

  def read(self):
    return None

class DuinoIRRecv:
  def __init__(self, board, pin_obj,callback):
    self.board = board
    self.pin_obj = pin_obj
    self.board.board.set_pin_mode_ir_recv(self.pin_obj.pin, callback)

  def read(self):
    return self.board.board.ir_read(self.pin_obj.pin)


class IRRecv:
  def __init__(self, board=None, pin_obj=None, callback=None):
    if isinstance(board, Pin):
      callback = pin_obj
      pin_obj = board
      board = gboard
    elif board is None:
      board = gboard
    
    self.board = board
    if self.board.boardname == "RPI":
      self.obj = RPiIRRecv(board, pin_obj, callback)
    else:
      self.obj = DuinoIRRecv(board, pin_obj, callback)

  def read(self):
    return self.obj.read()


class RPiIRRemote:
  def __init__(self, board, pin_obj):
    self.pin_obj = pin_obj

  def send(self, value):
    return None

class DuinoIRRemote:
  def __init__(self, board, pin_obj,callback=None):
    self.board = board
    self.pin_obj = pin_obj
#    self.board.board.set_pin_mode_ir_recv(self.pin_obj.pin, callback)

  def send(self, value):
    return self.board.board.ir_send(self.pin_obj.pin, value)

class IRRemote:
  def __init__(self, board=None, pin_obj=None):
    if isinstance(board, Pin):
      pin_obj = board
      board = gboard
    elif board is None:
      board = gboard
    
    self.board = board
    if self.board.boardname == "RPI":
      self.obj = RPiIRRemote(board, pin_obj)
    else:
      self.obj = DuinoIRRemote(board, pin_obj)

  def send(self, value):
    return self.obj.send(value)


class RPiTone:
  def __init__(self, board, pin_obj):
    self.board = board
    self.pwm = PWM(pin_obj = pin_obj)
    self.freq_value = 0

  def on(self):
    self.pwm.freq(self.freq_value)

  def off(self):
    self.pwm.freq(0)

  def freq(self, v=None):
    if v is None:
      return self.freq_value
    else:
      self.freq_value = v
      self.pwm.freq(v)

  def tone(self, freq, duration):
#    self.pwm.play_tone(self.pin_obj.pin, freq, duration) 
     pass

class DuinoTone:
  def __init__(self, board, pin_obj):
    self.board = board
    self.pin_obj = pin_obj
    self.board.board.set_pin_mode_tone(self.pin_obj.pin)
    self.freq_value = 100
    
  def on(self):
    self.board.board.play_tone(self.pin_obj.pin, self.freq_value, 0)

  def off(self):
    self.board.board.play_tone(self.pin_obj.pin, 0, 0)

  def freq(self, v=None):
    if v == None:
      return self.freq_value
    else:
      self.freq_value = v

  def tone(self, freq, duration):
    self.board.board.play_tone(self.pin_obj.pin, freq, duration)

class Tone:
  def __init__(self, board=None, pin_obj=None):
    if isinstance(board, Pin):
      pin_obj = board
      board = gboard
    elif board is None:
      board = gboard

    self.board = board
    if self.board.boardname == "RPI":
      self.obj = RPiTone(board, pin_obj)
    else:
      self.obj = DuinoTone(board, pin_obj)
      
  def on(self):
    self.obj.on()

  def off(self):
    self.obj.off()

  def freq(self, v=None):
    if v == None:
      return self.obj.freq(v)
    else:
     self.obj.freq(v)

  def tone(self, freq, duration):
    self.obj.tone(freq=freq,duration=duration)

class Servo:
  def __init__(self, board=None, pin_obj=None):
    if isinstance(board, Pin):
      pin_obj = board
      board = gboard
    elif board is None:
      board = gboard

    self.board = board
    self.pin_obj = pin_obj
    if self.board.boardname == "RPI":
      GPIO.setup(self.pin_obj.pin, GPIO.OUT)
      self.pwm=GPIO.PWM(self.pin_obj.pin, 50)
      self.pwm.start(0)
    else:
      self.board.board.set_pin_mode_servo(self.pin_obj.pin)
      self.board.board.set_mode_servo(self.pin_obj.pin)
      
  def write_angle(self, value):
    self.angle(value)

  def angle(self, _angle):
    if self.board.boardname == "RPI":
      duty = int(_angle*(10.0/180.0)+2.5)
      self.pwm.ChangeDutyCycle(duty)
    elif self.board.boardname == "HANDPY" or self.board.boardname == "MICROBIT":
      if self.pin_obj.pin < 16:
        self.board.board.servo_write(self.pin_obj.pin, _angle)
      else:
        self.board.board.dfrobot_servo_write(self.pin_obj.pin, _angle)
    else:
      self.board.board.servo_write(self.pin_obj.pin, _angle)
    
  def detach(self):
    if self.boardname == "RPI":
      self.pwm.stop()
      self.pwm = None
      GPIO.setup(self.pin_obj.pin, GPIO.IN)
    else:
      self.board.set_pin_mode_digital_input(self.pin_obj.pin, callback=None)

class NeoPixel(object):
  def __init__(self, board=None, pin_obj=None, num=None):
    if isinstance(board, Pin):
      num = pin_obj
      pin_obj = board
      board = gboard
    elif board is None:
      board = gboard

    self.pin_obj  = pin_obj
    self.board = board
    self.num = num
    self.__data = [(0,0,0) for i in range(num)]
    #self.board.board.set_pin_mode_neo(self.pin_obj.pin)
    self.board.board.neopixel_config(self.pin_obj.pin,self.num)
    time.sleep(0.1)

  def __repr__(self):
    return 'pixel data (%s)' % self.__data
 
  def __getitem__(self, i):
    return self.__data[i]  # 返回data绑定列表中的第i个元素
 
  def __setitem__(self, i, v):
    #print(i,v)
    self.__data[i]=v
    self.write(i,v)

  def write(self , index, r, g=None, b=None):
    if isinstance(r,tuple):
      b=r[2]
      g=r[1]
      r=r[0]
    color = (r<<16) + (g<<8) + b
    self.board.board.neopixel_write(self.pin_obj.pin, index, color)

  def rainbow(self , start, end, hsv_start, hsv_end):
    self.board.board.neopixel_set_rainbow(self.pin_obj.pin, start, end, hsv_start, hsv_end)

  def shift(self , n):
    self.board.board.neopixel_shift(self.pin_obj.pin, n)

  def rotate(self , n):
    self.board.board.neopixel_rotate(self.pin_obj.pin, n)

  def range_color(self, start, end, color):
    self.board.board.neopixel_set_range_color(self.pin_obj.pin, start, end, color)
    
#  def bar_graph(self, start, end, numerator, denominator):
#    self.board.board.set_bar_graph(self.pin_obj.pin, start, end, numerator, denominator)

  def clear(self):
    self.board.board.neopixel_set_range_color(self.pin_obj.pin, 0, self.num-1, 0)

class DHT11:
  def __init__(self,board=None, pin_obj=None):
    if isinstance(board, Pin):
      pin_obj = board
      board = gboard
    elif board is None:
      board = gboard

    self.board = board
    self.pin_obj = pin_obj
    self.type = 11
    self.board.board.set_pin_mode_dht(self.pin_obj.pin, self.type, differential=.01)
    
  def measure(self):
    self.value = self.board.board.dht_read(self.pin_obj.pin)

  def temp_c(self):
    return self.board.board.dht_read(self.pin_obj.pin)[1]

  def humidity(self):
    return self.board.board.dht_read(self.pin_obj.pin)[0]

class DHT22:
  def __init__(self,board=None, pin_obj=None):
    if isinstance(board, Pin):
      pin_obj = board
      board = gboard
    elif board is None:
      board = gboard

    self.board = board
    self.pin_obj = pin_obj
    self.type = 22
    self.board.board.set_pin_mode_dht(self.pin_obj.pin, self.type, differential=.01)

  def measure(self):
    self.value = self.board.board.dht_read(self.pin_obj.pin)

  def temp_c(self):
    return self.board.board.dht_read(self.pin_obj.pin)[1]

  def humidity(self):
    return self.board.board.dht_read(self.pin_obj.pin)[0]

class SR04_URM10:
  def __init__(self,board=None, trigger_pin_obj=None, echo_pin_obj=None):
    if isinstance(board, Pin):
      echo_pin_obj = trigger_pin_obj
      trigger_pin_obj = board
      board = gboard
    elif board is None:
      board = gboard

    self.board  = board
    self.trigger_pin_obj = trigger_pin_obj
    self.echo_pin_obj = echo_pin_obj
    self.board.board.set_pin_mode_sonar(self.trigger_pin_obj.pin, self.echo_pin_obj.pin)

  def distance_cm(self):
    return self.board.board.sonar_read(self.trigger_pin_obj.pin)[0]

class DS18B20:
  def __init__(self, board=None, pin_obj=None):
    if isinstance(board, Pin):
      pin_obj = board
      board = gboard
    elif board is None:
      board = gboard
    
    self.board = board
    self.pin_obj = pin_obj
    self.board.board.set_pin_mode_DS18B20(self.pin_obj.pin)
    
  def temp_c(self):
    return self.board.board.ds18b20_read(self.pin_obj.pin)

class AUDIO:
  def __init__(self, board=None, strobe=None, RST=None, DC=None):
    if isinstance(board, int):
      strobe_pin = board
      RST_pin = strobe
      DC_pin = RST
      board = gboard
    elif board is None:
      board = gboard
    
    self.board = board
    self.strobe_pin = strobe_pin
    self.RST_pin = RST_pin
    self.DC_pin,self.DC_apin = get_pin(self.board, DC_pin)
    self.RST_pin,self.RST_apin = get_pin(self.board, RST_pin)
    self.strobe_pin,self.strobe_apin = get_pin(self.board, strobe_pin)
    self.board.board.set_audio_init(self.strobe_pin, self.RST_pin, self.DC_pin)
    
  def read_freq(self):
    return self.board.board.audio_analyzer_read_freq()

class HX711:
  def __init__(self, board, dout_pin, sck_pin = 2121, scale = None):
    if isinstance(board, int):
      scale = sck_pin
      sck_pin = dout_pin
      dout_pin = board
      board = gboard
    elif board is None:
      board = gboard
    
    self.board = board
    self.dout_pin = dout_pin
    self.sck_pin = sck_pin
    self.dout_pin,self.dout_apin = get_pin(self.board, dout_pin)
    self.sck_pin,self.sck_apin = get_pin(self.board, sck_pin)
    self.scale = scale
    self.board.board.set_hx711_init(self.dout_pin, self.sck_pin, self.scale)
  
  def read_weight(self):
    return self.board.board.hx711_read_weight(self.dout_pin)
    
class HEARTRATE:
  def __init__(self, board, mode, pin=None):
    if isinstance(board, int):
      self.mode = board
      self.pin = mode
      board = gboard
    elif board is None:
      board = gboard
    
    self.board = board
    self.rpin,self.apin = get_pin(self.board, self.pin)
    self.board.board.heartrate_init(self.rpin)
    
  def get_rate(self):
    return self.board.board.get_heartrate_value(self.mode, self.rpin)
    
class TCP:
  def __init__(self, board = None):
    board = gboard
    self.board = board
    
  def set_ssid(self, ssid):
    self.ssid = ssid
    self.board.board.tcp_set_ssid(self.ssid)
  
  def set_password(self, password):
    self.password = password
    self.board.board.tcp_set_password(self.password)
    
  def connect_wifi(self):
    self.board.board.tcp_connect_wifi()
  
  def get_ip_port(self):
    ip,port = self.board.board.tcp_ret_ip_port()
    return ip,port

class HSensor:
  def __init__(self, board=None):
    if board == None:
      board = gboard
    self.board = board
    self.board.board.esp32_report_sensor()
  
  def buttonA_is_pressed(self):
    return self.board.board.esp32_buttonA_is_pressed()
  
  def buttonB_is_pressed(self):
    return self.board.board.esp32_buttonB_is_pressed()

  def buttonAB_is_pressed(self):
    return self.board.board.esp32_buttonAB_is_pressed()
    
  def touch_P(self):
    return self.board.board.esp32_touchP()
  
  def touch_Y(self):
    return self.board.board.esp32_touchY()
  
  def touch_T(self):
    return self.board.board.esp32_touchT()
  
  def touch_H(self):
    return self.board.board.esp32_touchH()
  
  def touch_O(self):
    return self.board.board.esp32_touchO()
  
  def touch_N(self):
    return self.board.board.esp32_touchN()
  
  def set_touch_threshold(self, obj="", value=30):
    if value > 80:
      value = 80
    elif value < 0:
      value = 0
    data = obj.upper()
    self.board.board.esp32_set_touch_threshold(data, value)
  
  def read_touch_P(self):
    return self.board.board.esp32_read_touch_P()
  
  def read_touch_Y(self):
    return self.board.board.esp32_read_touch_Y()
  
  def read_touch_T(self):
    return self.board.board.esp32_read_touch_T()
  
  def read_touch_H(self):
    return self.board.board.esp32_read_touch_H()
  
  def read_touch_O(self):
    return self.board.board.esp32_read_touch_O()
  
  def read_touch_N(self):
    return self.board.board.esp32_read_touch_N()
  
  def read_sound(self):
    return self.board.board.esp32_read_sound()
  
  def read_light(self):
    return self.board.board.esp32_read_light()
  
  def get_accelerometer_X(self):
    return self.board.board.esp32_get_accelerometer_X()
  
  def get_accelerometer_Y(self):
    return self.board.board.esp32_get_accelerometer_Y()
  
  def get_accelerometer_Z(self):
    return self.board.board.esp32_get_accelerometer_Z()
  
  def get_accelerometer_strength(self):
    return round(self.board.board.esp32_get_accelerometer_strength(),2)
  
class HScreen:
  def __init__(self, board=None):
    if board == None:
      board = gboard
    self.board = board

  def display_in_line(self, data, line):
    try:
      if line < 1 or line > 4:
        raise ValueError("line must be a number greater than 0 and less than or equal to 4")
    except ValueError as e:
      print("Throw an exception:",repr(e))
    else:
      buf = []
      text = str(data)
      text = text.encode(encoding='UTF-8',errors='strict')
      for i in text:
        buf.append(i)
      length = len(buf)
      try:
        if length > 500:
          raise ValueError("Please enter less than 500")
      except ValueError as e:
        print("Throw an exception:",repr(e))
      else:
        self.board.board.esp32_display_in_line(buf, line, length)

  def display_clear_in_line(self, line):
    self.board.board.esp32_display_clear_in_line(line)
  
  def display_in_XY(self, data, x, y):
    try:
      if x < 0 or x > 127 or y < 0 or y > 63:
        raise ValueError("Please input x:0-127 y:0-63")
    except ValueError as e:
      print("Throw an exception:",repr(e))
    else:
      buf = []
      text = str(data)
      text = text.encode(encoding='UTF-8',errors='strict')
      for i in text:
        buf.append(i)
      length = len(buf)
      try:
        if length > 500:
          raise ValueError("Please input less than 500")
      except ValueError as e:
        print("Throw an exception:",repr(e))
      else:
        self.board.board.esp32_display_in_XY(x, y, buf, length)
  
  def fill_screen(self, color = "black"):
    color = str(color)
    color = color.upper()
    try:
      if color != "BLACK" and color != "WHITE":
        raise ValueError("Please input white or black")
    except ValueError as e:
      print("Throw an exception:",repr(e))
    else:
      color = 0 if color == "BLACK" else 1
      self.board.board.esp32_fill_screen(color)

  def screen_rotation(self, angle = 0):
    try:
      if angle != 0 and angle != 180:
        raise ValueError("Please input 0 or 180")
    except ValueError as e:
      print("Throw an exception:",repr(e))
    else:
      angle = 2 if angle == 180 else 0
      self.board.board.esp32_screen_rotation(angle)

  def point_drawing(self, x, y):
    try:
      if x < 0 or x > 127 or y < 0 or y > 63:
        raise ValueError("Please input x:0-127 y:0-63")
    except ValueError as e:
      print("Throw an exception:",repr(e))
    else:
      self.board.board.esp32_point_drawing(x, y)

  def set_line_width(self, lineW):
    try:
      if lineW < 1 or lineW > 128:
        raise ValueError("Please input x:0-127 y:0-63")
    except ValueError as e:
      print("Throw an exception:",repr(e))
    else:
      self.board.board.esp32_set_line_width(lineW)

  def line_drawing(self, x1, y1, x2, y2):
    try:
      if x1 < 0 or x1 > 127 or y1 < 0 or y1 > 63 or x2 < 0 or x2 > 127 or y2 < 0 or y2 > 63:
        raise ValueError("Please input x:0-127 y:0-63")
    except ValueError as e:
      print("Throw an exception:",repr(e))
    else:
      self.board.board.esp32_line_drawing(x1, y1, x2, y2)

  def circle_drawing(self, x, y, r):
    self.board.board.esp32_circle_drawing(x, y, 0 ,r)

  def circle_drawing_fill(self, x, y, r):
    self.board.board.esp32_circle_drawing_fill(x, y, 1 ,r)

  def rectangle_drawing(self, x, y, width, height):
    self.board.board.esp32_rectangle_drawing(x, y, width, height, 0)

  def rectangle_drawing_fill(self, x, y, width, height):
    self.board.board.esp32_rectangle_drawing_fill(x, y, width, height, 1)
  
  def display_image(self, x, y, width, height, path):
    try:
      if width < 0 or height < 0  or x < 0 or y < 0 or height > 64 or y >= 64 or width > 128 or x >= 128:
        raise ValueError("Please input width, x:0-127 height, y:0-63")
    except ValueError as e:
        print("Throw an exception:",repr(e))
    else:
      img_src = Image.open(path)
      im = img_src.resize((width,height))
      img_src = im.convert('L')
      aa = img_src.getdata()
      sequ0 = list(aa)
      data = []
      threshold = 130
      for i in range(height):
        j = 0; k = 0; l=0
        for j in range(width//8):
          byte = 0
          for k in range(8):
            byte <<= 1
            bit = sequ0[i*width+j*8+k]
            byte |= (1 if bit>threshold else 0)
          data .append(byte)
        byte = 0
        for l in range(width%8):
          byte <<= 1
          bit = sequ0[i*width+j*8+k + l]
          byte |= (1 if bit>threshold else 0)
        for m in range(7-l):
          byte <<= 1
        if width%8:
          data.append(byte)
      width_bytes = len(data) // height
      max_height = 128 // width_bytes
      for ii in range(height // max_height):
        time.sleep(0.1)
        self.board.board.esp32_display_image(x, y+max_height*ii, width, max_height, data[max_height * width_bytes * ii : max_height * width_bytes*(ii+1)], max_height * width_bytes)
      time.sleep(0.1)
      if height % max_height:
        self.board.board.esp32_display_image(x, y+max_height * (height // max_height), width, height % max_height, data[len(data) -((height % max_height) * width_bytes) : len(data)], (height % max_height) * width_bytes)
      time.sleep(0.1)
      self.board.board.esp32_oled12864_show(x, y, width, height)

class LED:
  def __init__(self, board=None):
    if board == None:
      board = gboard
    self.board = board
    self.board.board.esp32_report_sensor()
  
  def set_rgb_color(self, index, r, g, b):
    try:
      if index < -1 or index > 2 or r < 0 or r > 255 or g < 0 or g > 255 or b < 0 or b > 255:
         raise ValueError("Please input (-1,0,1,2) rgb(0-255)")
    except ValueError as e:
      print("Throw an exception:",repr(e))
    else:
      if index == -1:
        index = 3
      color = r << 16 | g << 8 | b
      self.board.board.esp32_set_lights_color(index, color)

  def rgb_disable(self, index):
    try:
      if index < -1 or index > 2:
        raise ValueError("Please input (-1,0,1,2)")
    except ValueError as e:
      print("Throw an exception:",repr(e))
    else:
      if index == -1:
        index = 3
      self.board.board.esp32_rgb_disable(index, 0)
  
  def set_brightness(self, value):
    try:
      if value < 0 or value > 9:
        raise ValueError("Please input 0-9")
    except ValueError as e:
      print("Throw an exception:",repr(e))
    else:
      self.board.board.esp32_set_brightness(value)
  
  def get_brightness(self):
    return self.board.board.esp32_get_brightness()

class Music:
  sound = {
    "DADADADUM": 0,
    "ENTERTAINER": 1,
    "PRELUDE": 2,
    "ODE": 3,
    "NYAN": 4,
    "RINGTONE": 5,
    "FUNK": 6,
    "BLUES": 7,
    "BIRTHDAY": 8,
    "WEDDING": 9,
    "FUNERAL": 10,
    "PUNCHLINE": 11,
    "BADDY": 12,
    "CHASE": 13,
    "BA_DING": 14,
    "WAWAWAWAA": 15,
    "JUMP_UP": 16,
    "JUMP_DOWN": 17,
    "POWER_UP": 18,
    "POWER_DOWN": 19
  }
  music_map = {
    "C/C3":131,
    "D/D3":147,
    "E/E3":165,
    "F/F3":175,
    "G/G3":196,
    "A/A3":220,
    "B/B3":247,
    "C/C4":262,
    "D/D4":294,
    "E/E4":330,
    "F/F4":349,
    "G/G4":392,
    "A/A4":440,
    "B/B4":494,
    "C/C5":523,
    "D/D5":587,
    "E/E5":659,
    "F/F5":698,
    "G/G5":784,
    "A/A5":880,
    "B/B5":988,
    "C#/C#3":139,
    "D#/D#3":156,
    "F#/F#3":185,
    "G#/G#3":208,
    "A#/A#3":233,
    "C#/C#4":277,
    "D#/D#4":311,
    "F#/F#4":370,
    "G#/G#4":415,
    "A#/A#4":466,
    "C#/C#5":554,
    "D#/D#5":622,
    "F#/F#5":740,
    "G#/G#5":831,
    "A#/A#5":932
  }
  beats_map = {
    1/4: 1,
    1/2: 2,
    3/4: 3,
    1: 4,
    1.5: 6,
    2: 8,
    3: 12,
    4: 16
  }
  microbit_map = {
    1: 1,
    1/2: 2,
    1/4: 4,
    1/8: 8,
    1/16: 16,
    2: 32,
    4: 64
  }
  def __init__(self, board=None):
    if board == None:
      board = gboard
    self.board = board
    self.speed = 120
  
  def music_set_tempo(self, ticks, tempo):
    self.board.board.esp32_music_set_tempo(0x7f, ticks, tempo)
  
  def set_buzzer_freq(self, note, beat):
    note = note.upper()
    _note = self.music_map[note]
    if self.beats_map[beat]:
      _beat = self.beats_map[beat]
    else:
      if beat > 0.125 and beat <= 0.25:
        _beat = 1
      elif beat > 0.25 and beat <= 0.5:
        _beat = 2
      elif beat > 0.5 and beat <=0.75:
        _beat = 3
      elif beat > 0.75 and beat <= 1:
        _beat = 4
      elif beat > 1 and beat <= 1.5:
        _beat = 6
      elif beat > 1.5 and beat <= 2:
        _beat = 8
      elif beat > 2 and beat <= 3:
        _beat = 12
      elif beat > 3 and beat <= 4:
        _beat = 16
      else:
        _beat = 4
    self.board.board.esp32_set_buzzer_freq(0x7f, _note, _beat)
  
  def background_set_buzzer_freq(self, note):
    _note = self.music_map[note]
    self.board.board.esp32_set_buzzer_freq(0x7f, _note, 0)

  def stop_background_buzzer_freq(self):
    self.board.board.esp32_stop_background_buzzer_freq()
  
  def play_music_background(self, pin, music):
    try:
      val = self.sound[music]
    except:
      print("please input correct music")
    else:
      self.board.board.set_pin_mode_digital_output(pin)
      time.sleep(0.1)
      self.board.board.microbit_play_music_background(pin, val, 0)
  
  def play_music_until_end(self, pin, music):
    try:
      val = self.sound[music]
    except:
      print("please input correct music")
    else:
      self.board.board.set_pin_mode_digital_output(pin)
      time.sleep(0.1)
      self.board.board.microbit_play_music_background(pin, val, 1)
  
  def play_buzzer_freq(self, pin, note, beat):
    try:
      note = note.upper()
      _note = self.music_map[note]
      if self.microbit_map[beat]:
        _beat = self.microbit_map[beat]
      else:
        if (num > 0 and num <= 0.0625): _beat = 16
        elif (num > 0.0625 and num <= 0.125): _beat = 8
        elif (num > 0.125 and num <= 0.25): _beat = 4
        elif (num > 0.25 and num <= 0.5): _beat = 2
        elif (num > 0.5 and num <= 1): _beat = 1
        elif (num > 1 and num <= 2): _beat = 32
        elif (num > 2 and num <= 4): _beat = 64
        else: _beat = 1
    except:
      print("please input correct param")
    else:
      self.board.board.microbit_play_buzzer_freq(pin, _note, _beat)
  
  def change_speed(self, val):
    self.speed += val
    if self.speed < 4:
      self.speed = 4
    if self.speed > 400:
      self.speed = 400
    self.board.board.microbit_set_speed(self.speed)

  def set_speed(self, val):
    self.speed = val
    if self.speed < 4:
      self.speed = 4
    if self.speed > 400:
      self.speed = 400
    self.board.board.microbit_set_speed(self.speed)
  
  def get_speed(self):
    return self.speed

class MScreen:
  value = {   
  "HEART":         "0101010101100010101000100",
  "HEART_SMALL":   "0000001010011100010000000",
  "ARROW_N":       "0010001110101010010000100",
  "ARROW_S":       "0010000100101010111000100",
  "ARROW_W":       "0010001000111110100000100",
  "ARROW_E":       "0010000010111110001000100",
  "ARROW_NE":      "0011100011001010100010000",
  "ARROW_NW":      "1110011000101000001000001",
  "ARROW_SE":      "1000001000001010001100111",
  "ARROW_SW":      "0000100010101001100011100",
  "YES":           "0000000001000101010001000",
  "NO":            "1000101010001000101010001",
  "HAPPY":         "0000001010000001000101110",
  "SAD":           "0000001010000000111010001",
  "ANGRY":         "1000101010000001111110101",
  "SILLY":         "1000100000111110010100111",
  "SMILE":         "0000000000000001000101110",
  "ASLEEP":        "0000011111000000111000000",
  "SQUARE":        "1111110001100011000111111",
  "SQUARE_SMALL":  "0000001110010100111000000",
  "TRIANGLE":      "0000000100010101111100000",
  "TRIANGLE_LEFT": "1000011000101001001011111",
  "DIAMOND_SMALL": "0000000100010100010000000",
  "MUSIC_CROTCHET":"0010000100001001110011100",
  "MUSIC_QUAVER":  "0010000111001011110011100",
  "MUSIC_QUAVERS": "0111101001010011101111011",
  "CLOCK1":        "0001000010001000000000000",
  "CLOCK2":        "0000000011001000000000000",
  "CLOCK3":        "0000000000001110000000000",
  "CLOCK4":        "0000000000001000001100000",
  "CLOCK5":        "0000000000001000001000010",
  "CLOCK6":        "0000000000001000010000100",
  "CLOCK7":        "0000000000001000100001000",
  "CLOCK8":        "0000000000001001100000000",
  "CLOCK9":        "0000000000111000000000000",
  "CLOCK10":       "0000011000001000000000000",
  "CLOCK11":       "0100001000001000000000000",
  "CLOCK12":       "0010000100001000000000000",
  "SKULL":         "0111010101111110111001110",
  "BUTTERFLY":     "1101111111001001111111011",
  "CHESSBOARD":    "0101010101010101010101010",
  "CONFUSED":      "0000001010000000101010101",
  "COW":           "1000110001111110111000100",
  "DIAMOND":       "0010001010100010101000100",
  "DUCK":          "0110011100011110111000000",
  "FABULOUS":      "1111111011000000101001110",
  "GHOST":         "1111110101111111111110101",
  "GIRAFFE":       "1100001000010000111001010",
  "HOUSE":         "0010001110111110111001010",
  "MEH":           "0101000000000100010001000",
  "PACMAN":        "0111111010111001111001111",
  "PITCHFORK":     "1010110101111110010000100",
  "RABBIT":        "1010010100111101101011110",
  "ROLLERSKATE":   "0001100011111111111101010",
  "SNAKE":         "1100011011010100111000000",
  "STICKFIGURE":   "0010011111001000101010001",
  "SURPRISED":     "0101000000001000101000100",
  "SWORD":         "0010000100001000111000100",
  "TARGET":        "0010001110110110111000100",
  "TORTOISE":      "0000001110111110101000000",
  "TSHIRT":        "1101111111011100111001110",
  "UMBRELLA":      "0111011111001001010001100",
  "XMAS":          "0010001110001000111011111"
  }
  def __init__(self, board=None):
    if board == None:
      board = gboard
    self.board = board
  
  def show_shape(self, shape):
    shape = shape.upper()
    data = self.value[shape]
    buf = []
    for i in range(0, 21, 5):
      buf.append(data[i:i+5])
    data = []
    for i in buf:
      data.append(int(i,2))
    self.board.board.microbit_show_shape(data)
  
  def show_font(self, data):
    data = str(data)
    if len(data) > 20:
      data = data[0:20]
    buf = []
    for i in data:
      buf.append(ord(i))
    buf.append(0)
    self.board.board.microbit_show_font(buf)
  
  def control_light_on(self, x, y):
    try:
      if x < 0 or y < 0 or x > 4 or y > 4:
        raise ValueError("Please input 0-4")
    except ValueError as e:
      print("Throw an exception:",repr(e))
    else:
      self.board.board.microbit_control_light_on(x, y, 1)
  
  def control_light_off(self, x, y):
    try:
      if x < 0 or y < 0 or x > 4 or y > 4:
        raise ValueError("Please input 0-4")
    except ValueError as e:
      print("Throw an exception:",repr(e))
    else:
      self.board.board.microbit_control_light_on(x, y, 0)

  def set_light_brightness(self, brightness):
    try:
      if brightness < 0 or brightness > 9 :
        raise ValueError("Please input 0-9")
    except ValueError as e:
      print("Throw an exception:",repr(e))
    else:
      if brightness == 0:
        val = 0
      elif brightness == 9:
        val = 255
      else:
        val = brightness * 28
      self.board.board.microbit_set_light_brightness(val)
  
  def hide_all_lights(self):
    self.board.board.microbit_hide_all_lights()

class MSensor:
  _gesture = {
    1 :'Logo up',
    2 :'Logo down',
    3 :'Tilt left',
    4 :'Tilt right',
    5 :'Face up',
    6 :'Face down',
    7 :'Freefall',
    8 :'3g',
    9 :'6g',
    10:'8g',
    11:'shake' 
  }
  def __init__(self, board=None):
    if board == None:
      board = gboard
    self.board = board
    self.board.board.microbit_report_sensor()

  def buttonA_is_pressed(self):
    return self.board.board.microbit_buttonA_is_pressed()
  
  def buttonB_is_pressed(self):
    return self.board.board.microbit_buttonB_is_pressed()

  def buttonAB_is_pressed(self):
    return self.board.board.microbit_buttonAB_is_pressed()
  
  def touch0(self):
    return self.board.board.microbit_touch0()
  
  def touch1(self):
    return self.board.board.microbit_touch1()
  
  def touch2(self):
    return self.board.board.microbit_touch2()
  
  def get_gesture(self):
    val = self.board.board.microbit_get_gesture()
    if val:
      return self._gesture[val]
    else:
      return "Failure to recognize gesture"
  
  def get_brightness(self):
    return self.board.board.microbit_get_brightness()

  def get_compass(self):
    return self.board.board.microbit_get_compass()
  
  def cal_compass(self):
    self.board.board.microbit_cal_compass()
  
  def get_temp(self):
    return self.board.board.microbit_get_temp()
  
  def get_accelerometer_X(self):
    return self.board.board.microbit_get_accelerometer_X()
  
  def get_accelerometer_Y(self):
    return self.board.board.microbit_get_accelerometer_Y()
  
  def get_accelerometer_Z(self):
    return self.board.board.microbit_get_accelerometer_Z()
  
  def get_accelerometer_strength(self):
    return self.board.board.microbit_get_accelerometer_strength()
  
class Wireless:
  def __init__(self, board=None):
    if board == None:
      board = gboard
    self.board = board
  
  def set_wireless_channel(self, channel):
    self.board.board.microbit_set_wireless_channel(channel)
  
  def open_wireless(self):
    self.board.board.microbit_open_wireless(1)
  
  def close_wireless(self):
    self.board.board.microbit_open_wireless(0)
  
  def send_wireless(self, data):
    data = str(data)
    val = []
    for i in data:
      val.append(ord(i))
    self.board.board.microbit_send_wireless(val)
  
  def recv_data(self, callback = None):
    self.board.board.microbbit_recv_data(callback)

class Board:
  def __init__(self, boardname="", port=None):
    global gboard
    self.boardname = boardname.upper()
    self.port = port
    self._i2c_init = [False,False,False,False,False]
    self.i2c = [None, None, None, None, None]
    self._spi_init = [False,False,False,False,False]
    self.spi = [None, None, None, None, None]

    if gboard is None:
      gboard = self

    name = platform.platform()
    self.connected = False
    if self.boardname == "RPI":#本地资源
      GPIO.setmode(GPIO.BCM)
      GPIO.setwarnings(False)
    elif self.boardname == "XUGU":
      self.boardname = "UNO"
      self.port = "/dev/ttyS1"
    #  self.begin()
    #else:#外部资源
    #  self.begin()
  
  def begin(self):
    if self.connected:
      return
    printlogo()
    version = sys.version.split(' ')[0]
    plat = platform.platform()
    print("[01] Python"+version+" "+plat+" Board: "+ self.boardname)
    if self.boardname == "RPI":
      self.connected = True
      return self
    major,minor = self.detect_firmata()
    print("[32] Firmata ID: %d.%d"%(major,minor))
    if major != FIRMATA_MAJOR or minor != FIRMATA_MINOR:
      print("[35] Burning firmware...")
      cwdpath,_ = os.path.split(os.path.realpath(__file__))
      pgm = Burner(self.boardname,self.port)
      if(self.boardname == "UNO"):
        name = platform.platform()
        if name.find("Linux_vvBoard_OS")>=0 or name.find("Linux-4.4.159-aarch64-with-Ubuntu-16.04-xenial")>=0:
          cmd = "/home/scope/software/avrdude-6.3/avrdude -C/home/scope/software/avrdude-6.3/avrdude.conf -v -patmega328p -carduino -P"+self.port+" -b115200 -D -Uflash:w:"+cwdpath + "/base/FirmataExpress.UNO."+str(FIRMATA_MAJOR)+"."+str(FIRMATA_MINOR)+".hex"+":i"
          os.system(cmd)
        else:
          pgm.burn(cwdpath + "/base/FirmataExpress.UNO."+str(FIRMATA_MAJOR)+"."+str(FIRMATA_MINOR)+".hex")
      elif(self.boardname == "LEONARDO"):
        port_list_0 = list(serial.tools.list_ports.comports())
        port_list_0 = [list(x) for x in port_list_0]
        port_list_0 = [x[0:2] for x in port_list_0]
        ser = serial.Serial(self.port,1200,timeout=1) #复位
        ser.close()
        time.sleep(0.2)
        retry = 5
        port = None
        while retry:
          retry = retry - 1
          port_list_2 = list(serial.tools.list_ports.comports())
          port_list_2 = [list(x) for x in port_list_2]
          port_list_2 = [x[0:2] for x in port_list_2]
          for p in port_list_2:
            if p not in port_list_0:
              port = p
              break
          if port == None:
            time.sleep(0.5)
          if port: #找到了BootLoader串口
            break
        if port == None:
          print("[99] can NOT find ",self.boardname)
          sys.exit(0)
        pgm = Burner(self.boardname, port[0])
        pgm.burn(cwdpath + "/base/FirmataExpress.LEONARDO."+str(FIRMATA_MAJOR)+"."+str(FIRMATA_MINOR)+".hex")
      elif(self.boardname == 'MEGA2560'):
        pgm.burn(cwdpath + "/base/FirmataExpress.MEGA2560."+str(FIRMATA_MAJOR)+"."+str(FIRMATA_MINOR)+".hex")
      elif(self.boardname == 'HANDPY'):
        pgm.burn(cwdpath + "/base/FirmataExpress.HANDPY."+str(FIRMATA_MAJOR)+"."+str(FIRMATA_MINOR)+".bin")
        time.sleep(1)
        ser=serial.Serial(self.port, 115200, timeout=3)
        ser.read(ser.in_waiting)
        ser.close()
      elif(self.boardname == 'MICROBIT'):
        pgm.burn(cwdpath + "/base/FirmataExpress.MICROBIT."+str(FIRMATA_MAJOR)+"."+str(FIRMATA_MINOR)+".hex")
      print("[37] Burn done")
    time.sleep(2)
    self.board = pymata4.Pymata4(com_port=self.port, baud_rate=115200)
    
    self.connected = True
    return self
  '''
  Uno:
  ['COM99', 'Arduino Uno (COM99)', 'USB VID:PID=2341:0043 SER=5573932393735151F0C1 LOCATION=1-10']
  ['/dev/ttyACM0', 'ttyACM0', 'USB VID:PID=2341:0043 SER=5573932393735151F0C1 LOCATION=1-2:1.0']
  Leonardo:
  ['COM18', 'Arduino Leonardo (COM18)', 'USB VID:PID=2341:8036 SER=6 LOCATION=1-10.10:x.0']
  ['/dev/ttyACM1', 'Arduino Leonardo', 'USB VID:PID=2341:8036 LOCATION=1-10:1.0']
  MEGA2560:
  ['COM7', 'Arduino Mega 2560 (COM7)', 'USB VID:PID=2341:0042 SER=556393132333512141A2 LOCATION=1-10']
  ['/dev/ttyACM0', 'ttyACM0', 'USB VID:PID=2341:0042 SER=556393132333512141A2 LOCATION=1-2:1.0']
  Microbit:
  ['COM12', 'mbed Serial Port (COM12)', 'USB VID:PID=0D28:0204 SER=6 LOCATION=1-1:x.1']
  Handpy:
  ['COM29', 'Silicon Labs CP210x USB to UART Bridge (COM29)', 'USB VID:PID=10C4:EA60 SER=01CEDB2F LOCATION=1-9']
  '''
  def detect_firmata(self):
    vidpid={
    "UNO":"2341:0043",
    "LEONARDO":"2341:8036",
    "MEGA2560":"2341:0042",
    "MICROBIT":"0D28:0204",
    "HANDPY":"10C4:EA60"
    }
    portlist=[]
    localportlist=[]
    if self.boardname == "RPI":
      print("Using local resources")
      return (-1,-1)
    elif self.port == None:
      plist = list(serial.tools.list_ports.comports())
      for port in plist:
        msg = list(port)
        if msg[2].find(vidpid[self.boardname]) >= 0:
          portlist.insert(0,msg)
          break
        elif msg[2].find("USB") >= 0:
          portlist.insert(0,msg)
        else:
          localportlist.append(msg)
        portlist += localportlist
      if len(portlist) > 0:
        self.port = portlist[0][0]
        print("Automatically selected -> ",self.port)
    print("[10] Opening "+self.port)
    name = platform.platform()
    if name.find("Linux_vvBoard_OS")>=0 or name.find("Linux-4.4.159-aarch64-with-Ubuntu-16.04-xenial") >= 0:
      os.system("echo scope | sudo -S /home/scope/software/scripts/arduino_burn_setup.sh Arduino_Reset")
    ser=serial.Serial(self.port, 115200, timeout=3)
    if self.boardname == "HANDPY" or self.boardname == "MICROBIT":
      time.sleep(1)
    if(self.boardname == "UNO" or self.boardname == "MEGA2560"):
      time.sleep(3)
    ser.read(ser.in_waiting)
    buf=bytearray(b"\xf0\x79\xf7")
    ser.write(buf)
    res = ser.read(10)
    if len(res) < 3:
      major=0
      minor=0
    elif res[0] == 0xF9:
      major = res[1]
      minor = res[2]
    elif res[0] == 0xF0 and res[1] == 0x79:
      major = res[2]
      minor = res[3]
    else:
      major=0
      minor=0
    if major == 2 and minor == 6:
      if self.boardname == "HANDPY" or self.boardname == "MICROBIT":
        ser.read(ser.in_waiting)
        reset_buf=bytearray(b"\xf0\x0d\x55\xf7")
        ser.write(reset_buf)
        reset = ser.read(10)
    ser.close()
    print("[15] Close "+self.port)
    return major,minor

  def get_i2c_master(self, bus_num=0):
    if bus_num == -1:#如果用户填写-1，自动分配device_num
      for i in range(len(self.i2c)):
        if self.i2c[i] is None:
          bus_num = i
          break

    if bus_num == -1: #分配满了，不再分配
      return None

    if self.i2c[bus_num] is None:
      self._i2c_init[bus_num] = True
      self.i2c[bus_num] = IIC(self,bus_num)
    return self.i2c[bus_num]

  def get_spi_master(self, device_num=0, sck=None, mosi=None, miso=None, cs=None, baudrate=100000, polarity=0, phase=0, bits=8):
    if device_num == -1:#如果用户填写-1，自动分配device_num
      for i in range(len(self.spi)):
        if self.spi[i] is None:
          device_num = i
          break

    if device_num == -1: #分配满了，不再分配
      return None

    if self.spi[device_num] is None:
      self._spi_init[device_num] = True
      self.spi[device_num] = SPI(self, device_num, sck, mosi, miso, cs, baudrate, polarity, phase, bits)
    return self.spi[device_num]
  
  @staticmethod
  def set_default_board(board):
    global gboard
    gboard = board

'''
if platform.system() == "Linux":
  name = platform.platform()
  if name.find("Linux_vvBoard_OS")>=0 or name.find("Linux-4.4.159-aarch64-with-Ubuntu-16.04-xenial") >= 0:
    #虚谷号内部资源没有引出，不需要创建本地主板，创建uno主板
    gboard = Board("uno","/dev/ttyS1")
  else: #RPi
    output = subprocess.Popen(['lsb_release','-a'], shell=False, stdout=subprocess.PIPE, stderr=subprocess.STDOUT).stdout.read()
    print(output)
    print(type(output))
    if str(output).find("Raspbian") >= 0:
      print("RPi")
      #Linux平台自动创建内置的本地主板,用户层可以不再创建gboard
      gboard = Board()
'''
class tcp_begin:
  def __init__(self, ip, port):
    self._i2c_init = [False,False,False,False,False]
    self.i2c = [None, None, None, None, None]
    self._spi_init = [False,False,False,False,False]
    self.spi = [None, None, None, None, None]
    printlogo()
    global gboard
    self.ip = ip
    self.port = port
    if gboard == None:
      gboard = self
    self.boardname = "UNO"
    self.board = pymata4.Pymata4(ip_address=self.ip, ip_port=self.port)
