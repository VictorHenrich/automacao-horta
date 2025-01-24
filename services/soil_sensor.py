from machine import ADC, Pin
from utils.patterns import BaseService, ServiceResponse
from utils.exceptions import ServiceError
from utils import config


class SoilSensorService(BaseService):
    def __init__(
        self,
        soil_sensor_port=config.SOIL_SENSOR_PORT,
        water_pump_port=config.WATER_PUMP_PORT,
    ):
        self.__soil_pin = Pin(soil_sensor_port, Pin.IN)

        self.__soil_sensor = ADC(self.__soil_pin, atten=ADC.ATTN_11DB)

        self.__water_pump_pin = Pin(water_pump_port, Pin.OUT)

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

        print(f"Valor do sensor de solo: {sensor_value}")

        water_pump_activated = self.__activate_water_pump(sensor_value)

        return ServiceResponse(
            topic=config.TOPIC_SENDING_SOIL_SENSOR_DATA,
            data={
                "sensor_value": sensor_value,
                "water_pump_activated": water_pump_activated,
            },
        )
