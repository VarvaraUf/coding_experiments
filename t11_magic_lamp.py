from machine import Pin
import utime
def magic_lamp():
    sensor=Pin(9,Pin.IN)
    led=Pin(7,Pin.OUT)

    while True:
        if sensor.value() == 1:
            led.value(1)  
        else:
            led.value(0)


def magic_lamp_rrq():
    global last_clap_time
    last_clap_time = 0

    sound_sensor = Pin(9,Pin.IN)
    led = Pin(7,Pin.OUT)
    led.value(0)

    def on_clap(pin):
        global last_clap_time
        
        if (utime.ticks_ms() - last_clap_time) <= 200:
            print(utime.ticks_ms(), 'on_clap skip', pin.value())
            return
        print(utime.ticks_ms(), 'on_clap toggle', pin.value())
        led.value(not led.value())
        last_clap_time = utime.ticks_ms()
        
    sound_sensor.irq(trigger=Pin.IRQ_RISING, handler=on_clap)
    while True:
        pass

magic_lamp_rrq()