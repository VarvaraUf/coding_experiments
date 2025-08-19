from machine import Pin,ADC,PWM
import utime 


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
            
# meet_the_light_bulp()
adjust_blinck_speed()



