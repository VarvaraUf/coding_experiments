from machine import Pin, I2C
from picobricks import MotorDriver, SHTC3

def smart_cooler():
    LIMIT_TEMPERATURE = 20 #define the limit temperature

    i2c = I2C(0, scl=Pin(5), sda=Pin(4))   # Init I2C using pins
    motor = MotorDriver(i2c)
    shtc_sensor = SHTC3(i2c)

    motor.dc(2,0,0)

    while True:
        temp = shtc_sensor.temperature()
        print(temp)
        if temp >= LIMIT_TEMPERATURE:    #operate if the room temperature is higher than the limit temperature 
            motor.dc(2,125,0)
        else:
            motor.dc(2,0,0)

class SmartCooler:
    LIMIT_TEMPERATURE = 28
    i2c = I2C(0, scl=Pin(5), sda=Pin(4))

    def __init__(self):
        self.motor = MotorDriver(self.i2c)
        self.shtc_sensor = SHTC3(self.i2c)

    def run(self):
        self.motor.dc(2,0,0)

        while True:
            temp = self.shtc_sensor.temperature()
            print(temp)
            if temp >= self.LIMIT_TEMPERATURE:    #operate if the room temperature is higher than the limit temperature 
                self.motor.dc(2,125,1)
            else:
                self.motor.dc(2,0,0)

smart_cooler_object = SmartCooler()
smart_cooler_object.run()

        

