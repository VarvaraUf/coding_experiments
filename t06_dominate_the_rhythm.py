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
    "F4": 349,
    "beep": 200
}

melody = [("A3", 1), ("E4", 0.5), ("E4",0.5), ("E4",0.5),("E4",0.5), ("E4",0.5), ("E4",0.5), ("F4",0.5), ("E4",0.5), ("D4",0.5), ("F4",0.5), ("E4",1)]
beep_melody = [("M8", 5.0)]
# for item in melod0y:
#     note = item[0]
#     time = item[1]
#     print('note = ', note, "time = ", time)
# for note, time in melody:
#     print('note = ', note, "time = ", time)

def map_range_value(value, min, max, min_new, max_new):
    size = max - min
    #print("size",size)
    #print("value",value)
    position = (value - min) / size
    #print(utime.ticks_ms(),"position",position)
    size_new = max_new - min_new
    #print(utime.ticks_ms(),"size_new",size_new)
    v_new = (size_new * position) + min_new
    #print(utime.ticks_ms(),"v_new",v_new)
    return v_new

def map_u16_value(v, min, max):
    return map_range_value(v, 0, 65535, min, max)

def play_the_song():

    def playtone(frequency):
        buzzer.duty_u16(6000)
        buzzer.freq(frequency)
    
    def enable_buzzer(pin):
        global is_routine_enabled
        is_routine_enabled = not is_routine_enabled
    
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

def detect_button_events():
    LONG_PRESS_TIME = 1000
    events = []
    
    def record_button_event(pin: Pin):
        events.append({"state": pin.value(), "time": utime.ticks_ms()})
    
    button.irq(trigger=Pin.IRQ_RISING | Pin.IRQ_FALLING, handler=record_button_event)
    # 0        {'state': 1, 'time': 13216968} m 
    # 1        {'state': 1, 'time': 13216968}
    # 2        {'state': 1, 'time': 13216981}
    # 3        {'state': 0, 'time': 13217160} m
    # 4        {'state': 0, 'time': 13217165} +
    while True:
        utime.sleep_ms(500)
        
        # print("events")
        # for index, event in enumerate(events):
        #     print(index, '\t', event)
        
        if len(events) > 0:
            merged_events = []
            for event in events:
                if len(merged_events) > 0 and merged_events[-1]['state'] == event['state']:
                    continue
                
                merged_events.append(event)
            
            # print("merged_events")
            # for index, event in enumerate(merged_events):
            #     print(index, '\t', event)

            event = merged_events[-1]
            # long press
            if event["state"] == 1 and (utime.ticks_ms() - event["time"]) >= LONG_PRESS_TIME:
                print("long press")
                events = []
            # click
            elif event["state"] == 0 and len(merged_events) >= 2:
                previous_event = merged_events[-2]
                if previous_event["state"] == 1:
                    print("click")                                   
                    events = []    
                 
def beep_on_button_event():
    LONG_PRESS_TIME = 1000
    events = []
    time = 0
    time_when_click_happened = 0
    def record_button_event(pin: Pin):
        events.append({"state": pin.value(), "time": utime.ticks_ms()})
    
    button.irq(trigger=Pin.IRQ_RISING | Pin.IRQ_FALLING, handler=record_button_event)

    while True:
        utime.sleep_ms(100)
        # print("events")
        # for index, event in enumerate(events):
        #     print(index, '\t', event)
        
        if len(events) > 0:
            merged_events = []
            for event in events:
                if len(merged_events) > 0 and merged_events[-1]['state'] == event['state']:
                    continue
                
                merged_events.append(event)
            
            # print("merged_events")
            # for index, event in enumerate(merged_events):
            #     print(index, '\t', event)

            event = merged_events[-1]
            # long press
            if event["state"] == 1 and (utime.ticks_ms() - event["time"]) >= LONG_PRESS_TIME:
                print("long press")
                events = []
                time_when_click_happened = utime.ticks_ms()
                time = 200
            # click
            elif event["state"] == 0 and len(merged_events) >= 2:
                previous_event = merged_events[-2]
                if previous_event["state"] == 1:
                    print("click") 
                    time = 100 
                    time_when_click_happened = utime.ticks_ms()
                    events = []
                    
        # print("utime.ticks_ms()",utime.ticks_ms(),"time_when_click_happened",time_when_click_happened,"time pased",utime.ticks_ms() - time_when_click_happened)
        if (utime.ticks_ms() - time_when_click_happened) < time:
            buzzer.duty_u16(6000)
            buzzer.freq(349)
            # print("turn buzzer on time pased",utime.ticks_ms() - time_when_click_happened)
        else:
            # print("turn buzzer off time pased",utime.ticks_ms() - time_when_click_happened)
            buzzer.duty_u16(0)
            # buzzer.duty_u16(6000)
            # buzzer.freq(349)
               

                               
                    

def control_buzzer():
    LONG_PRESS_TIME = 1000
    events = []
    is_routine_enabled = False
    
    def record_button_event(pin: Pin):
        events.append({"state": pin.value(), "time": utime.ticks_ms()})
    
    button.irq(trigger=Pin.IRQ_RISING | Pin.IRQ_FALLING, handler=record_button_event)
    # 0        {'state': 1, 'time': 13216968} m 
    # 1        {'state': 1, 'time': 13216968}
    # 2        {'state': 1, 'time': 13216981}
    # 3        {'state': 0, 'time': 13217160} m
    # 4        {'state': 0, 'time': 13217165} +
    while True:
        # utime.sleep_ms(500)
        frequency = map_u16_value(pot.read_u16(),200,4000)

        if is_routine_enabled == True:
                playtone(int(frequency))
        
        # print("events")
        oled.fill(0)
        oled.text("frequency", 30, 10)
        oled.text(str(int(frequency)), 45, 25)
        oled.show()
        for index, event in enumerate(events):
            print(index, '\t', event)
        
        if len(events) > 0:
            merged_events = []
            for event in events:
                if len(merged_events) > 0 and merged_events[-1]['state'] == event['state']:
                    continue
                
                merged_events.append(event)
            
            # print("merged_events")
            for index, event in enumerate(merged_events):
                print(index, '\t', event)

            event = merged_events[-1]
            # long press
            if event["state"] == 1 and (utime.ticks_ms() - event["time"]) >= LONG_PRESS_TIME:
                print("long press")
                play_the_beep_song()
                events = []
            # click
            elif event["state"] == 0 and len(merged_events) >= 2:
                previous_event = merged_events[-2]
                if previous_event["state"] == 1:
                    print("click") 
                    play_the_beep_song()
                    is_routine_enabled = not is_routine_enabled
                                   
                    events = []  
             

            
            
# play_the_song()
beep_on_button_event()
# detect_button_events()
