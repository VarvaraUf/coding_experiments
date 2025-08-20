from machine import Pin,ADC,PWM,I2C
from picobricks import SSD1306_I2C, SHTC3
import utime 

WIDTH=128
HEIGHT=64

i2c = I2C(0, scl=Pin(5), sda=Pin(4))   
oled = SSD1306_I2C(WIDTH, HEIGHT, i2c)
shtc_sensor = SHTC3(i2c)
push_button = Pin(10,Pin.IN,Pin.PULL_DOWN)
led_pwm = PWM(Pin(7))
led = Pin(7, Pin.OUT)
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




# meet_the_light_bulp()
#adjust_blinck_speed()
#adjust_blinck_speed_and_display_the_speed()
adjust_blinck_speed_and_display_the_speed_and_enable_by_button()

