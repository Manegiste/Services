#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-
import RPi.GPIO as GPIO
import time as time
from time import sleep
import os
import signal

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

# Define mode to access GPIO pins
GPIO.setmode(GPIO.BOARD)

# pin id for the shutdown button
GPIO_shutdown=32
# pin id for the LED status
GPIO_led=36

# GPIO_shutdown will be an input pin
GPIO.setup(GPIO_shutdown, GPIO.IN, pull_up_down=GPIO.PUD_UP)
# GPIO_led will be an output pin
GPIO.setup(GPIO_led, GPIO.OUT)

# Handler to stop the process
def signal_handler(signal, frame):
    # Turn off the status LED
    GPIO.output(GPIO_led, False)
    lcd = HD44780()
    lcd.clear()
    lcd.message("Shutting down...\nBye!")
    GPIO.cleanup()
    exit(0)

# Define what to do when the shutdown button is pressed
def funcShutdown(channel):
    start_time = time.time()
    intSeconds = 0
    # How long to wait for the button
    maxWaitPushButton = 2
    while intSeconds < maxWaitPushButton and GPIO.input(channel) == GPIO.LOW :
         intSeconds = time.time() - start_time
         time.sleep(0.1)
    if intSeconds >= maxWaitPushButton:
        os.system('sudo service lcdip stop')
        lcd = HD44780()
        lcd.clear()
        lcd.message("Shutting down...\nBye!")
        # Turn off the status LED
        GPIO.output(GPIO_led, False)
        GPIO.cleanup()
        os.system('sudo halt')
        #exit()  

# Add a signal handler for the SIGTERM signal
signal.signal(signal.SIGTERM, signal_handler)
# Wait for the shutdown button to be pressed
GPIO.add_event_detect(GPIO_shutdown, GPIO.FALLING, callback=funcShutdown, bouncetime=300) 
# Light up the status LED
GPIO.output(GPIO_led, True)
# Loop
while 1:
    time.sleep(0.2)
