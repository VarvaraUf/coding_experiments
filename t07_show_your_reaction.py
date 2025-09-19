from machine import Pin, I2C
from picobricks import SSD1306_I2C
import utime
import urandom
#define the library
WIDTH=128
HEIGHT=64
#define the width and height values
sda=Pin(4)
scl=Pin(5)
i2c= I2C(0,sda=sda, scl=scl)
oled = SSD1306_I2C(WIDTH, HEIGHT, i2c)
button = Pin(10,Pin.IN,Pin.PULL_DOWN)
led = Pin(7,Pin.OUT)
#define our input and output pins
def show_your_reaction():
    while True:
        led.value(0)
        oled.fill(0)
        oled.text("press the button",0,10)
        oled.text("TO START!",25,25)
        oled.show()
        
        while button.value()==0:
            pass
        oled.fill(0)
        oled.text("Wait For LED",15,30)
        oled.show()
        
        utime.sleep(urandom.uniform(1,5))
        led.value(1)
        timer_start=utime.ticks_ms()
        
        while button.value()==0:
            pass
        timer_reaction=utime.ticks_diff(utime.ticks_ms(), timer_start)
        oled.fill(0)
        oled.text("Your Time",25,25)
        oled.text(str(timer_reaction),50,50)
        oled.show()
        led.value(0)
        utime.sleep(1.5)
        
def show_your_reaction_score():
    best_score = 9999
    while True:
        led.value(0)
        oled.fill(0)
        oled.text("press the button",0,10)
        oled.text("TO START!",25,25)
        oled.show()
        
        while button.value()==0:
            pass
        oled.fill(0)
        oled.text("Wait For LED",15,30)
        oled.show()
        
        utime.sleep(urandom.uniform(1,5))
        led.value(1)
        timer_start=utime.ticks_ms()
        
        while button.value()==0:
            pass
        timer_reaction=utime.ticks_diff(utime.ticks_ms(), timer_start)
        if timer_reaction < best_score:
            best_score = timer_reaction
        oled.fill(0)
        oled.text("Your Time",25,25)
        oled.text(str(timer_reaction),26,35)
        oled.text("best score",26,45)
        oled.text(str(best_score),26,55)
        oled.show()
        led.value(0)
        utime.sleep(2.5)

STATE_START = 'start'
STATE_WAIT_LED = 'wait_led'
STATE_WAIT_REACTION = 'wait_reaction'
STATE_SCORE = 'score'

previous_state = STATE_SCORE
state = STATE_START
best_score = 9999
sleep_ms = 0
random_sleep_start_time = 0
reaction_timer_start_time = 0
user_reaction_time = 0
score_display_start_time = 0
def show_your_reaction_score_state():    
    global previous_state
    global state
    global best_score
    global sleep_ms
    global random_sleep_start_time
    global reaction_timer_start_time
    global user_reaction_time
    global score_display_start_time

    def on_start_click(pin):
        global state
        state = STATE_WAIT_LED    
        print(utime.ticks_ms(), f'on_start_click state = {state}, pin.value = {pin.value()}')

    def register_user_reaction(pin):
        global user_reaction_time
        global state
        user_reaction_time = utime.ticks_diff(utime.ticks_ms(), reaction_timer_start_time)
        state = STATE_SCORE

    while True:
        # utime.sleep_ms(500)
        # print(utime.ticks_ms(), f'while start. state = {state}, previous_state = {previous_state}')
        if state == STATE_START:
            
            if previous_state == STATE_START:
                continue
            previous_state = STATE_START
            print(utime.ticks_ms(), 'state == STATE_START')
            led.value(0)
            oled.fill(0)
            oled.text("press the button",0,10)
            oled.text("TO START!",25,25)
            oled.show()
            button.irq(trigger=Pin.IRQ_RISING, handler=on_start_click)            
        elif state == STATE_WAIT_LED:
            if previous_state != STATE_WAIT_LED:
                print(utime.ticks_ms(), 'state == STATE_WAIT_LED')
                previous_state = STATE_WAIT_LED
                oled.fill(0)
                oled.text("Wait For LED",15,30)
                oled.show()
        
                sleep_ms = urandom.uniform(1,5)*1000
                random_sleep_start_time = utime.ticks_ms()
                continue

            if utime.ticks_ms() - random_sleep_start_time >= sleep_ms:
                led.value(1)
                reaction_timer_start_time=utime.ticks_ms()
                state = STATE_WAIT_REACTION
        elif state == STATE_WAIT_REACTION and previous_state != STATE_WAIT_REACTION:
            print(utime.ticks_ms(), 'state == STATE_WAIT_REACTION')
            previous_state = STATE_WAIT_REACTION
            button.irq(trigger=Pin.IRQ_RISING, handler=register_user_reaction)
        elif state == STATE_SCORE:
            if previous_state != STATE_SCORE:
                print(utime.ticks_ms(), 'state == STATE_SCORE')
                previous_state = STATE_SCORE
                if user_reaction_time < best_score:
                    best_score = user_reaction_time

                led.value(0)
                oled.fill(0)
                oled.text("Your Time",25,25)
                oled.text(str(user_reaction_time),26,35)
                oled.text("best score",26,45)
                oled.text(str(best_score),26,55)
                oled.show()
                score_display_start_time = utime.ticks_ms()
                continue
            
            if utime.ticks_ms() - score_display_start_time >= 2000:
                state = STATE_START

