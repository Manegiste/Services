#!/usr/bin/python
# -*- coding: utf-8 -*-

import RPi.GPIO as GPIO
import netifaces
from time import sleep
from datetime import datetime
import psutil


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

for t in range(5):
   try:
      EthAd =  "E:" + netifaces.ifaddresses('eth1')[netifaces.AF_INET][0]['addr']
      break
   except:
      EthAd = "No LAN"
      sleep(5)

for t in range(5):
   try:
      WifAd =  "W:" + netifaces.ifaddresses('wlan0')[netifaces.AF_INET][0]['addr']
      break
   except:
      WifAd = "No wifi"
      sleep(5)

if __name__ == '__main__':
    lcd = HD44780()
    lcd.clear()
    lcd.message("%s\n%s" % ( WifAd , EthAd))

#sleep (20)

def funcMode(channel):
    global mode
    mode=mode+1 
    if mode >= 2:
        mode=0

GPIO_mode=33 #Button to switch mode
GPIO.setup(GPIO_mode, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.add_event_detect(GPIO_mode, GPIO.FALLING, callback=funcMode, bouncetime=300)


while 1 :
    timestamp=str(datetime.now().time())[:8]
    cpu= psutil.cpu_percent()
    mem=float(psutil.virtual_memory().used) * 100 / float(psutil.virtual_memory().total)
    lcd.home()
    if mode == 0:
        lcd.message("%s\n%s" % ( WifAd.ljust(16) , EthAd.ljust(16)))
    else:
        lcd.message ( "{}\nCPU% {:3.0f} MEM {:3.0f} ".format(timestamp, cpu,mem))
    sleep(1)
