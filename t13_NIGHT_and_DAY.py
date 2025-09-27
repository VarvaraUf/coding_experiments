from machine import Pin, I2C, Timer, ADC, PWM
from picobricks import SSD1306_I2C
import utime
import urandom
#define the libraries
def NIGHT_and_DAY():
    WIDTH = 128
    HEIGHT = 64
    #OLED Screen Settings
    sda=Pin(4)
    scl=Pin(5)
    #initialize digital pin 4 and 5 as an OUTPUT for OLED Communication
    i2c=I2C(0,sda=sda, scl=scl)
    oled = SSD1306_I2C(WIDTH, HEIGHT, i2c)
    buzzer = PWM(Pin(20))
    buzzer.freq(440)
    ldr=ADC(Pin(27))
    button=Pin(10,Pin.IN,Pin.PULL_DOWN)
    #define the input and output pins
    
    #OLED Screen Texts Settings

    def changeWord():
        global NIGHT_OR_DAY
        oled.fill(0)
        oled.show()
        NIGHT_OR_DAY=round(urandom.uniform(0,1))
        #when data is '0', OLED texts NIGHT
        if NIGHT_OR_DAY==0:
            oled.text("---NIGHT---", 20, 30)
            oled.show()
        else:
            oled.text("---DAY---", 20, 30)
            oled.show()
        #waits for the button to be pressed to activate
            
    while button.value()==0:
        print("Press the Button")
        utime.sleep(0.01)
        
    oled.fill(0)
    oled.show()
    start=1
    score = 0
    while start==1:
        global gamerReaction
        
        changeWord()
        startTime=utime.ticks_ms()
        #when LDR's data greater than 2000, gamer reaction '0'
        while utime.ticks_diff(utime.ticks_ms(), startTime)<=2000:
            if ldr.read_u16()>20000:
                gamerReaction=0
            #when LDR's data lower than 2000, gamer reaction '1'
            else:
                gamerReaction=1
            utime.sleep(0.01)
        #buzzer working
        buzzer.duty_u16(2000)
        utime.sleep(0.05)
        buzzer.duty_u16(0)
        if gamerReaction==NIGHT_OR_DAY:
            score += 10
        #when score is 10, OLED says 'Game Over'
        else:
            oled.fill(0)
            oled.show()
            oled.text("Game Over", 0, 18, 1)
            oled.text("Your score " + str(score), 0,35)
            oled.text("Press RESET",0, 45)
            oled.text("To REPEAT",0,55)
            oled.show()
            buzzer.duty_u16(2000)
            utime.sleep(0.05)
            buzzer.duty_u16(0)
            break
        if score==100:
            #when score is 10, OLED says 'You Won'
            oled.fill(0)
            oled.show()
            oled.text("Congratulations", 10, 10)
            oled.text("Top Score: 100", 5, 35)
            oled.show()
            buzzer.duty_u16(2000)
            utime.sleep(0.1)
            buzzer.duty_u16(0)
            utime.sleep(0.1)
            buzzer.duty_u16(2000)
            utime.sleep(0.1)
            buzzer.duty_u16(0)
            break

class Beeper:
    buzzer = PWM(Pin(20))
    button = Pin(10, Pin.IN, Pin.PULL_DOWN)
    last_click_time_ms = 0
    CLICK_DEBOUNCE_TIME = 200
    click_counter = 0
    
    last_beep_time_ms = 0
    beep_times = 0
    beep_delay = 0
    silence_delay = 0
    beep_on = False
    beep_patterns = (
        (1, 50, 100),
        (2, 50, 100),
        (3, 50, 100),
        (1, 500, 100),
        (2, 250, 100),
        (3, 125, 100)
    )

    def __init__(self) -> None:
        self.buzzer.freq(440)

    def button_click(self, pin):
        if pin.value() == 0:
            return
        
        now_ms = utime.ticks_ms()
        if (now_ms - self.last_click_time_ms) < self.CLICK_DEBOUNCE_TIME:
            return
        
        print(now_ms, 'button_click', self.click_counter)
        self.last_click_time_ms = now_ms
        times, delay, silence = self.beep_patterns[self.click_counter % len(self.beep_patterns)]
        self.configure_beep(times, delay, silence)
        self.click_counter += 1

    def run(self):
        self.button.irq(trigger=Pin.IRQ_FALLING, handler=self.button_click)
        while True:
            utime.sleep(0.01)
            self.beep()

    def beep(self):
        if self.beep_times == 0:
            return
        
        now_ms = utime.ticks_ms()
        time_passed = now_ms - self.last_beep_time_ms
        if self.beep_on and time_passed > self.beep_delay:
            print(now_ms, 'beep silence cycle start', self.beep_times, self.beep_delay, self.silence_delay)
            self.buzzer.duty_u16(0)
            self.beep_on = False
            self.last_beep_time_ms = now_ms
            self.beep_times -= 1
            return
        
        if self.beep_on == False and time_passed > self.silence_delay:
            print(now_ms, 'beep on cycle start', self.beep_times, self.beep_delay, self.silence_delay)
            self.buzzer.duty_u16(2000)
            self.beep_on = True
            self.last_beep_time_ms = now_ms
            return
        

    def configure_beep(self, times, delay, silence):
        print(utime.ticks_ms(), f"configure_beep {self.beep_times}!, {times}, {delay}, {silence}",)
        if self.beep_times != 0:
            return
        
        self.beep_times = times
        self.beep_delay = delay
        self.silence_delay = silence

