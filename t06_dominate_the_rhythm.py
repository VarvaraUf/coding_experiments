from machine import Pin, PWM, ADC, I2C
from picobricks import SSD1306_I2C
import utime

WIDTH=128
HEIGHT=64

i2c = I2C(0, sda=Pin(4), scl=Pin(5))
oled = SSD1306_I2C(WIDTH, HEIGHT, i2c)
button = Pin(10, Pin.IN, Pin.PULL_DOWN)
pot = ADC(Pin(26))
buzzer = PWM(Pin(20))

is_routine_enabled = False
rhythm_speed = 0

tones = {
    "A3": 220,
    "D4": 294,
    "E4": 330,
    "F4": 349
}

melody = [("A3", 1), ("E4", 0.5), ("E4",0.5), ("E4",0.5),("E4",0.5), ("E4",0.5), ("E4",0.5), ("F4",0.5), ("E4",0.5), ("D4",0.5), ("F4",0.5), ("E4",1)]
# for item in melod0y:
#     note = item[0]
#     time = item[1]
#     print('note = ', note, "time = ", time)
# for note, time in melody:
#     print('note = ', note, "time = ", time)

def playtone(frequency):
    buzzer.duty_u16(6000)
    buzzer.freq(frequency)

def enable_buzzer(pin):
    global is_routine_enabled
    is_routine_enabled = not is_routine_enabled

def play_the_song():
    global button_clicked
    button.irq(trigger=Pin.IRQ_RISING, handler=enable_buzzer)

    note_count = 0
    note_play_start_time = 0
    while True:
        current_time = utime.ticks_ms()
        oled.show()
        oled.text("Press the button",0,0)
    
        if is_routine_enabled:
            oled.fill(0)
            oled.text("Dominate ", 30, 10)
            oled.text("the ", 45, 25)
            oled.text("Rhythm ", 35, 40)
            rhythm_speed=((pot.read_u16()/65535.0)*20) + 1 # range from 1 to 20
            if (current_time - note_play_start_time)/1000.0 >= melody[note_count][1]/rhythm_speed:
                note_play_start_time = utime.ticks_ms()
            # print("note_count = ", note_count
            #       , "mysong[note_count] = ", mysong[note_count]
            #       , "tones[mysong[note_count]]", tones[mysong[note_count]])
                playtone(tones[melody[note_count][0]])
                note_count += 1
                if note_count == len(melody):
                    note_count = 0                

        if is_routine_enabled == False:
            buzzer.duty_u16(0)
            
play_the_song()
        
        
        