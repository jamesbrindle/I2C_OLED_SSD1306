# Copyright (c) 2017 Adafruit Industries
# Author: Tony DiCola & James DeVito
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.

import Adafruit_GPIO.SPI as SPI
import Adafruit_SSD1306
import datetime
import time

from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont

import subprocess

# Raspberry Pi pin configuration:
RST = None     # on the PiOLED this pin isnt used
# Note the following are only used with SPI:
DC = 23
SPI_PORT = 0
SPI_DEVICE = 0

# Beaglebone Black pin configuration:
# RST = 'P9_12'
# Note the following are only used with SPI:
# DC = 'P9_15'
# SPI_PORT = 1
# SPI_DEVICE = 0

# 128x32 display with hardware I2C:
disp = Adafruit_SSD1306.SSD1306_128_32(rst=RST)

# 128x64 display with hardware I2C:
# disp = Adafruit_SSD1306.SSD1306_128_64(rst=RST)

# Note you can change the I2C address by passing an i2c_address parameter like:
# disp = Adafruit_SSD1306.SSD1306_128_64(rst=RST, i2c_address=0x3C)

# Alternatively you can specify an explicit I2C bus number, for example
# with the 128x32 display you would use:
# disp = Adafruit_SSD1306.SSD1306_128_32(rst=RST, i2c_bus=2)

# 128x32 display with hardware SPI:
# disp = Adafruit_SSD1306.SSD1306_128_32(rst=RST, dc=DC, spi=SPI.SpiDev(SPI_PORT, SPI_DEVICE, max_speed_hz=8000000))

# 128x64 display with hardware SPI:
# disp = Adafruit_SSD1306.SSD1306_128_64(rst=RST, dc=DC, spi=SPI.SpiDev(SPI_PORT, SPI_DEVICE, max_speed_hz=8000000))

# Alternatively you can specify a software SPI implementation by providing
# digital GPIO pin numbers for all the required display pins.  For example
# on a Raspberry Pi with the 128x32 display you might use:
# disp = Adafruit_SSD1306.SSD1306_128_32(rst=RST, dc=DC, sclk=18, din=25, cs=22)

# Initialize library.
disp.begin()

# Low contrast - Save the display
disp.set_contrast(1)

# Clear display.
disp.clear()
disp.display()

# Create blank image for drawing.
# Make sure to create image with mode '1' for 1-bit color.
width = disp.width
height = disp.height
image = Image.new('1', (width, height))

# Get drawing object to draw on image.
draw = ImageDraw.Draw(image)

# Draw a black filled box to clear the image.
draw.rectangle((0,0,width,height), outline=0, fill=0)

# Draw some shapes.
# First define some constants to allow easy resizing of shapes.
padding = -3
top = padding
bottom = height-padding
# Move left to right keeping track of the current x position for drawing shapes.
x = 0


# Load default font.
font = ImageFont.load_default()

# Alternatively load a TTF font.  Make sure the .ttf font file is in the same directory as the python script!
# Some other nice fonts to try: http://www.dafont.com/bitmap.php

fontSmall = ImageFont.truetype('Montserrat-Light.ttf', 12)
fontMedium = ImageFont.truetype('Montserrat-Medium.ttf', 14)
fontBig = ImageFont.truetype('Montserrat-Medium.ttf', 19)

fontIconSmall = ImageFont.truetype('fontawesome-webfont.ttf', 12)
fontIconMedium = ImageFont.truetype('fontawesome-webfont.ttf', 14)
fontIconBig = ImageFont.truetype('fontawesome-webfont.ttf', 18)

iteration = 0

while True:

    now = datetime.datetime.now()
    
    if (now.hour > 2 and now.hour < 8):
        disp.clear()
        disp.display()
        disp.command(0xAE) # Display off
        time.sleep(5)

    elif (iteration % 300 == 0 and iteration != 0):
        disp.clear()
        disp.display()
        disp.command(0xAE) # Display off
        time.sleep(60)
        
    else:
        # Draw a black filled box to clear the image.
        draw.rectangle((0,0,width,height), outline=0, fill=0)

        # Shell scripts for system monitoring from here : https://unix.stackexchange.com/questions/119126/command-to-display-memory-usage-disk-usage-and-cpu-load
        cmd = "hostname -I | cut -d\' \' -f1 | head --bytes -1"
        IP = subprocess.check_output(cmd, shell = True )
        cmd = "top -bn1 | grep load | awk '{printf \"%.2f, %.2f, %.2f\", $(NF-2),$(NF-1),$(NF-0)}'"
        CPU = subprocess.check_output(cmd, shell = True )
        cmd = "free -m | awk 'NR==2{printf \"%.1f%%\", $3*100/$2 }'"
        MemUsage = subprocess.check_output(cmd, shell = True )
        cmd = "df -h | awk '$NF==\"/\"{printf \"HDD: %d/%dGB %s\", $3,$2,$5}'"
        cmd = "df -h | awk '$NF==\"/\"{printf \"%s\", $5}'"
        Disk = subprocess.check_output(cmd, shell = True )
        cmd = "vcgencmd measure_temp | cut -d '=' -f 2 | head --bytes -1"
        Temperature = subprocess.check_output(cmd, shell = True )

        # Icons
        draw.text((x+3, top+3),    unichr(61820),  font=fontIconMedium, fill=255) # CPU
        draw.text((x+4, top+19),    unichr(62152),  font=fontIconMedium, fill=255) # Temperatue      
        draw.text((x+70, top+19),    unichr(62171),  font=fontIconSmall, fill=255) # Memory    

        draw.text((x+20, top+1), str(CPU), font=fontMedium, fill=255)
        draw.text((x+20, top+17), str(Temperature),  font=fontMedium, fill=255)
        draw.text((x+86, top+17), str(MemUsage), font=fontMedium, fill=255)
 
        disp.command(0xAF) # Display on
        disp.image(image.transpose(Image.FLIP_TOP_BOTTOM).transpose(Image.FLIP_LEFT_RIGHT))
        disp.display()
        time.sleep(5)

    iteration = iteration + 1

    if (iteration > 10000):
        iteration = 0
