from machine import Pin, I2C, ADC, PWM
from picobricks import SSD1306_I2C, WS2812
import utime
led = Pin(7,Pin.OUT)

WIDTH  = 128                                            
HEIGHT = 64

sda=Pin(4)
scl=Pin(5)
#initialize digital pin 4 and 5 as an OUTPUT for OLED Communication

i2c=I2C(0,sda=sda, scl=scl)
neo = WS2812(pin_num=6, num_leds=1, brightness=0.05)#initialize digital pin 6 as an OUTPUT for NeoPixel

oled = SSD1306_I2C(WIDTH, HEIGHT, i2c)
ldr = ADC(Pin(27))#initialize digital pin 6 as an OUTPUT for NeoPixel
button = Pin(10,Pin.IN,Pin.PULL_DOWN)#initialize digital pin 10 as an INPUT for button
buzzer = PWM(Pin(20, Pin.OUT))#initialize digital pin 20 as an OUTPUT for buzzer
buzzer.freq(1000)

RED = (255, 0, 0)
WHITE = (255, 255, 255)
#RGB black and white color code
def alarm_clock():
    oled.fill(0)
    oled.show()

    neo.pixels_fill(RED)
    neo.pixels_show()
    led.value(0)

    if ldr.read_u16()<4000:
        wakeup = True
    else:
        wakeup = False
        
    while True:
        while wakeup==False:
            oled.fill(0)
            oled.text("Good night",25,32)
            oled.show()
            #Show on OLED and print "Good night"
            utime.sleep(1)
            if ldr.read_u16()<4000:
                while button.value()==0:
                    oled.fill(0)
                    
                    oled.text("Good morning",15,32)
                    oled.show()
                    #Print the minutes, seconds, milliseconds and "Goog morning" values ​​to the X and Y coordinates determined on the OLED screen.
                    neo.pixels_fill(WHITE)
                    neo.pixels_show()
                    buzzer.duty_u16(6000)
                    led.value(1)
                    utime.sleep(1)
                    
                    #wait for one second
                    buzzer.duty_u16(0)
                    
                    utime.sleep(0.5)
                    
                    #wait for half second
                    wakeup=True
                neo.pixels_fill(RED)
                neo.pixels_show()
                led.value(0)
        oled.fill(0)
        oled.text("Have a nice day!",0,32)
        #Print the minutes, seconds, milliseconds and "Have a nice day!" values ​​to the X and Y coordinates determined on the OLED screen.
        oled.show()
        if ldr.read_u16()>40000:
            wakeup= False
            
        utime.sleep(1.0)

STATE_NIGHT = "NIGHT"
STATE_ALARM = "ALARM"
STATE_DAY = "DAY"
state = STATE_NIGHT
buzzer_state_change_time = 0
is_buzzer_on = False
def alarm_clock_state():
    global state
    global buzzer_state_change_time
    global is_buzzer_on

    def on_click_change_state_to_day(pin):
        global state
        state = STATE_DAY

    while True:
        # print(utime.ticks_ms(),"state4",state)
        if state == STATE_NIGHT:
            if ldr.read_u16()>4000:
                oled.fill(0)
                oled.text("Good night",25,32)
                oled.show()
                neo.pixels_fill(RED)
                neo.pixels_show()
            else:
                state = STATE_ALARM

        if state == STATE_ALARM:
            neo.pixels_fill((255,255,255))
            neo.pixels_show()

            oled.fill(0)
            oled.text("Good morning",25,32)
            oled.show()

            if utime.ticks_ms() - buzzer_state_change_time >= (1000 if is_buzzer_on else 500):
                is_buzzer_on = not is_buzzer_on
                buzzer_state_change_time = utime.ticks_ms()
                buzzer.duty_u16(6000 if is_buzzer_on else 0)

            button.irq(trigger=Pin.IRQ_RISING, handler=on_click_change_state_to_day)

        if state == STATE_DAY:
            buzzer.duty_u16(0)
            if ldr.read_u16()<4000:
                oled.fill(0)
                oled.text("Have a nice day!",0,32)
                oled.show()
                neo.pixels_fill((0,0,0))
                neo.pixels_show()
                print(utime.ticks_ms(),"state8",state)
            else:
                state = STATE_NIGHT





    

   
#wait for one second
# alarm_clock()
alarm_clock_state()