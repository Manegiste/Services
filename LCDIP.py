#!/usr/bin/python
# -*- coding: utf-8 -*-

import RPi.GPIO as GPIO
import netifaces
from time import sleep
from datetime import datetime
import psutil
import os


class HD44780:

    def __init__(self, pin_rs=7, pin_e=11, pins_db=[12, 13, 15, 16]):
        self.pin_rs = pin_rs
        self.pin_e = pin_e
        self.pins_db = pins_db

        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(self.pin_e, GPIO.OUT)
        GPIO.setup(self.pin_rs, GPIO.OUT)
        for pin in self.pins_db:
            GPIO.setup(pin, GPIO.OUT)

        self.clear()

    def clear(self):
        self.cmd(0x33) # init 8 bits
	self.cmd(0x32) # init 8 bits confirmation
	self.cmd(0x28) # 4 bits - 2 lignes
	self.cmd(0x0C) # Pas de curseur
	self.cmd(0x06) # Incrémentation curseur
	self.cmd(0x01) # Efface écran

    def home(self):
	self.cmd(0x0C) # Pas de curseur
	self.cmd(0x06) # Incrémentation curseur
	self.cmd(0x02) # "Home" : curseur en haut à gauche
	
    def cmd(self, bits, char_mode=False):
        sleep(0.005)
        bits=bin(bits)[2:].zfill(8)

        GPIO.output(self.pin_rs, char_mode)

        for pin in self.pins_db:
            GPIO.output(pin, False)

        for i in range(4):
            if bits[i] == "1":
                GPIO.output(self.pins_db[::-1][i], True)

        GPIO.output(self.pin_e, True)
        GPIO.output(self.pin_e, False)

        for pin in self.pins_db:
            GPIO.output(pin, False)

        for i in range(4,8):
            if bits[i] == "1":
                GPIO.output(self.pins_db[::-1][i-4], True)

        GPIO.output(self.pin_e, True)
        GPIO.output(self.pin_e, False)

    def message(self, text):
        for char in text:
            if char == '\n':
                self.cmd(0xC0) # 0x80 + 0x40 adresse 2eme ligne
            else:
                self.cmd(ord(char),True)

    def __del__(self):
        GPIO.cleanup()
#end class

mode=0


if __name__ == '__main__':
    lcd = HD44780()
    lcd.clear()

#sleep (20)

def funcMode(channel):
    global mode
    mode=mode+1 
    if mode >= 3:
        mode=0

GPIO_mode=33 #Button to switch mode
GPIO.setup(GPIO_mode, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.add_event_detect(GPIO_mode, GPIO.FALLING, callback=funcMode, bouncetime=300)


while 1 :
    timestamp=str(datetime.now().time())[:8]
    cpu= psutil.cpu_percent()
    temp= os.popen('vcgencmd measure_temp').readline()[5:11]
    mem=float(psutil.virtual_memory().used) * 100 / float(psutil.virtual_memory().total)
    lcd.home()
    if mode == 0:
       try:
          EthAd =  "E:" + netifaces.ifaddresses('eth1')[netifaces.AF_INET][0]['addr']
       except:
          EthAd = "No LAN"

       try:
          WifAd =  "W:" + netifaces.ifaddresses('wlan0')[netifaces.AF_INET][0]['addr']
       except:
          WifAd = "No wifi"
       lcd.message("%s\n%s" % ( WifAd.ljust(16) , EthAd.ljust(16)))
    elif mode == 1:
        lcd.message ( "{}\nCPU% {:3.0f} MEM {:3.0f} ".format(timestamp, cpu,mem))
    elif mode == 2:
        lcd.message ("Temp: {} \nCPU% {:11.0f}".format(temp,cpu))
    sleep(1)
