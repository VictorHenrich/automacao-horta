from machine import Pin
from dht import DHT11
from utils.patterns import BaseService, ServiceResponse
from utils.exceptions import ServiceError
from utils import config


class HumidityAndTemperatureSensorService(BaseService):
    def __init__(self, port=config.HUM_AND_TEMP_SENSOR_PORT, sensor_class=DHT11):
        self.__pin = Pin(port, Pin.IN)

        self.__sensor = sensor_class(self.__pin)

    def __get_humidity_and_temperature(self):
        try:
            self.__sensor.measure()

            temperature = self.__sensor.temperature()

            humidity = self.__sensor.humidity()

            return humidity, temperature

        except Exception as error:
            raise ServiceError(
                self, "Falha ao realizar captura de umidade e temperatura!", error
            )

    def execute(self):
        humidity, temperature = self.__get_humidity_and_temperature()

        print(f"Humidade: {humidity}%\nTemperatura: {temperature}C°")

        return ServiceResponse(
            topic=config.TOPIC_SENDING_HUM_AND_TEMP_SENSOR_DATA,
            data={"humidity": humidity, "temperature": temperature},
        )
