from machine import Pin, I2C, ADC, Timer
from picobricks import SSD1306_I2C, WS2812
import utime

WIDTH = 128                                            
HEIGHT = 64

sda=Pin(4)
scl=Pin(5)
i2c=I2C(0, sda=sda, scl=scl)

oled = SSD1306_I2C(128, 64, i2c)
potentiometer = ADC(Pin(26))
button = Pin(10, Pin.IN, Pin.PULL_DOWN)
ws = WS2812(brightness=0.1)

def map_range_value(value, min, max, min_new, max_new):
    size = max - min
    #print("size",size)
    #print("value",value)
    position = (value - min) / size
    #print(utime.ticks_ms(),"position",position)
    size_new = max_new - min_new
    #print(utime.ticks_ms(),"size_new",size_new)
    v_new = (size_new * position) + min_new
    #print(utime.ticks_ms(),"v_new",v_new)
    return v_new

def map_u16_value(v, min, max):
    return map_range_value(v, 0, 65535, min, max)


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
    
    while button.value()==0:
        oled.fill(0)
        minutes=int((potentiometer.read_u16()*60)/65536)+1
        
        oled.text("Set timer:" + str(minutes) + " min", 0, 12)
        oled.show()
        
        
    update_minute(None)

    time=Timer(mode=Timer.PERIODIC, period=60000, callback=update_minute)
    time2=Timer(mode=Timer.PERIODIC, period=1000, callback=update_second)
    time3=Timer(mode=Timer.PERIODIC, period=10, callback=update_millisecond)

    utime.sleep(0.3)

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

def my_timer_set(number,secound,color):
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
        # oled.text(str(number ) + "%: " + str(secound) + "%: " + str(color) +":",0,32)
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
    

def get_remander(a,b):
    c = a//b
    e = c*b
    return a - e

def secounds_to_time(seconds):
    minutes = seconds//60
    e = minutes*60
    ramainder_seconds = seconds - e
    return str(minutes) + "m" + str(ramainder_seconds) + "s"#"1m1s"
    
def seconds_to_hms(seconds):
    minutes = seconds//60
    e = minutes*60
    ramainder_seconds = seconds - e
    hours = minutes//60
    e = hours*60
    ramainder_minutes = minutes - e

    return str(hours) + "h" + str(ramainder_minutes) + "m" + str(ramainder_seconds) + "s"#"1m1s"

def millisecounds_to_hmsms(millisecounds):
    secounds = millisecounds//1000
    e = secounds*1000
    ramainder_millisecounds = millisecounds - e

    minutes = secounds//60
    e = minutes*60
    ramainder_seconds = secounds - e

    hours = minutes//60
    e = hours*60
    ramainder_minutes = minutes - e
    return str(hours) + "h " + str(ramainder_minutes) + "m " + str(ramainder_seconds) + "s " + str(ramainder_millisecounds) + "ms"#"1m1s"
def pad_2(n):
    if n < 10:
        return "0" + str(n)
    
    return str(n)
    
def pad_3(w):
    if w > 0:
        if w < 10:
            return "00" + str(w)
        if w < 100:
            return "0" + str(w)
    return str(w)

def pad_zeroes(n,l):
    times = l - len(str(n))
    zeroes = ""
    for index in range(0,times):
        zeroes += "0"
        
    return zeroes + str(n)

def millisecounds_to_clock(millisecounds):
    secounds = millisecounds//1000
    e = secounds*1000
    milliseconds_ramainder = millisecounds - e

    minutes = secounds//60
    e = minutes*60
    seconds_ramainder = secounds - e    

    return pad_zeroes(minutes,2) + ":" + pad_zeroes(seconds_ramainder,2) + "." + pad_zeroes(milliseconds_ramainder,3) + "ms"#"1m1s"


milliseconds=0
def my_timer_count_milliseconds():
    global milliseconds
            
    def update_millisecond(timer):
        global milliseconds
        milliseconds -= 9
       
    while button.value()==0:
        oled.fill(0)
        milliseconds=int(map_u16_value(potentiometer.read_u16(),0,3_600_000))
        
        oled.text("Set timer: ", 10, 12)
        oled.text(millisecounds_to_clock(milliseconds) + " min",10,24)
        oled.show()
        
    time3=Timer(mode=Timer.PERIODIC, period=9, callback=update_millisecond)

    utime.sleep(0.3)

    while button.value()==0:
        oled.fill(0)
        
        oled.text(millisecounds_to_clock(milliseconds),10,20)
                
        oled.show()
        utime.sleep(0.01)
        if(milliseconds < 0):
            milliseconds=0
            break

    time3.deinit()
    oled.fill(0)
    oled.text(millisecounds_to_clock(milliseconds),10,30)
    oled.text("Time is Over!",10,48)
    oled.show()
    
# my_timer_set(100,100,8)
# my_timer_count_milliseconds()
# my_timer()
# print(millisecounds_to_clock(3600000))
my_timer_count_milliseconds()