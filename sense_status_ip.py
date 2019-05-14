#!/usr/bin/python3
from sense_hat import SenseHat
import netifaces

# define a colum for ethO and one for wlan
x_eth=2
x_wlan=0

color_192=(100,255,100)
color_10=(255,0,128)
red=(128,0,0)
green=(0,128,0)
blue=(0,0,128)

def show_error(column):
    for y in range(0,8):
        sense.set_pixel(column,y,red)
        sense.set_pixel(column+1,y,red)


def show_address(address, column):
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

sense = SenseHat()
sense.set_rotation(270)
sense.clear()

try:
    eth0=netifaces.ifaddresses('eth0')[netifaces.AF_INET][0]['addr']
    show_address(eth0,x_eth) 
except:
    show_error(x_eth)

try:
    wlan=netifaces.ifaddresses('wlan0')[netifaces.AF_INET][0]['addr']
    show_address(wlan,x_wlan)
except:
    show_error(x_wlan)

