from machine import Pin, ADC
from picobricks import WS2812
import utime
push_button = Pin(10,Pin.IN,Pin.PULL_DOWN)#initialize digital pin 10 as an input
ldr = ADC(Pin(27))
ws = WS2812(brightness=0.1)
#define the input and output pins

#define colors
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
VIOLET = (255, 0, 255)
YELLOW = (255, 255, 0)
TURCOISE = (0, 255, 255)
WHITE = (255, 255, 255)
ORANGE = (255, 165, 0)
COLORS = (RED, ORANGE, YELLOW, GREEN, BLUE, TURCOISE, VIOLET, WHITE)
#RGB color Code

def rotate_colors_when_dark_blocking():
    if(ldr.read_u16()>10000):#let's check the ldr sensor
        for color in COLORS:            
            #turn on the LDR
            print(utime.ticks_ms(),"color",color)
            ws.pixels_fill(color)
            ws.pixels_show()
            
            utime.sleep(0.5)
    else:
        ws.pixels_fill((0,0,0))  #turn off the RGB
        ws.pixels_show()
        
        
previous_button_state = 0
previous_ticks_ms = 0
color_index = 0
is_routine_enabled = False
def rotate_colors_when_dark_and_routine_enabled():
    global previous_button_state
    global previous_ticks_ms
    global color_index
    global is_routine_enabled

    current_time = utime.ticks_ms()

    # Button falling edge detection
    if push_button.value() == 0 and previous_button_state == 1:
        is_routine_enabled = not is_routine_enabled  # toggle is_routine_enabled on/off
        previous_ticks_ms = current_time  # reset timer so next change is in 500ms
        print(utime.ticks_ms(), "Button pressed, is_routine_enabled=", is_routine_enabled)        
            
    previous_button_state = push_button.value()
    
    if is_routine_enabled and ldr.read_u16() > 10000 and utime.ticks_diff(current_time, previous_ticks_ms) >= 500:    
        print(utime.ticks_ms(), "Fill and show color: ", COLORS[color_index])
        ws.pixels_fill(COLORS[color_index])
        ws.pixels_show()
        
        color_index += 1
        if color_index == len(COLORS):
            color_index = 0
            
        previous_ticks_ms = current_time  
        
    if is_routine_enabled == False or ldr.read_u16() <= 10000:
        ws.pixels_fill((0, 0, 0,))
        ws.pixels_show()
        print(utime.ticks_ms(), "we are turning of the ws2812")
        
previous_ticks_ms = 0
previous_button_state = 0
long_press_in_progres = False
is_routine_enabled = False
color_index = 0
is_long_click_hapened = False
def switch_color_on_button_long_press():
    global previous_ticks_ms
    global previous_button_state    
    global long_press_in_progres
    global is_routine_enabled
    global color_index
    global is_long_click_hapened    

    # print(utime.ticks_ms(), "previous_button_state", previous_button_state, "push_button.value()", push_button.value(), "is_long_click_hapened", is_long_click_hapened)
    if push_button.value() == 0 and previous_button_state == 1:
        if is_long_click_hapened == False:
            is_routine_enabled = not is_routine_enabled
            print(utime.ticks_ms(),"click")

        is_long_click_hapened = False

    # print(utime.ticks_ms(), "ldr.read_u16() > 10000", ldr.read_u16() > 10000,"is_routine_enabled",is_routine_enabled)
    if is_routine_enabled and ldr.read_u16() > 10000:
        ws.pixels_fill(COLORS[color_index])
        ws.pixels_show()

    if is_routine_enabled == False or ldr.read_u16() <= 10000:
        ws.pixels_fill((0, 0, 0))
        ws.pixels_show()       

    if push_button.value() == 1 and previous_button_state == 0:
        long_press_in_progres = True
        previous_ticks_ms = utime.ticks_ms()

    if long_press_in_progres and push_button.value() == 1 and previous_button_state == 1 and (utime.ticks_ms() - previous_ticks_ms) >= 1000:
        print("long click")
        is_long_click_hapened = True
        long_press_in_progres = False
        color_index += 1
        if color_index == len(COLORS):
            color_index = 0

    previous_button_state = push_button.value()

while True:
    utime.sleep(0.2)
    #rotate_colors_when_dark_blocking()
    #rotate_colors_when_dark_and_routine_enabled()
    switch_color_on_button_long_press()