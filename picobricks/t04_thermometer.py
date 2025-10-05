from machine import Pin, I2C
from picobricks import SSD1306_I2C, SHTC3 
import utime 

WIDTH=128
HEIGHT=64

i2c = I2C(0, scl=Pin(5), sda=Pin(4))   
oled = SSD1306_I2C(WIDTH, HEIGHT, i2c)
shtc_sensor = SHTC3(i2c)

while True:
	oled.fill(0)	
	temperature = shtc_sensor.temperature()
	humidity = shtc_sensor.humidity()
	oled.text("Temperature: ",15,10)
	oled.text(str(int(temperature)),55,25)
	oled.text("Humidity: ", 30,40)
	oled.text(str(int(humidity)),55,55)
	oled.show()
	utime.sleep(3.0)

	
                 