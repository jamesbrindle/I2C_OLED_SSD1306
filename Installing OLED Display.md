## Installing I2C OLED Display

https://www.instructables.com/Raspberry-Pi-Monitoring-System-Via-OLED-Display-Mo/

** Refer to image for wire pin layout**

```
sudo raspi-config
```

1. A blue screen may appear on the display. Now select Interfacing option.
2. After this, we need to select I2C option.
3. After this, we need to select Yes and press enter and then ok.
4. After this, we need to reboot Raspberry Pi by typing below command:

*reboot*

```
sudo apt-get update
sudo apt-get install build-essential python-dev python-pip
sudo apt-get install i2c-tools
sudo apt-get install python-smbus

sudo apt install -y python3-dev
sudo apt install -y python-smbus i2c-tools
sudo apt install -y python3-pil
sudo apt install -y python3-pip
sudo apt install -y python-setuptools
sudo apt install -y python3-setuptools
sudo apt install -y python3-rpi.gpio
sudo apt install -y python-dev
sudo apt install -y python-smbus i2c-tools
sudo apt install -y python-pil
sudo apt install -y python-pip
sudo apt install -y python-setuptools 
sudo pip install setuptools
sudo pip install RPi.GPIO
sudo pip3 install RPi.GPIO
sudo pip install Adafruit_BBIO
sudo pip3 install Adafruit_BBIO
sudo pip install Pillow
sudo pip3 install Pillow
sudo pip install Image
sudo pip3 install Image

```

sudo i2cdetect -y 1

OUTPUT

```
0 1 2 3 4 5 6 7 8 9 a b c d e f

00: -- -- -- -- -- -- -- -- -- -- -- -- --

10: -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --

20: -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --

30: -- -- -- -- -- -- -- -- -- -- -- -- 3c -- -- --

40: -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --

50: -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --

60: -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --

70: -- -- -- -- -- -- -- --
```

If have a value somewhere, we're good

## Install Adafruit Python Library

```
git clone https://github.com/adafruit/Adafruit_Python_SSD1306.git
cd Adafruit_Python_SSD1306
sudo python setup.py install
sudo python3 setup.py install
cd ..
git clone https://github.com/adafruit/Adafruit_Python_GPIO.git
cd Adafruit_Python_GPIO
sudo python setup.py install
sudo python3 setup.py install
cd ..
git clone https://github.com/adafruit/Adafruit_Python_PureIO.git
cd Adafruit_Python_PureIO
sudo python setup.py install
sudo python3 setup.py install
```

## Using Provided 'Stats' Python Script

1. Create a folder in the home directory called 'Repositories'
2. Copy folder RPI_SSD1306 to Repositories folder
3. You can run the script via:

```
cd python /home/pi/Repositories/RPI_SSD1306
python SSD1306-Stats.py
```

### Stating Script On Boot

Terminal:

```
sudo nano /etc/rc.local
```

Add lines **before** the 'exit 0' command:

```
cd /home/pi/Repositories/RPI_SSD1306
sudo python SSD1306-Stats.py &
```







