from core.patterns import BaseService, ServiceResponse
from core.exceptions import ServiceError
from core import config
from utils.pins import AnalogPin, DigitalPin, PinTypes, AttenuityTypes


class LightLevels(dict):
    DEFAULT = "NORMAL"

    ABOVE = "ALTA"

    BELOW = "BAIXA"

    @classmethod
    def get_level(cls, sensor_value):
        if sensor_value >= config.MAX_VALUE_PHOTO_SENSOR:
            return cls.BELOW

        elif sensor_value <= config.MIN_VALUE_PHOTO_SENSOR:
            return cls.ABOVE

        else:
            return cls.DEFAULT


class PhotoresistorSensorService(BaseService):
    def __init__(
        self,
        analog_port=config.PHOTORESISTOR_SENSOR_PORT,
        light_led_digital_port=config.LIGHT_LED_PORT,
    ):
        self.__sensor = AnalogPin(analog_port, PinTypes.IN, AttenuityTypes.ATTN_11DB)

        self.__led = (
            DigitalPin(light_led_digital_port, PinTypes.OUT)
            if light_led_digital_port is not None
            else None
        )

    def __get_message(self, sensor_value, light_percentage, light_on):
        message = f"Luz: {light_percentage}\n"

        if self.__led is not None:
            message += f"Led: {'LIGADO' if light_on else 'DESLIGADO'}"

        else:
            level = LightLevels.get_level(sensor_value).upper()

            message += f"Nivel: {level}"

        return message

    def __turn_on_or_off_led(self, sensor_value):
        turn_on_light = LightLevels.get_level(sensor_value) == LightLevels.ABOVE

        if self.__led:
            self.__led.value(turn_on_light)

        return turn_on_light

    def __transform_value_into_light_percentage(self, sensor_value):
        voltage = sensor_value / 4095

        light_percentage = 100 - (voltage * 100)

        return f"{light_percentage:.2f}%"

    def __capture_sensor_value(self):
        try:
            return self.__sensor.read()

        except Exception as error:
            raise ServiceError(self, "Falha ao realizar leitura do sensor!", error)

    def execute(self):
        sensor_value = self.__capture_sensor_value()

        light_percentage = self.__transform_value_into_light_percentage(sensor_value)

        light_on = self.__turn_on_or_off_led(sensor_value)

        message = self.__get_message(sensor_value, light_percentage, light_on)

        return ServiceResponse(
            mqtt_topic=config.TOPIC_RECEIVING_INFRARED_SENSOR_DATA,
            mqtt_data={
                "sensor_value": sensor_value,
                "light_percentage": light_percentage,
                "light_on": light_on,
            },
            display_message=message,
        )