class NightAndDay:
    WIDTH = 128
    HEIGHT = 64
    oled: SSD1306_I2C
    i2c: I2C
    ldr: ADC
    buzzer: PWM
    button: Pin
    STATE_START = "STATE_START"
    STATE_GO = "go"
    STATE_LOOSE = "loose"
    STATE_WIN = "win"
    state = STATE_START
    state_handlers = None
    state_counter = -1
    score = 0   
    NIGHT_OR_DAY = None 
    gamerReaction = None
    buzzer_on_time = 0
    beeper = Beeper()
    startTime = 0

    #OLED Screen Settings
    def __init__(self):
        sda = Pin(4)
        scl = Pin(5)
        self.i2c = I2C(0, sda=sda, scl=scl)
        self.oled = SSD1306_I2C(self.WIDTH, self.HEIGHT, self.i2c)
        self.buzzer = PWM(Pin(20))
        self.ldr = ADC(Pin(27))
        self.button = Pin(10, Pin.IN, Pin.PULL_DOWN)

        self.state_handlers = {
            self.STATE_START: self.run_state_start,
            self.STATE_GO: self.run_state_go,
            self.STATE_WIN: self.run_state_win,
            self.STATE_LOOSE: self.run_state_loose
        }

        self.buzzer.freq(440)

    def run_state_start(self):
        if self.state_counter == 0:
            self.oled.fill(0)
            self.oled.text("NIGHT and DAY", 10, 0)
            self.oled.text("<GAME>", 40, 20)
            self.oled.text("Press the Button", 0, 40)
            self.oled.text("to START!", 40, 55)
            self.oled.show()
            self.beeper.configure_beep(1, 100, 0)

        if self.button.value() == 1:
            self.state = self.STATE_GO
            self.state_counter = -1
            self.oled.fill(0)
            self.oled.show()

    def change_word(self):
        self.NIGHT_OR_DAY=round(urandom.uniform(0, 1))
        self.oled.fill(0)
        if self.NIGHT_OR_DAY==0:
            self.oled.text("---NIGHT---", 20, 30)       
        else:
            self.oled.text("---DAY---", 20, 30)
            
        self.oled.show()
        
    def run_state_go(self):
        if self.state_counter == 0:
            self.score = 0

        if utime.ticks_diff(utime.ticks_ms(), self.startTime)>2000:
            if self.state_counter != 0:
                if self.gamerReaction == self.NIGHT_OR_DAY:
                    self.score += 10
                else:
                    self.score -= 10
                    self.state = self.STATE_LOOSE
                    self.state_counter = -1
                    return                    

                if self.score == 100:
                    self.state = self.STATE_WIN
                    self.state_counter = -1
                    return
                    
            
            self.change_word()
            self.beeper.configure_beep(1,50,0)
            self.startTime=utime.ticks_ms()
        else:
            if self.ldr.read_u16()>=20000:
                self.gamerReaction=0            
            else:
                self.gamerReaction=1

    def run_state_loose(self):
        if self.state_counter == 0:
            self.oled.fill(0)
            self.oled.show()
            self.oled.text("Game Over", 0, 18, 1)
            self.oled.text("Your score " + str(self.score), 0,31)
            self.oled.text("Press The button",0, 45)
            self.oled.text("To REPEAT",0,55)
            self.oled.show()
            self.beeper.configure_beep(2, 150, 100)

        if self.button.value() == 1:
            self.state = self.STATE_START
            self.state_counter = -1
            self.oled.fill(0)
            self.oled.show()
            utime.sleep(0.3)

    def run_state_win(self):
        if self.state_counter == 0:
            self.oled.fill(0)
            self.oled.show()
            self.oled.text("Congratulations", 10, 10)
            self.oled.text("Top Score: 100", 5, 35)
            self.oled.text("Press The button",0, 45)
            self.oled.text("To REPEAT",0,55)
            self.oled.show()
            self.beeper.configure_beep(3, 150, 100)

        if self.button.value() == 1:
            self.state = self.STATE_START
            self.state_counter = -1
            self.oled.fill(0)
            self.oled.show()
            utime.sleep(0.3)

    def run(self) -> None:
        while True:
            utime.sleep(0.01)
            self.state_counter += 1
            self.beeper.beep()
            self.handler = self.state_handlers[self.state] # type: ignore
            self.handler()

night_and_day_object = NightAndDay()
night_and_day_object.run()
# NIGHT_and_DAY()
# beeper = Beeper()
# beeper.run()
