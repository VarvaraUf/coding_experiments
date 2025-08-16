from machine import Pin, ADC
from picobricks import WS2812
import utime
push_button = Pin(10,Pin.IN,Pin.PULL_DOWN)#initialize digital pin 10 as an input
ldr = ADC(Pin(27))
led = Pin(7,Pin.OUT)
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
LIGHT_BLUE = (48, 200, 207)
LIGHT_PINK = (255, 148, 202)
LIGHT_YELLOW = (255, 255, 132)
LIGHT_GREENESH = (128, 255, 255)
LIGHT_ORANGE = (237, 165, 84)
DARCK_PINK = (255, 0, 128)
LIGHT_RED = (255, 115, 115)
DARCK_GREEN = (128, 128, 0)
LIGHT_GREEN = (128, 255, 128)
GOLLDEN = (151, 75, 0)

COLORS = (RED, ORANGE, YELLOW, GREEN, BLUE, TURCOISE, VIOLET, WHITE, LIGHT_BLUE, LIGHT_PINK, LIGHT_YELLOW, LIGHT_GREENESH, LIGHT_ORANGE, DARCK_PINK, LIGHT_RED, DARCK_GREEN, LIGHT_GREEN, GOLLDEN)

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
long_press_start_time_ms = 0
color_index = 0
is_routine_enabled = False
def rotate_colors_when_dark_and_routine_enabled():
    global previous_button_state
    global long_press_start_time_ms
    global color_index
    global is_routine_enabled

    current_time = utime.ticks_ms()

    # Button falling edge detection
    if push_button.value() == 0 and previous_button_state == 1:
        is_routine_enabled = not is_routine_enabled  # toggle is_routine_enabled on/off
        long_press_start_time_ms = current_time  # reset timer so next change is in 500ms
        print(utime.ticks_ms(), "Button pressed, is_routine_enabled=", is_routine_enabled)        
            
    previous_button_state = push_button.value()
    
    if is_routine_enabled and ldr.read_u16() > 10000 and utime.ticks_diff(current_time, long_press_start_time_ms) >= 500:    
        print(utime.ticks_ms(), "Fill and show color: ", COLORS[color_index])
        ws.pixels_fill(COLORS[color_index])
        ws.pixels_show()
        
        color_index += 1
        if color_index == len(COLORS):
            color_index = 0
            
        long_press_start_time_ms = current_time  
        
    if is_routine_enabled == False or ldr.read_u16() <= 10000:
        ws.pixels_fill((0, 0, 0,))
        ws.pixels_show()
        print(utime.ticks_ms(), "we are turning of the ws2812")
        
long_press_start_time_ms = 0
previous_button_state = 0
long_press_in_progres = False
is_routine_enabled = False
color_index = 0
is_long_press_hapened = False
def switch_color_on_button_long_press():
    global long_press_start_time_ms
    global previous_button_state    
    global long_press_in_progres
    global is_routine_enabled
    global color_index
    global is_long_press_hapened    

    # print(utime.ticks_ms(), "previous_button_state", previous_button_state, "push_button.value()", push_button.value(), "is_long_click_hapened", is_long_click_hapened)
    if push_button.value() == 0 and previous_button_state == 1:
        if is_long_press_hapened == False:
            is_routine_enabled = not is_routine_enabled
            print(utime.ticks_ms(),"click")

        is_long_press_hapened = False

    # print(utime.ticks_ms(), "ldr.read_u16() > 10000", ldr.read_u16() > 10000,"is_routine_enabled",is_routine_enabled)
    if is_routine_enabled and ldr.read_u16() > 10000:
        ws.pixels_fill(COLORS[color_index])
        ws.pixels_show()

    if is_routine_enabled == False or ldr.read_u16() <= 10000:
        ws.pixels_fill((0, 0, 0))
        ws.pixels_show()       

    if push_button.value() == 1 and previous_button_state == 0:
        long_press_in_progres = True
        long_press_start_time_ms = utime.ticks_ms()

    if long_press_in_progres and push_button.value() == 1 and previous_button_state == 1 and (utime.ticks_ms() - long_press_start_time_ms) >= 1000:
        print("long click")
        is_long_press_hapened = True
        long_press_in_progres = False
        color_index += 1
        if color_index == len(COLORS):
            color_index = 0

    previous_button_state = push_button.value()

    
has_time_passed = True
def rotate_colors():
    global long_press_start_time_ms
    global previous_button_state 
    global color_index
    global has_time_passed
    global is_routine_enabled

    print(utime.ticks_ms())
    if push_button.value() == 0 and previous_button_state == 1:
        is_routine_enabled = not is_routine_enabled
        print(utime.ticks_ms(),"is_routine_enabled",is_routine_enabled)

    if is_routine_enabled and has_time_passed and ldr.read_u16() > 10000:
        ws.pixels_fill(COLORS[color_index])
        ws.pixels_show()
        long_press_start_time_ms = utime.ticks_ms()
        
        print(utime.ticks_ms(),"is_routine_enabled",is_routine_enabled,"has_time_passed",has_time_passed)

    has_time_passed = False

    if is_routine_enabled and (utime.ticks_ms() - long_press_start_time_ms) >= 500:
        has_time_passed = True
        color_index += 1
        if color_index == len(COLORS):
            color_index = 0
        print(utime.ticks_ms(),"has_time_passed",has_time_passed,"is_routine_enabled",is_routine_enabled)

    

    previous_button_state = push_button.value()

