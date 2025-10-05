from machine import Pin, PWM, I2C
from utime import sleep
from picobricks import SSD1306_I2C
import utime

def digital_ruler():
    #define the libraries
    redLed=Pin(7,Pin.OUT)
    button=Pin(10,Pin.IN,Pin.PULL_DOWN)
    buzzer=PWM(Pin(20,Pin.OUT))
    buzzer.freq(392)
    trigger = Pin(15, Pin.OUT)
    echo = Pin(14, Pin.IN)
    #define input and output pins
    WIDTH = 128                                            
    HEIGHT = 64                                       
    #OLED screen settings
    sda=Pin(4)
    scl=Pin(5)
    i2c=I2C(0,sda=sda, scl=scl)
        
    #initialize digital pin 4 and 5 as an OUTPUT for OLED communication
    oled = SSD1306_I2C(WIDTH, HEIGHT,i2c)
    measure = 0
    finalDistance = 0

    def getDistance():
        trigger.low()
        utime.sleep_us(2)
        trigger.high()
        utime.sleep_us(5)
        trigger.low()
        while echo.value() == 0:
            signaloff = utime.ticks_us()
        while echo.value() == 1:
            signalon = utime.ticks_us()
        timepassed = int(signalon) - int(signaloff)
        distance = (timepassed * 0.0343) / 2
        return distance
    #calculate the distance
    def getMeasure(pin):
        global measure
        global finalDistance
        redLed.value(1)
        for i in range(20):
            measure += getDistance()
            sleep(0.05)
        redLed.value(0)
        finalDistance = (measure/20) + 1
        oled.fill(0)
        oled.show()
        oled.text(">Digital Ruller<", 2,5)
        oled.text("Distance " + str(round(finalDistance)) +" cm", 0, 32)
        oled.show()
    #print the specified distance to the specified x and y coordinates on the OLED screen
        print(finalDistance)
        buzzer.duty_u16(4000)
        sleep(0.05)
        buzzer.duty_u16(0)
        measure=0
        finalDistance=0
    #sound the buzzer  
    button.irq(trigger=Pin.IRQ_RISING, handler=getMeasure)
    while True:
        pass

