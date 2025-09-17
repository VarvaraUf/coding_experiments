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

red = "red"
yellow = "yellow"
green = "green"
color = red
previous_color = green
loops = 0
is_routine_enabled = True
changed_color_time = 0
def red_light_green_light():
    global previous_color
    global color
    global loops
    global is_routine_enabled
    global changed_color_time

    led.value(0)

    def change_to_yellow(pin):
        global color
        color = yellow
        is_routine_enabled = False
        changed_color_time = utime.ticks_ms()

    def change_to_green(pin):
        global color
        color = green
        is_routine_enabled = False
        changed_color_time = utime.ticks_ms()
        

    def change_to_red(pin):
        global color
        color = red
        is_routine_enabled = False
        changed_color_time = utime.ticks_ms()

    while True:
        if color == red and previous_color != red:
            if is_routine_enabled == True:
                neo.pixels_fill((255,0,0))
                previous_color = red
                loops += 1
                led.value(1)
                oled.fill(0)
                oled.text(str(color) + str(loops),57,32)
                #Print the minutes, seconds, milliseconds and "Have a nice day!" values ​​to the X and Y coordinates determined on the OLED screen.
                oled.show()
                neo.pixels_show() 
                print("red")
                button.irq(trigger=Pin.IRQ_RISING, handler=change_to_yellow)

        if color == yellow and previous_color == red:
            if is_routine_enabled == True:
                neo.pixels_fill((255,255,0))
                previous_color = yellow
                oled.fill(0)
                oled.text(str(color) + str(loops),57,32)
                #Print the minutes, seconds, milliseconds and "Have a nice day!" values ​​to the X and Y coordinates determined on the OLED screen.
                oled.show()
                neo.pixels_show() 
                print("yelow")
                button.irq(trigger=Pin.IRQ_RISING, handler=change_to_green)
               
        if color == green and previous_color == yellow:
            if is_routine_enabled == True:
                neo.pixels_fill((0,255,0))
                previous_color = green
                oled.fill(0)
                oled.text(str(color) + str(loops),57,32)
                #Print the minutes, seconds, milliseconds and "Have a nice day!" values ​​to the X and Y coordinates determined on the OLED screen.
                oled.show()
                neo.pixels_show()
                print("green")
                button.irq(trigger=Pin.IRQ_RISING, handler=change_to_red)
            
        if (utime.ticks_ms() - changed_color_time) >= 500:
            is_routine_enabled = True

   
#wait for one second
# alarm_clock()
red_light_green_light()