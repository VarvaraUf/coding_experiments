from machine import Pin, I2C, ADC, Timer
from picobricks import SSD1306_I2C
import utime

WIDTH = 128                                            
HEIGHT = 64

sda=Pin(4)
scl=Pin(5)
i2c=I2C(0, sda=sda, scl=scl)

oled = SSD1306_I2C(128, 64, i2c)
potentiometer = ADC(Pin(26))
button = Pin(10, Pin.IN, Pin.PULL_DOWN)


seconds=59
milliseconds=999
minutes = 0
def my_timer():
    global seconds
    global milliseconds
    global minutes

    def update_minute(timer):
        global minutes
        minutes -= 1
        
    def update_second(timer):
        global seconds
        seconds -= 1
        if seconds < 0:
            seconds = 59
            
    def update_millisecond(timer):
        global milliseconds
        milliseconds -= 10
        if milliseconds < 0:
            milliseconds = 999

    #We determine the increments of the minute-second and millisecond values.
    seconds=59
    milliseconds=999
    minutes = 0

    while button.value()==0:
        oled.fill(0)
        minutes=int((potentiometer.read_u16()*60)/65536)+1
        oled.text("Set timer:" + str(minutes) + " min", 0, 12)
        oled.show()
        utime.sleep(0.1)
        
    update_minute(None)

    time=Timer(mode=Timer.PERIODIC, period=60000, callback=update_minute)
    time2=Timer(mode=Timer.PERIODIC, period=1000, callback=update_second)
    time3=Timer(mode=Timer.PERIODIC, period=10, callback=update_millisecond)

    utime.sleep(0.1)

    while button.value()==0:
        oled.fill(0)
        oled.text("min:" + str(minutes),50,10)
        oled.text("sec:" + str(seconds),50,20)
        oled.text("ms:" + str(milliseconds),50,30)
        oled.show()
        utime.sleep(0.01)
        if(minutes < 0):
            utime.sleep(0.1)
            milliseconds=0
            break

    time.deinit()
    time2.deinit()
    time3.deinit()

    oled.fill(0)
    oled.text(str(minutes),60,10)
    oled.text(str(seconds),60,20)
    oled.text(str(milliseconds),60,30)
    oled.text("Time is Over!",10,48)
    oled.show()

my_timer()
