from machine import Pin, ADC
from utils.patterns import BaseService



class InfraredSensorService(BaseService):
    def __init__(self, port):
        self.__pin = Pin(port, Pin.IN)

        self.__sensor = ADC(self.__pin)

    @property
    def pin(self):
        return self.__pin
    
    @property
    def sensor(self):
        return self.__sensor

    def execute(self):
        pass