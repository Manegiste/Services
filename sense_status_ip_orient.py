#!/usr/bin/python3
from sense_hat import SenseHat
import netifaces
import time

# define a column for ethO and one for wlan
x_eth=2
x_wlan=0

color_192=(100,255,100)
color_10=(255,0,128)
red=(128,0,0)
green=(0,128,0)
blue=(0,0,128)

def show_error(column):
    for y in range(0,4):
        sense.set_pixel(column,y*2,red)
        sense.set_pixel(column+1,y*2+1,red)


def show_time(time, column):
    #Show address address
    color=red
    for y in range(0,8):
        if( time == y-1):
            sense.set_pixel(column, y, color)

def show_address(address, column, error=False):
    #Show address address
    if address.split(".")[0]=='192':
        color=color_192
        show=True
    elif address.split(".")[0]=='10':
        color=color_10
        show=True
    else:
        color=red
        show=False

    if error:
        color=red
   
    addr=int(address.split(".")[3])
    for y in range(0,8):
        if(show):		
            if( addr & (1<<y)):
                sense.set_pixel(column, y, color)
        else:
                sense.set_pixel(column, y, color)

    addr=int(address.split(".")[2])
    for y in range(0,8):
        if(show):		
            if( addr & (1<<y)):
                sense.set_pixel(column+1, y, color)
        else:
                sense.set_pixel(column+1, y, color)
   
def auto_rotate_display():
    # read sensor
    x = round(sense.get_accelerometer_raw()['x'],0)
    y = round(sense.get_accelerometer_raw()['y'],0)
    z = round(sense.get_accelerometer_raw()['z'],0)

    if ( z == 0):
        sense.set_rotation(0)
        rot = 180
        if x == -1.0:
            rot=270
        elif y == -1.0:
            rot=0
        elif x == 1.0:
            rot=90
    elif z == 1:
        rot=0

    sense.set_rotation(rot)

#
# Initialize Sensehat with the current orientation
#
sense = SenseHat()
auto_rotate_display()
sense.clear()

erroreth=False
errorwlan=False
tried=0


eth0=""
wlan=""

while "Not found all addresses yet":
    auto_rotate_display()
    try:
        oldeth0=eth0
        eth0=netifaces.ifaddresses('eth0')[netifaces.AF_INET][0]['addr']
        show_address(eth0,x_eth) 
    except:
        show_address(oldeth0,x_eth, True) 

    try:
        oldwlan=wlan
        wlan=netifaces.ifaddresses('wlan0')[netifaces.AF_INET][0]['addr']
        show_address(wlan,x_wlan)
    except:
        show_address(oldwlan,x_wlan, True)

    time.sleep(2)
