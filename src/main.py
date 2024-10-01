from machine import Pin, UART, I2C
import utime
import math
from machine import I2C, Pin
from lcd_api import LcdApi         #https://github.com/oguzhanbaser/picoWorkspace/blob/master/pico-w-telegram/lcd_api.py
from i2c_lcd import I2cLcd         #https://github.com/oguzhanbaser/picoWorkspace/blob/master/pico-w-telegram/i2c_lcd.py
from micropyGPS import MicropyGPS  #https://github.com/inmcm/micropyGPS/blob/master/micropyGPS.py
from picozero import Button

#####################################################
#### Comment out all gc.collect() from i2c_lcd.py ###
#####################################################

#Led init
led = Pin(25, Pin.OUT)
led.toggle()

#Buttons init
red_button = Button(18)
blue_button = Button(22)

#GPS init
gps_module = UART(1, baudrate=9600, tx=Pin(4), rx=Pin(5))
time_zone = +2
gps = MicropyGPS(time_zone)

#LCD init
I2C_ADDR     = 39
I2C_NUM_ROWS = 2
I2C_NUM_COLS = 16
i2c = I2C(0, sda=machine.Pin(0), scl=machine.Pin(1), freq=400000)
lcd = I2cLcd(i2c, I2C_ADDR, I2C_NUM_ROWS, I2C_NUM_COLS)

#Init message
lcd.move_to(0,0)
lcd.putstr(">>> Willkomen   >>> Arrancanding")
utime.sleep_ms(3000)
lcd.move_to(0,0)
lcd.putstr("                                ")


def read_temp():
    temp_sensor = machine.ADC(4)
    conversion_factor = 3.3 / (65535)
    reading = temp_sensor.read_u16() * conversion_factor 
    temperature = 27 - (reading - 0.706)/0.001721
    formatted_temperature = "{:.0f}".format(temperature)
    string_temperature = str(formatted_temperature+"o")
    return string_temperature

def convert_signal(sections):
    # sections[0] contains the degrees
    # sections[1] contains the minutes    
    if (len(sections) != 3 or (sections[0] == 0 and sections[1] == 0.0)):
        return None
    data = sections[0]+(sections[1]/60.0)

    # sections[2] contains 'E', 'W', 'N', 'S'
    if (sections[2] == 'S'):
        data = -data
    if (sections[2] == 'W'):
        data = -data

    return data

def distance(origin, destination):
    """
    Calculate the Haversine distance.

    Parameters
    ----------
    origin : tuple of float
        (lat, long)
    destination : tuple of float
        (lat, long)

    Returns
    -------
    distance_in_km : float

    Examples
    --------
    >>> origin = (48.1372, 11.5756)  # Munich
    >>> destination = (52.5186, 13.4083)  # Berlin
    >>> round(distance(origin, destination), 1)
    504.2
    """
    lat1, lon1 = origin
    lat2, lon2 = destination
    radius = 6371  # km

    dlat = math.radians(lat2 - lat1)
    dlon = math.radians(lon2 - lon1)
    a = (math.sin(dlat / 2) * math.sin(dlat / 2) +
         math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) *
         math.sin(dlon / 2) * math.sin(dlon / 2))
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    d = radius * c

    return d

#Init all vars
last_lat = 0.0
last_long = 0.0
total_distance = 0.0
load_index = 0
red_button_inc = 0
blue_button_inc = 0
both_button_inc = 0

def increase_distance():
    global total_distance
    total_distance += 0.01

def decrease_distance():
    global total_distance
    if total_distance > 0.0:
        total_distance -= 0.01

while True:
    gps_data = gps_module.any()
    if gps_data > 0:
        b = gps_module.read(gps_data)
        print(b)
        for x in b:
            msg = gps.update(chr(x))
    
    gps_lat = convert_signal(gps.latitude)
    gps_lon = convert_signal(gps.longitude)

    if (gps.valid):
        #Line 1
        t = gps.timestamp
        time_formated = '{:02d}:{:02d}:{:02}'.format(t[0], t[1], t[2])

        temperature = read_temp()

        sat_in_use = 'Y'+"{:2.0f}".format(gps.satellites_in_use)

        #Line 2
        formatted_course = "{:3.0f}".format(gps.course)

        if (last_lat == 0.0):
            last_lat = gps_lat;
        if (last_long == 0.0):
            last_long = gps_lon;
        origin = (last_lat, last_long)  
        destination = (gps_lat, gps_lon)  
        partial_distance = round(distance(origin, destination), 3)
        
        if (partial_distance >= 0.01):
            total_distance += partial_distance
            last_lat = gps_lat;
            last_long = gps_lon;
            
        formatted_speed = "{:3.0f}".format(gps.speed[2])

        formated_distance = "{:6.2f}".format(total_distance)
            
        line1 = time_formated + ' ' + temperature + ' ' + sat_in_use
        line2 = formatted_course + 'N ' + formated_distance + ' S' + formatted_speed

    else:
        line1 = 'Buscan satelich '
        #When some signal is received, but not enough to get a position, we use a T in front
        line2 = 'T'+"{:2.0f}".format(gps.satellites_in_use) + '.............'[:load_index] + '             '[load_index:]
        
        #When we do not receive any signal from satellites, we use a Y in front
        if(gps.timestamp[0] == 0):
            line2 = 'Y'+"{:2.0f}".format(gps.satellites_in_use) + '.............'[:load_index] + '             '[load_index:]
        
        load_index += 1
        if (load_index == 14):
            load_index = 0


    #Manage distance with buttons
    if (red_button.is_active and blue_button.is_active):
        if (both_button_inc >= 91):
            total_distance = 0.00
            line1 = "****************"
            line2 = "****************"
        else:
            both_button_inc += 1
            line1 = "RRReset........" + "{:1.0f}".format(100 - both_button_inc)
            line2 = line1
    else:
        both_button_inc = 0
        if (red_button.is_active):
            red_button_inc += 1
            total_distance += 0.01
            if (red_button_inc > 20):
                total_distance += 0.10
            if (red_button_inc > 50):
                total_distance += 0.50
        else:
            red_button_inc = 0
            
        if (blue_button.is_active):
            blue_button_inc += 1
            total_distance -= 0.01
            if (blue_button_inc > 20):
                total_distance -= 0.10
            if (blue_button_inc > 50):
                total_distance -= 0.50
            if (total_distance <= 0):
                total_distance = 0.00
        else:
            blue_button_inc = 0

    #Put in LCD whatever string
    lcd.move_to(0,0)
    lcd.putstr(line1)
    lcd.move_to(0,1)
    lcd.putstr(line2)



