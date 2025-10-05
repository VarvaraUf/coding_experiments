from machine import Pin, I2C
from picobricks import SSD1306_I2C, WS2812
import utime
import urandom
import _thread


WIDTH  = 128                                            
HEIGHT = 64   

sda=Pin(4)
scl=Pin(5)
i2c=I2C(0,sda=sda, scl=scl)
ws = WS2812(pin_num=6, num_leds=1, brightness=0.05)
oled = SSD1306_I2C(WIDTH, HEIGHT, i2c)

button = Pin(10,Pin.IN,Pin.PULL_DOWN)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

COLORS = (RED,GREEN,BLUE,WHITE)
TEXTS = ("RED","GREEN","BLUE","WHITE")

oled.fill(0)
oled.show()

ws.pixels_fill(BLACK)
ws.pixels_show()

global button_pressed
score=0
button_pressed = False
ledcolor = None

def random_rgb():
    global ledcolor
    ledcolor=urandom.randint(0,3)
    ws.pixels_fill(COLORS[ledcolor])
    ws.pixels_show()

def random_text():
    global oledtext
    oledtext=urandom.randint(0,3)
    oled.fill(0)
    oled.text(TEXTS[oledtext],45,32)
    oled.show()

def button_reader_thread():
    while True:
        global button_pressed
        if button_pressed == False:
            if button.value() == 1:
                button_pressed = True
                global score
                global oledtext
                global ledcolor
                if ledcolor == oledtext:
                    score += 10
                else:
                    score -= 10
        utime.sleep(0.01)

_thread.start_new_thread(button_reader_thread, ())
oled.fill(0)
oled.text("The Game Begins",0,10)
oled.show()
utime.sleep(2)

for i in range(10):
    random_text()
    random_rgb()
    button_pressed=False
    utime.sleep(1.5)
utime.sleep(1.5)
oled.fill(0)
oled.text("Your total score:",0,20)
oled.text(str(score), 57,40)
oled.show()
ws.pixels_fill(BLACK)
ws.pixels_show()