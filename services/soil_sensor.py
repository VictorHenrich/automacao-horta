from core.patterns import BaseService, ServiceResponse
from core.exceptions import ServiceError
from core import config
from utils.pins import AnalogPin, DigitalPin, PinTypes, AttenuityTypes


class WaterLevels(dict):
    DEFAULT = "NORMAL"

    ABOVE = "ALTO"

    BELOW = "BAIXO"

    @classmethod
    def get_level(cls, sensor_value):
        if sensor_value >= config.MAX_VALUE_SOIL_SENSOR:
            return cls.BELOW

        elif sensor_value <= config.MIN_VALUE_SOIL_SENSOR:
            return cls.ABOVE

        else:
            return cls.DEFAULT


class SoilSensorService(BaseService):
    def __init__(
        self,
        soil_sensor_analog_port=config.SOIL_SENSOR_PORT,
        water_pump_digital_port=config.WATER_PUMP_PORT,
    ):

        self.__soil_sensor = AnalogPin(
            soil_sensor_analog_port, PinTypes.IN, AttenuityTypes.ATTN_11DB
        )

        self.__water_pump_pin = (
            DigitalPin(water_pump_digital_port, PinTypes.OUT)
            if water_pump_digital_port is not None
            else None
        )

    def __capture_sensor_value(self):
        try:
            return self.__soil_sensor.read()

        except Exception as error:
            raise ServiceError(self, "Falha ao realizar leitura do sensor!", error)

    def __get_message(self, sensor_value, water_percentage, water_pump_activated):
        message = f"Agua S.: {water_percentage}\n"

        if self.__water_pump_pin is not None:
            message += f"Bomba: {'LIGADA' if water_pump_activated else 'DESLIGADA'}"

        else:
            level = WaterLevels.get_level(sensor_value).upper()

            message += f"Nivel: {level}"

        return message

    def __activate_water_pump(self, sensor_value):
        if self.__water_pump_pin is None:
            return False

        try:
            activate_water_pump = (
                WaterLevels.get_level(sensor_value) == WaterLevels.ABOVE
            )

            self.__water_pump_pin.value(activate_water_pump)

            return activate_water_pump

        except Exception as error:
            raise ServiceError(self, "Falha ao ativar bomba dagua!", error)

    def __transform_value_into_water_percentage(self, sensor_value):
        voltage = sensor_value / 4095

        water_percentage = 100 - (voltage * 100)

        return f"{water_percentage:.2f}%"

    def execute(self):
        sensor_value = self.__capture_sensor_value()

        water_pump_activated = self.__activate_water_pump(sensor_value)

        water_percentage = self.__transform_value_into_water_percentage(sensor_value)

        message = self.__get_message(
            sensor_value, water_percentage, water_pump_activated
        )

        return ServiceResponse(
            mqtt_topic=config.TOPIC_SENDING_SOIL_SENSOR_DATA,
            mqtt_data={
                "sensor_value": sensor_value,
                "water_pump_activated": water_pump_activated,
                "water_percentage": water_percentage,
            },
            display_message=message,
        )