class ShowYourReactionGame:
    led: Pin
    oled: SSD1306_I2C
    button: Pin

    STATE_START = "start"
    STATE_WAIT_LED = "wait_led"
    STATE_WAIT_REACTION = "wait_reaction"
    STATE_SCORE = "score"
    state = STATE_START
    best_score = 9999
    sleep_ms = 0
    random_sleep_start_time = 0
    user_reaction_time = 0
    reaction_timer_start_time = 0
    score_display_start_time = 0
    state_counter = -1
    state_handlers = None

    def __init__(self, led: Pin, oled: SSD1306_I2C, button: Pin) -> None:
        self.oled = oled
        self.led = led
        self.button = button

        self.state_handlers = {
            self.STATE_START:self.run_STATE_START,
            self.STATE_WAIT_LED:self.run_STATE_WAIT_LED,
            self.STATE_WAIT_REACTION:self.run_STATE_WAIT_REACTION,
            self.STATE_SCORE:self.run_STATE_SCORE
        }

    def set_state_to(self, what_state):
        self.state = what_state
        self.state_counter = -1

    def on_click_set_state_to_state_wait_led(self, pin):
        self.set_state_to(self.STATE_WAIT_LED)

    def on_click_set_state_to_state_score(self, pin):
        self.user_reaction_time = utime.ticks_ms() - self.reaction_timer_start_time
        self.led.value(0)
        self.set_state_to(self.STATE_SCORE)

    def run_STATE_START(self):
        if self.state_counter == 0:
            self.led.value(0)
            self.oled.fill(0)
            self.oled.text("press the button",0,10)
            self.oled.text("TO START!",25,25)
            self.oled.show()
            self.button.irq(trigger=Pin.IRQ_RISING, handler=self.on_click_set_state_to_state_wait_led) 

    def run_STATE_WAIT_LED(self):
        if self.state_counter == 0:
            self.oled.fill(0)
            self.oled.text("Wait For LED",15,30)
            self.oled.show()
            self.random_sleep_start_time = utime.ticks_ms()
            self.sleep_ms = urandom.uniform(1,5)*1000
                
        if utime.ticks_ms() - self.random_sleep_start_time >= self.sleep_ms:
            self.led.value(1)
            self.reaction_timer_start_time = utime.ticks_ms()
            self.set_state_to(self.STATE_WAIT_REACTION)

    def run_STATE_WAIT_REACTION(self):
        if self.state_counter == 0:
            self.button.irq(trigger=Pin.IRQ_RISING, handler=self.on_click_set_state_to_state_score)

    def run_STATE_SCORE(self):
        if self.state_counter == 0:
            if self.user_reaction_time < self.best_score:
                self.best_score = self.user_reaction_time

            self.led.value(0)
            self.oled.fill(0)
            self.oled.text("Your Time",25,25)
            self.oled.text(str(self.user_reaction_time),26,35)
            self.oled.text("best score",26,45)
            self.oled.text(str(self.best_score),26,55)
            self.oled.show()
            self.score_display_start_time = utime.ticks_ms()            
            
        if utime.ticks_ms() - self.score_display_start_time >= 2000:
            self.set_state_to(self.STATE_START)

    def run(self) -> None:
        while True:
            utime.sleep(0.01)
            self.state_counter += 1
            handler = self.state_handlers[self.state] # type: ignore
            handler()
    

# show_your_reaction()
# show_your_reaction_score()
# show_your_reaction_score_state()
show_your_reaction_obgect = ShowYourReactionGame(led,oled,button)
show_your_reaction_obgect.run()