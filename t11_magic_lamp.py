from machine import Pin #to access the hardware on the pico
import utime
sensor=Pin(9,Pin.IN) #initialize digital pin 1 as an INPUT for Sensor
led=Pin(7,Pin.OUT)#initialize digital pin 7 as an OUTPUT for LED
print('magic lamp 0')
while True:
    # print('magic lamp 1')
    #When sensor value is '0', the relay will be '1'
    # utime.sleep(0.05)
    # print('magic lamp 2, sensor value = ', sensor.value())
    if sensor.value() == 1:
        led.value(1)  
    else:
        led.value(0)