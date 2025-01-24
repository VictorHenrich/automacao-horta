from machine import Pin, ADC
from utils.patterns import BaseService, ServiceResponse
from utils.exceptions import ServiceError
from utils import config


class PhotoresistorSensorService(BaseService):
    def __init__(self, port=config.PHOTORESISTOR_SENSOR_PORT):
        self.__pin = Pin(port, Pin.IN)

        self.__sensor = ADC(self.__pin)

    def __capture_sensor_value(self):
        try:
            return self.__sensor.read()

        except Exception as error:
            raise ServiceError(self, "Falha ao realizar leitura do sensor!", error)

    def execute(self):
        sensor_value = self.__capture_sensor_value()

        print(f"Valor sensor Photoresistor: {sensor_value}")

        return ServiceResponse(
            topic=config.TOPIC_RECEIVING_INFRARED_SENSOR_DATA,
            data={"sensor_value": sensor_value},
        )
