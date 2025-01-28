from machine import Pin, ADC
from core.patterns import BaseService, ServiceResponse
from core.exceptions import ServiceError
from core import config


class TemperatureSensorService(BaseService):
    def __init__(self, analog_port=config.TEMPERATURE_SENSOR_PORT):
        pin = Pin(analog_port, Pin.IN)

        self.__sensor = ADC(pin, atten=ADC.ATTN_11DB)

    def __capture_sensor_value(self):
        try:
            return self.__sensor.read()

        except Exception as error:
            raise ServiceError(self, "Falha ao realizar leitura do sensor!", error)

    def __transform_value_into_temperature(self, sensor_value):
        voltage = (sensor_value / 4095) * 3.3

        temperature = voltage * 100

        return f"{temperature:.2f}ºC"

    def execute(self):
        sensor_value = self.__capture_sensor_value()

        temperature = self.__transform_value_into_temperature(sensor_value)

        return ServiceResponse(
            mqtt_topic=config.TOPIC_SENDING_INFRARED_SENSOR_DATA,
            mqtt_data={"sensor_value": sensor_value, "temperature": temperature},
            display_message=f"Temperatura: {temperature}",
        )
