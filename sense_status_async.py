#!/usr/local/bin/python3.8
from sense_hat import SenseHat
import netifaces
import time
import asyncio

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


def show_time(column):
    #Show address address
    color=red
    for y in range(0,8):
       # if( time == y+1):
       sense.set_pixel(column, y, color)

def show_address(address, column):
    auto_rotate_display()
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
async def get_address(name, x_addr):
    while(True):
        try:
            addr=netifaces.ifaddresses(name)[netifaces.AF_INET][0]['addr']
            show_address(addr, x_addr) 
            erroreth=False
        except:
            show_time(x_addr) 
        asyncio.sleep(5)

# Initialize Sensehat with the current orientation
#
sense = SenseHat()
auto_rotate_display()
sense.clear()
asyncio.create_task(get_address('eth0', x_eth),name='ETH0')
asyncio.create_task(get_address('wlan0', x_wlan), name='WLAN')