rotation_delay = 500
last_color_change_ms = 0
last_long_press_ms = 0
indicate_long_press = False
def rotate_colors_and_adjust_speed():
    global long_press_start_time_ms
    global previous_button_state 
    global last_long_press_ms
    global color_index
    global has_time_passed
    global is_routine_enabled
    global rotation_delay
    global indicate_long_press
    global is_long_press_hapened  
    global long_press_in_progres   
    global last_color_change_ms
    # print(utime.ticks_ms(), 
    #       "previous_button_state=", previous_button_state,
    #       "push_button.value=",push_button.value(),
    #       "is_long_click_hapened=",is_long_click_hapened)
    if push_button.value() == 0 and previous_button_state == 1:
        if is_long_press_hapened == False:
            print(utime.ticks_ms(),"click")
            is_routine_enabled = not is_routine_enabled

        is_long_press_hapened = False

    # turn led off
    
    if is_routine_enabled == False or indicate_long_press or ldr.read_u16() <= 10000:
        ws.pixels_fill((0, 0, 0))
        ws.pixels_show()    
    else:
        if (utime.ticks_ms() - last_color_change_ms) >= rotation_delay:
            color_index += 1
            if color_index == len(COLORS):
                color_index = 0
            
            ws.pixels_fill(COLORS[color_index])
            ws.pixels_show()
            last_color_change_ms = utime.ticks_ms()
        # print(utime.ticks_ms(),"has_time_passed",has_time_passed,"is_routine_enabled",is_routine_enabled)

    if push_button.value() == 1 and previous_button_state == 0:
        long_press_in_progres = True
        long_press_start_time_ms = utime.ticks_ms()

    # print(utime.ticks_ms(), 
    #       "previous_button_state=", previous_button_state,
    #       "push_button.value=",push_button.value(),
    #       "is_long_click_hapened=",is_long_click_hapened,
    #       "long_press_in_progres", long_press_in_progres,
    #       utime.ticks_ms() - previous_ticks_ms)

    if long_press_in_progres and push_button.value() == 1 and previous_button_state == 1 and (utime.ticks_ms() - long_press_start_time_ms) >= 1000:
        print("long press")
        is_long_press_hapened = True
        long_press_in_progres = False
        indicate_long_press = True
        last_long_press_ms = utime.ticks_ms()    

        rotation_delay -= 50
        if rotation_delay == 0:
            rotation_delay = 500
        print(utime.ticks_ms(), "speed", rotation_delay)

    if (utime.ticks_ms() - last_long_press_ms) >= 500:
        indicate_long_press = False

    previous_button_state = push_button.value()

hue_value = 0
color_change_step_value = 1
color_loops_counter = 0
last_time_signal_led_changed_ms = 0 
def rotate_rainbow_colors():
    global previous_button_state
    global is_routine_enabled
    global is_long_press_hapened
    global long_press_in_progres
    global long_press_start_time_ms
    global hue_value
    global color_change_step_value
    global color_loops_counter
    global last_time_signal_led_changed_ms

    if (utime.ticks_ms() - last_time_signal_led_changed_ms) >= 200:
        led.value(0)

    if push_button.value() == 0 and previous_button_state == 1:
        if is_long_press_hapened == False:
            print("click")
            is_routine_enabled = not is_routine_enabled
            led.value(1)
            last_time_signal_led_changed_ms = utime.ticks_ms()

        is_long_press_hapened = False    
        
    if is_routine_enabled and ldr.read_u16() > 10000:
        print(utime.ticks_ms(),
              "hue_value",hue_value,"step",color_change_step_value,"loops", color_loops_counter,"light level", ldr.read_u16())
        hue_value += color_change_step_value

        if hue_value >= 360:
            hue_value = 0
            color_loops_counter += 1

        ws.pixels_fill_hsv((hue_value, 100, 100))
        ws.pixels_show()        
    else:
        ws.pixels_fill((0, 0, 0,))
        ws.pixels_show()


    if push_button.value() == 1 and previous_button_state == 0:
        long_press_in_progres = True
        long_press_start_time_ms = utime.ticks_ms()

    if long_press_in_progres and push_button.value() == 1 and previous_button_state == 1 and (utime.ticks_ms() - long_press_start_time_ms) >= 1000:
        print("long press")
        long_press_in_progres = False
        is_long_press_hapened = True

        color_change_step_value += 1
        if color_change_step_value > 10:
            color_change_step_value = 1

        led.value(1)
        last_time_signal_led_changed_ms = utime.ticks_ms()      
            
    previous_button_state = push_button.value()


while True:
    utime.sleep(0.02)
    #rotate_colors_when_dark_blocking()
    #rotate_colors_when_dark_and_routine_enabled()
    #switch_color_on_button_long_press()
    #rotate_colors()
    #rotate_colors_and_adjust_speed()
    rotate_rainbow_colors()