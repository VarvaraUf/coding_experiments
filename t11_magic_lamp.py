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



class MagicLamp:
    last_clap_time = 0

    def __init__(self):
        self.sound_sensor = Pin(9,Pin.IN)
        self.led = Pin(7,Pin.OUT)
        
        self.led.value(0)

    def on_clap(self, pin):        
        if (utime.ticks_ms() - self.last_clap_time) <= 200:
            print(utime.ticks_ms(), 'on_clap skip', pin.value())
            return
        print(utime.ticks_ms(), 'on_clap toggle', pin.value())
        self.led.value(not self.led.value())
        self.last_clap_time = utime.ticks_ms()
        
        
    def run(self):
        self.sound_sensor.irq(trigger=Pin.IRQ_RISING, handler=self.on_clap)
        while True:
            pass

# magic_lamp()
# magic_lamp_rrq()
magic_lamp_object = MagicLamp()
magic_lamp_object.run()