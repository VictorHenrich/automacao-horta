from machine import Pin, ADC
from utils.patterns import BaseService, ServiceResponse
from utils.exceptions import ServiceError
from utils import config


class WaterSensorService(BaseService):
    def __init__(self, analog_port=config.WATER_SENSOR_PORT):
        self.__pin = Pin(analog_port, Pin.IN)

        self.__sensor = ADC(self.__pin)

    def __capture_sensor_value(self):
        try:
            return self.__sensor.read()

        except Exception as error:
            raise ServiceError(self, "Falha ao realizar leitura do sensor!", error)

    def execute(self):
        sensor_value = self.__capture_sensor_value()

        return ServiceResponse(
            mqtt_topic=config.TOPIC_SENDING_WATER_SENSOR_DATA,
            mqtt_data={"sensor_value": sensor_value},
            display_message=f"Valor sensor da agua: {sensor_value}",
        )
