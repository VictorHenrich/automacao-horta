from dht import DHT11, DHT22
from machine import Pin


class DHTTypes:
    DHT11 = DHT11

    DHT22 = DHT22


class DHTSensor:
    def __init__(self, port, type=DHTTypes.DHT11):
        pin = Pin(port, Pin.IN)

        self.__sensor = type(pin)

    @property
    def sensor(self):
        return self.__sensor

    def measure(self):
        self.__sensor.measure()

        temperature = self.__sensor.temperature()

        humidity = self.__sensor.humidity()

        return {"temperature": temperature, "humidity": humidity}
