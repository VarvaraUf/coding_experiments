from machine import Pin,ADC,PWM,I2C
from picobricks import SSD1306_I2C, SHTC3,WS2812
import utime 

WIDTH=128
HEIGHT=64

i2c = I2C(0, scl=Pin(5), sda=Pin(4))   
oled = SSD1306_I2C(WIDTH, HEIGHT, i2c)
shtc_sensor = SHTC3(i2c)
push_button = Pin(10,Pin.IN,Pin.PULL_DOWN)
led_pwm = PWM(Pin(7))
led = Pin(7, Pin.OUT)
ws = WS2812(brightness=0.1)
ldr = ADC(Pin(27))
pot=ADC(Pin(26,Pin.IN))





led_pwm.freq(1000)

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

def meet_the_light_bulp():
    while True:
        led_pwm.duty_u16(pot.read_u16())
        print("potantiometer1",pot.read_u16())
        
        utime.sleep(0.3)

def adjust_blinck_speed():
    previous_signal_time_ms = 0
    led_speed_delay = 500

    while True:
        utime.sleep(0.005)
        # print(utime.ticks_ms(),"potantiometer2",pot.read_u16(),"(utime.ticks_ms() - previous_signal_time_ms)",(utime.ticks_ms() - previous_signal_time_ms))
        if (utime.ticks_ms() - previous_signal_time_ms) >= led_speed_delay:
            print("potantiometer4",pot.read_u16(),"led_speed_delay",int(led_speed_delay),"(utime.ticks_ms() - previous_signal_time_ms)",(utime.ticks_ms() - previous_signal_time_ms))
            led.value(not led.value())
            previous_signal_time_ms = utime.ticks_ms()
        led_speed_delay = map_u16_value(pot.read_u16(), 50, 1000)
        
        # print("potantiometer3",pot.read_u16(),"led_speed_delay",led_speed_delay)

def adjust_blinck_speed_and_display_the_speed():
    previous_signal_time_ms = 0
    led_speed_delay = 500

    while True:
        utime.sleep(0.005)

        # print(utime.ticks_ms(),"potantiometer2",pot.read_u16(),"(utime.ticks_ms() - previous_signal_time_ms)",(utime.ticks_ms() - previous_signal_time_ms))
        if (utime.ticks_ms() - previous_signal_time_ms) >= led_speed_delay:
            print("potantiometer", pot.read_u16(), "led_speed_delay", int(led_speed_delay), "time passed", utime.ticks_ms() - previous_signal_time_ms)
            led.value(not led.value())
            previous_signal_time_ms = utime.ticks_ms()            

        led_speed_delay = map_u16_value(pot.read_u16(), 50, 1000)
        oled.fill(0)
        oled.text("Blinking", 21, 21)
        oled.text("delay", 21, 32)
        oled.text(str(int(led_speed_delay)), 21, 43)
        oled.show()
        

def adjust_blinck_speed_and_display_the_speed_and_enable_by_button():
    previous_signal_time_ms = 0
    led_speed_delay = 500
    previous_button_state = 0
    previous_ticks_ms = 0
    is_long_press_in_progress = False
    is_routine_enabled = False
    

    while True:
        utime.sleep(0.005)

        current_button_state = push_button.value()
        # print(utime.ticks_ms(), "current button", current_button_state, "prev button", previous_button_state)
        if current_button_state == 1 and previous_button_state == 0:
            previous_ticks_ms = utime.ticks_ms()
            is_long_press_in_progress = True
            

        # print(utime.ticks_ms(), "is_long_press_in_progress", is_long_press_in_progress,
        #        "current button", current_button_state, "prev button", previous_button_state,
        #        "time passed", (utime.ticks_ms() - previous_ticks_ms))
        if is_long_press_in_progress and current_button_state == 1 and previous_button_state == 1 and (utime.ticks_ms() - previous_ticks_ms) >= 1000:
            print("long press")
            is_routine_enabled = not is_routine_enabled
            is_long_press_in_progress = False

        # print(utime.ticks_ms(),"potantiometer2",pot.read_u16(),"(utime.ticks_ms() - previous_signal_time_ms)",(utime.ticks_ms() - previous_signal_time_ms))
        if is_routine_enabled == True:
            if (utime.ticks_ms() - previous_signal_time_ms) >= led_speed_delay:
                print("potantiometer", pot.read_u16(), "led_speed_delay", int(led_speed_delay), "time passed", utime.ticks_ms() - previous_signal_time_ms,is_long_press_in_progress)
                led.value(not led.value())
                previous_signal_time_ms = utime.ticks_ms()            

            led_speed_delay = map_u16_value(pot.read_u16(), 50, 1000)
            oled.fill(0)
            oled.text("Blinking", 21, 21)
            oled.text("delay", 21, 32)
            oled.text(str(int(led_speed_delay)), 21, 43)
            oled.show()

        else:
            led.value(0)
            oled.fill(0)
            oled.text("push the", 21, 21)
            oled.text("Button to", 21, 32)
            oled.text("turn it on", 21, 43)
            oled.show()        

        previous_button_state = current_button_state
        # print(utime.ticks_ms(), "previous_button_state", previous_button_state)


def manage_rgb_led_speed_and_brightness():
    previous_button_state = 0
    long_press_in_progres = False
    long_press_start_time_ms = 0
    previous_signal_time = 0
    is_long_press_hapened = False
    is_routine_enabled = False
    manage_state = "speed"
    color_index = 1
    brightness = 0.01
    speed = 1
    

    while True:
        utime.sleep(0.2)

        current_button_state = push_button.value()
        # print("current_button_state",current_button_state,"previous_button_state",previous_button_state,(utime.ticks_ms() - long_press_start_time_ms),"manage_state",manage_state)
        if current_button_state == 1 and previous_button_state == 0:
            long_press_in_progres = True
            long_press_start_time_ms = utime.ticks_ms()            

        if long_press_in_progres and current_button_state == 1 and previous_button_state == 1 and (utime.ticks_ms() - long_press_start_time_ms) >= 1000:
            print("long click")
            led.value(1)
            previous_signal_time = utime.ticks_ms()
            is_long_press_hapened = True
            long_press_in_progres = False
            is_routine_enabled = not is_routine_enabled

        if current_button_state == 0 and previous_button_state == 1:
            if is_long_press_hapened == False:
                print("click")
                led.value(1)
                previous_signal_time = utime.ticks_ms()

                if manage_state == "brightness":
                    manage_state = "speed"
                else:
                    manage_state = "brightness"

            is_long_press_hapened = False
        if (utime.ticks_ms() - previous_signal_time) >= 100:
            led.value(0)

        oled.fill(0)
        if is_routine_enabled == True:            
            color_index += 1
            if color_index == 360:
                color_index = 1

            ws.pixels_fill_hsv((color_index, 100, 100))
            ws.pixels_show()        

            if manage_state == "brightness":
                oled.text("-",12, 21)
            else:
                oled.text("-",12, 43)            
        
            oled.text("brightness:",21,21)
            oled.text(str(brightness),21,32)
            oled.text("speed:",21,43)
            oled.text(str(speed),21,53)
            oled.show()

        else:
            oled.show()
            ws.pixels_fill((0,0,0))
            ws.pixels_show()

        
            

                 

                
                    



        # print("manage_state",manage_state)
        previous_button_state = push_button.value()




# meet_the_light_bulp()
#adjust_blinck_speed()
#adjust_blinck_speed_and_display_the_speed()
# adjust_blinck_speed_and_display_the_speed_and_enable_by_button()
manage_rgb_led_speed_and_brightness() 

