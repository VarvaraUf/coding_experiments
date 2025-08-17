from machine import Pin,ADC,PWM
import utime 


led=PWM(Pin(7))
pot=ADC(Pin(26,Pin.IN))

led.freq(1000)

def meet_the_light_bulp():
    while True:
        led.duty_u16(pot.read_u16())
        print("potantiometer",pot.read_u16())
        
        utime.sleep(0.3)
    
meet_the_light_bulp()
    
    