class DigitalRuler:
    redLed=Pin(7,Pin.OUT)
    button=Pin(10,Pin.IN,Pin.PULL_DOWN)
    buzzer=PWM(Pin(20,Pin.OUT))
    buzzer.freq(392)
    trigger = Pin(15, Pin.OUT)
    echo = Pin(14, Pin.IN)

    WIDTH = 128                                            
    HEIGHT = 64                                       
    
    sda = Pin(4)
    scl = Pin(5)
    i2c = I2C(0, sda = sda, scl = scl)
        
    oled = SSD1306_I2C(WIDTH, HEIGHT, i2c)
    measure = 0
    finalDistance = 0
    state_handlers = None
    STATE_START = "start"
    STATE_PROGRESS = "progress"
    STATE_FINISH = "finish"
    state_counter = -1
    state = STATE_START
    last_click_time_ms = 0
    buzzer_time_on_ms = 0

    def __init__(self):
        self.state_handlers = {
            self.STATE_START: self.run_state_start,
            self.STATE_PROGRESS: self.run_state_progress,
            self.STATE_FINISH: self.run_state_finish
        }

    def getDistance(self):
        self.trigger.low()
        utime.sleep_us(2)
        self.trigger.high()
        utime.sleep_us(5)
        self.trigger.low()
        while self.echo.value() == 0:
            signaloff = utime.ticks_us()
        while self.echo.value() == 1:
            signalon = utime.ticks_us()
        timepassed = int(signalon) - int(signaloff)
        distance = (timepassed * 0.0343) / 2
        return distance

    def getMeasure(self):
        for i in range(20):
            self.measure += self.getDistance()
            sleep(0.05)
        self.finalDistance = (self.measure/20) + 1

    def set_state(self,state):
        self.state = state
        self.state_counter = -1

    def change_state_to_progress(self,pin):
        if (utime.ticks_ms() - self.last_click_time_ms) >= 200:
            self.set_state(self.STATE_PROGRESS)
            self.last_click_time_ms = utime.ticks_ms()        

    def change_state_to_start(self,pin):
        if (utime.ticks_ms() - self.last_click_time_ms) >= 200:
            self.set_state(self.STATE_START)
            self.last_click_time_ms = utime.ticks_ms()

    def run_state_start(self):
        if self.state_counter == 0:
            self.oled.fill(0)
            self.oled.text("press the button",1,6)
            self.oled.text("to start!",1,21)
            self.oled.show()
            self.button.irq(trigger=Pin.IRQ_RISING, handler=self.change_state_to_progress)
        

    def run_state_progress(self):
        if self.state_counter == 0:
            self.oled.fill(0)
            self.oled.text("measure in", 2, 6)
            self.oled.text("progress", 0, 21)
            self.oled.show()
            self.redLed.value(1)
            self.getMeasure()
            self.redLed.value(0)
            self.set_state(self.STATE_FINISH)

    def run_state_finish(self):
        if self.state_counter == 0:
            self.oled.fill(0)
            self.oled.text(">Digital Ruller<", 2,5)
            self.oled.text("Distance " + str(round(self.finalDistance)) +" cm", 0, 32)
            self.oled.show()
            self.buzzer.duty_u16(4000)
            self.buzzer_time_on_ms = utime.ticks_ms()
            self.measure=0
            self.finalDistance=0
            self.button.irq(trigger=Pin.IRQ_RISING, handler=self.change_state_to_start)

        if (utime.ticks_ms() - self.buzzer_time_on_ms) >= 100:
            self.buzzer.duty_u16(0)

    def run(self):
        while True:
            utime.sleep(0.01)
            self.state_counter += 1
            handler = self.state_handlers[self.state] # type: ignore
            handler()

class buzzer:
    button = Pin(10,Pin.IN,Pin.PULL_DOWN)
    buzzer = PWM(Pin(20,Pin.OUT))
    sound_patterns = []
    pattern_index = -1
    last_click_time_ms = 0
    times = 0
    on_ms = 0
    off_ms = 0
    last_buzzer_toggle_ms = 0
    last_toggle_time_ms = 0

    def __init__(self,list):
        self.sound_patterns = list
        self.buzzer.freq(313)

    def on_button_click(self,pin):
        if pin.value() == 0:
            return
        
        if (utime.ticks_ms() - self.last_click_time_ms) < 200:
            return
        
        self.pattern_index += 1
        if self.pattern_index == len(self.sound_patterns):
            self.pattern_index = 0

        self.last_click_time_ms = utime.ticks_ms()

        self.times = self.sound_patterns[self.pattern_index][0]
        self.on_ms = self.sound_patterns[self.pattern_index][1]
        self.off_ms = self.sound_patterns[self.pattern_index][2]

    def buzz(self):
        if self.times == 0:
            return
        
        now = utime.ticks_ms()

        if now - self.last_buzzer_toggle_ms >= self.off_ms and self.buzzer.duty_u16() == 0:
            self.buzzer.duty_u16(4000)
            print(utime.ticks_ms(),"turn buzzer on")
            self.last_buzzer_toggle_ms = utime.ticks_ms()
        
        if now - self.last_buzzer_toggle_ms >= self.on_ms and self.buzzer.duty_u16() == 4000:
            self.buzzer.duty_u16(0)
            print(utime.ticks_ms(),"turn buzzer off")
            self.last_buzzer_toggle_ms = utime.ticks_ms()
            self.times -= 1

    def run(self):
        self.button.irq(trigger=Pin.IRQ_RISING, handler=self.on_button_click)
        while True:
            sleep(0.05)
            self.buzz()

buzzer_object = buzzer([(1,50,500),(2,50,150),(3,500,50),(4,50,250),(5,150,250)])
buzzer_object.run()
        
    

# digital_ruler_object = DigitalRuler()
# digital_ruler_object.run()