from machine import Pin#to acces the hardware picobricks
import utime
led = Pin(7,Pin.OUT)#initialize digital pin as an output for led
push_button = Pin(10,Pin.IN,Pin.PULL_DOWN)#initialize digital pin 10 as an input

def turn_led_on_when_button_on():
    led.value(push_button.value())

def turn_led_on_when_button_off():
    led.value(not push_button.value())
    
previous_button_state = 0
current_button_state = 0
def toggle_led_on_button_click():
    global previous_button_state
    global current_button_state
    
    current_button_state = push_button.value()
    if current_button_state == 0 and previous_button_state == 1:
        print("click")
        led.value(not led.value())
        
    previous_button_state = push_button.value()

is_led_enabled = False
previous_ticks_ms = 0
def blink_led_on_button_click():
    global is_led_enabled
    global previous_ticks_ms
    global previous_button_state
    global current_button_state
    
    current_button_state = push_button.value()
    if current_button_state == 0 and previous_button_state == 1:
        print("click")
        is_led_enabled = not is_led_enabled
        led.value(0)
        
    previous_button_state = push_button.value()
    
    print("utime.ticks_ms() - previous_ticks_ms",utime.ticks_ms() - previous_ticks_ms)
    print("is_led_enabled=",is_led_enabled)
    if (utime.ticks_ms() - previous_ticks_ms) >= 500 and is_led_enabled:
        print(utime.ticks_ms(), 'toggle')
        led.value(not led.value())
        
        previous_ticks_ms = utime.ticks_ms()

pattern = [0.5, 0.1, 0.1, 0.1]
n = 0
def blink_pattern_twice_blocking():
    global n
    
    if n == 4:
         n = 0
    
    led.value(n%2)
    utime.sleep(pattern[n])    
    n += 1

#previous_ticks_ms = utime.ticks_ms()
pattern_ms = [500, 100, 100, 100]   
def blink_pattern_twice():
    global n
    global previous_ticks_ms
    
    if n == 4:
        n = 0
       
    if (utime.ticks_ms() - previous_ticks_ms) >= pattern_ms[n]:
        n += 1
        led.value(n%2)
        previous_ticks_ms = utime.ticks_ms()
        
def blink_pattern_twice_on_button_click():
    global n
    global previous_ticks_ms
    global previous_button_state
    global current_button_state
    global is_led_enabled
    
    current_button_state = push_button.value()
    if current_button_state == 0 and previous_button_state == 1:
        print("click")
        is_led_enabled = not is_led_enabled
        led.value(0)
        
    if n == 4:
        n = 0
    
    previous_button_state = push_button.value()
    if (utime.ticks_ms() - previous_ticks_ms) >= pattern_ms[n] and is_led_enabled:
        n += 1
        led.value(n%2)
        previous_ticks_ms = utime.ticks_ms()
 
click_count = 0

def print_double_click_on_double_click():
    global previous_button_state
    global click_count
    global previous_ticks_ms
    
    
    if push_button.value() == 0 and previous_button_state == 1:
        click_count += 1
        
        if click_count == 1:
            previous_ticks_ms = utime.ticks_ms()
            
        if click_count == 2:
            if (utime.ticks_ms() - previous_ticks_ms) <= 500:
                print("double click")
                click_count = 0                
            else:
                click_count = 1
                previous_ticks_ms = utime.ticks_ms()

    previous_button_state = push_button.value()
    
n = 0
last_time_led_was_changed = 0 
pattern_time = []
click_series_begin_time = 0
def blinck_as_many_times_as_button_clicked():
    global previous_button_state
    global click_count
    global click_series_begin_time
    global pattern_time
    global n
    global last_time_led_was_changed
    global item_duration
    
    #print(utime.ticks_ms(),click_count,"previous time")
    if push_button.value() == 0 and previous_button_state == 1:
        click_count += 1
        print(utime.ticks_ms(), "click count", click_count)
        
        if click_count == 1:
            click_series_begin_time = utime.ticks_ms()
            print(utime.ticks_ms(), "click_series_begin_time")
                
    if click_count != 0 and (utime.ticks_ms() - click_series_begin_time) >= 1000:
        print(utime.ticks_ms(),"clicks in 1000ms", click_count)
        pattern_items = (click_count*2) - 1
        item_duration = 500/pattern_items
        pattern_time = [500]
        for a in range(pattern_items):
            pattern_time.append(item_duration)
        print(utime.ticks_ms(), "pattern_time", pattern_time)
        click_count = 0
        n = 0
        led.value(0)
        last_time_led_was_changed = utime.ticks_ms()            
            
    if len(pattern_time) != 0 and (utime.ticks_ms() - last_time_led_was_changed) >= pattern_time[n]:
        if n == len(pattern_time) - 1:
            n = 0
        else:
            n += 1
        print(utime.ticks_ms(),"toggle led", n%2, "delay ", utime.ticks_ms() - last_time_led_was_changed)
        last_time_led_was_changed = utime.ticks_ms()
        led.value(n%2)                

    previous_button_state = push_button.value()

long_press_in_progres = False
long_press_count = 0
def button_long_press():
    global previous_button_state
    global previous_ticks_ms
    global long_press_in_progres
    global long_press_count
    
    if push_button.value() == 1 and previous_button_state == 0:
        previous_ticks_ms = utime.ticks_ms()
        long_press_in_progres = True
        print("in if statement")

    
    if long_press_in_progres and push_button.value() == 1 and previous_button_state == 1 and (utime.ticks_ms() - previous_ticks_ms) >= 1000:
        long_press_count += 1
        print("long press",long_press_count,utime.ticks_ms() - previous_ticks_ms)
        long_press_in_progres = False
    previous_button_state = push_button.value()
    
    
functions_list_names = ["button_long_press", "blinck_as_many_times_as_button_clicked", "print_double_click_on_double_click", "blink_pattern_twice_on_button_click", "blink_pattern_twice", "blink_pattern_twice_blocking", "blink_led_on_button_click(), toggle_led_on_button_click", "turn_led_on_when_button_off", "turn_led_on_when_button_on"]
n = 0
def loop_for_functions():
    global previous_button_state
    global previous_ticks_ms
    global long_press_in_progres
    global functions_list_names
    global n
    global long_press_count
    
    if n == len(functions_list_names):
        n = 0
    
    if push_button.value() == 1 and previous_button_state == 0:
        previous_ticks_ms = utime.ticks_ms()
        long_press_in_progres = True
        print("in if statement")
    
    if long_press_in_progres and push_button.value() == 1 and previous_button_state == 1 and (utime.ticks_ms() - previous_ticks_ms) >= 1000:
        long_press_count += 1
        print("long press",long_press_count,utime.ticks_ms() - previous_ticks_ms, functions_list_names[n])
        n += 1
        long_press_in_progres = False
    previous_button_state = push_button.value()
    
while True:#while loop
    utime.sleep(0.1)
    #turn_led_on_when_button_on()_1
    #turn_led_on_when_button_off()_2
    #toggle_led_on_button_click()_3
    #blink_led_on_button_click()_4
    #blink_pattern_twice_blocking()_5
    #blink_pattern_twice()_6
    #blink_pattern_twice_on_button_click()
    #print_double_click_on_double_click()
    #blinck_as_many_times_as_button_clicked()
    button_long_press()
    #loop_for_functions()
    
    