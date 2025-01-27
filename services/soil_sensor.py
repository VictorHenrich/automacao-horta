from machine import ADC, Pin
from core.patterns import BaseService, ServiceResponse
from core.exceptions import ServiceError
from core import config


class SoilSensorService(BaseService):
    def __init__(
        self,
        soil_sensor_analog_port=config.SOIL_SENSOR_PORT,
        water_pump_digital_port=config.WATER_PUMP_PORT,
    ):
        soil_pin = Pin(soil_sensor_analog_port, Pin.IN)

        self.__soil_sensor = ADC(soil_pin, atten=ADC.ATTN_11DB)

        self.__water_pump_pin = Pin(water_pump_digital_port, Pin.OUT)

    def __capture_sensor_value(self):
        try:
            return self.__soil_sensor.read()

        except Exception as error:
            raise ServiceError(self, "Falha ao realizar leitura do sensor!", error)

    def __activate_water_pump(self, sensor_value):
        try:
            activate_water_pump = self.__validate_soil_sensor_value(sensor_value)

            self.__water_pump_pin.value(activate_water_pump)

            return activate_water_pump

        except Exception as error:
            raise ServiceError(self, "Falha ao ativar bomba dagua!", error)

    def __validate_soil_sensor_value(self, sensor_value):
        return sensor_value >= config.MAX_VALUE_SOIL_SENSOR

    def execute(self):
        sensor_value = self.__capture_sensor_value()

        water_pump_activated = self.__activate_water_pump(sensor_value)

        return ServiceResponse(
            mqtt_topic=config.TOPIC_SENDING_SOIL_SENSOR_DATA,
            mqtt_data={
                "sensor_value": sensor_value,
                "water_pump_activated": water_pump_activated,
            },
            display_message=f"Valor do sensor de solo: {sensor_value}",
        )
