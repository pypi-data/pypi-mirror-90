# -*- coding: utf-8 -*-

import time
from pinpong.board import Board,HScreen

Board("handpy").begin()#初始化，选择板型和端口号，不输入端口号则进行自动识别
#Board("handpy","COM36").begin()   #windows下指定端口初始化
#Board("handpy","/dev/ttyACM0").begin()   #linux下指定端口初始化
#Board("handpy","/dev/cu.usbmodem14101").begin()   #mac下指定端口初始化

esp32 = HScreen()

esp32.display_in_line("pinpong库",1)                    #屏幕显示"pinpong库"在第一行
#esp32.display_clear_in_line(1)                          #屏幕清除第一行的内容
#esp32.display_in_XY("pinpong", 42, 22)                  #屏幕显示"pinpong库"在x,y坐标处，x:0-127,y:0-63
#esp32.fill_screen("black")                              #屏幕显示"black"或者"white"
#esp32.screen_rotation(0)                                #屏幕反转0°或者180°
#esp32.point_drawing(0,0)                                #在坐标x,y画点
#esp32.set_line_width(1)                                 #设置线宽范围 1 - 128
#esp32.line_drawing(0,0,127,63)                          #划线，依次是起点坐标x1,y1和终点坐标x2,y2
#esp32.circle_drawing(63, 31, 20)                        #画圆，依次是坐标x, y和 半径, 不填充 
#esp32.circle_drawing_fill(63, 31, 20)                   #画圆，依次是坐标x, y和 半径, 填充
#esp32.rectangle_drawing(0,0, 63, 31)                    #画矩形，依次是起点坐标x, y, 宽，高, 不填充 
#esp32.rectangle_drawing_fill(0,0, 63, 31)               #画矩形，依次是起点坐标x, y, 宽，高, 填充 
