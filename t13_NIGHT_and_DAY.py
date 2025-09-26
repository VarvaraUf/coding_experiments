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
    state = STATE_START
    state_handlers = None
    state_counter = -1
    is_routine_enabled = True
    score = 0    

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

        if self.button.value() == 1:
            self.state = self.STATE_GO
            self.state_counter = -1
            self.oled.fill(0)
            self.oled.show()

    def change_word(self):
        global NIGHT_OR_DAY
        NIGHT_OR_DAY=round(urandom.uniform(0, 1))
        
        if NIGHT_OR_DAY==0:
            self.oled.fill(0)
            self.oled.text("---NIGHT---", 20, 30)
            self.oled.show()
        else:
            self.oled.fill(0)
            self.oled.text("---DAY---", 20, 30)
            self.oled.show()

    def run_state_go(self):
        self.score = 0
        start = 1
        if self.state_counter == 0:
            while start == 1:
                global gamerReaction
                
                self.change_word()
                startTime=utime.ticks_ms()
                #when LDR's data greater than 2000, gamer reaction '0'
                while utime.ticks_diff(utime.ticks_ms(), startTime)<=2000:
                    if self.ldr.read_u16()>20000:
                        gamerReaction=0
                    #when LDR's data lower than 2000, gamer reaction '1'
                    else:
                        gamerReaction=1
                    utime.sleep(0.01)
                #buzzer working
                self.buzzer.duty_u16(2000)
                utime.sleep(0.05)
                self.buzzer.duty_u16(0)
                if gamerReaction==NIGHT_OR_DAY:
                    self.score += 10
                else:
                    self.score -= 10
                    self.is_routine_enabled = True
                    start = 0
                    
                if self.score == 100:
                    self.oled.fill(0)
                    self.oled.show()
                    self.oled.text("Congratulations", 10, 10)
                    self.oled.text("Top Score: 100", 5, 35)
                    self.oled.show()
                    self.buzzer.duty_u16(2000)
                    utime.sleep(0.1)
                    self.buzzer.duty_u16(0)
                    utime.sleep(0.1)
                    self.buzzer.duty_u16(2000)
                    utime.sleep(0.1)
                    self.buzzer.duty_u16(0)
                    start = 0
                    self.is_routine_enabled = False

            if self.is_routine_enabled == True:
                self.oled.fill(0)
                self.oled.show()
                self.oled.text("Game Over", 0, 18, 1)
                self.oled.text("Your score " + str(self.score), 0,31)
                self.oled.text("Press The button",0, 45)
                self.oled.text("To REPEAT",0,55)
                self.oled.show()
                self.buzzer.duty_u16(2000)
                utime.sleep(0.05)
                self.buzzer.duty_u16(0)
                utime.sleep(0.1)
                self.buzzer.duty_u16(2000)
                utime.sleep(0.1)
                self.buzzer.duty_u16(0)

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
            self.handler = self.state_handlers[self.state] # type: ignore
            self.handler()

night_and_day_object = NightAndDay()
night_and_day_object.run()
# NIGHT_and_DAY()