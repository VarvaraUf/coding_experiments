from machine import Pin
import utime

led = Pin(15,Pin.OUT)

while True:
    utime.sleep(0.5)
    led.toggle()