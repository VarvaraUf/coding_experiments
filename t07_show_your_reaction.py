from machine import Pin, I2C
from picobricks import SSD1306_I2C
import utime
import urandom
#define the library
WIDTH=128
HEIGHT=64
#define the width and height values
sda=Pin(4)
scl=Pin(5)
i2c= I2C(0,sda=sda, scl=scl)
oled = SSD1306_I2C(WIDTH, HEIGHT, i2c)
button = Pin(10,Pin.IN,Pin.PULL_DOWN)
led = Pin(7,Pin.OUT)
#define our input and output pins
def show_your_reaction():
    while True:
        led.value(0)
        oled.fill(0)
        oled.text("press the button",0,10)
        oled.text("TO START!",25,25)
        oled.show()
        
        while button.value()==0:
            pass
        oled.fill(0)
        oled.text("Wait For LED",15,30)
        oled.show()
        
        utime.sleep(urandom.uniform(1,5))
        led.value(1)
        timer_start=utime.ticks_ms()
        
        while button.value()==0:
            pass
        timer_reaction=utime.ticks_diff(utime.ticks_ms(), timer_start)
        oled.fill(0)
        oled.text("Your Time",25,25)
        oled.text(str(timer_reaction),50,50)
        oled.show()
        led.value(0)
        utime.sleep(1.5)
        
def show_your_reaction_score():
    best_score = 9999
    while True:
        led.value(0)
        oled.fill(0)
        oled.text("press the button",0,10)
        oled.text("TO START!",25,25)
        oled.show()
        
        while button.value()==0:
            pass
        oled.fill(0)
        oled.text("Wait For LED",15,30)
        oled.show()
        
        utime.sleep(urandom.uniform(1,5))
        led.value(1)
        timer_start=utime.ticks_ms()
        
        while button.value()==0:
            pass
        timer_reaction=utime.ticks_diff(utime.ticks_ms(), timer_start)
        if timer_reaction < best_score:
            best_score = timer_reaction
        oled.fill(0)
        oled.text("Your Time",25,25)
        oled.text(str(timer_reaction),26,35)
        oled.text("best score",26,45)
        oled.text(str(best_score),26,55)
        oled.show()
        led.value(0)
        utime.sleep(2.5)

# show_your_reaction()
show_your_reaction_score()