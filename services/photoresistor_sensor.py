from core.patterns import BaseService, ServiceResponse
from core.exceptions import ServiceError
from core import config
from utils.pins import AnalogPin, DigitalPin, PinTypes


class PhotoresistorSensorService(BaseService):
    def __init__(
        self,
        analog_port=config.PHOTORESISTOR_SENSOR_PORT,
        light_led_digital_port=config.LIGHT_LED_PORT,
    ):
        self.__sensor = AnalogPin(analog_port, PinTypes.IN)

        self.__led = DigitalPin(light_led_digital_port, PinTypes.OUT)

    def __turn_on_or_off_led(self, sensor_value):
        turn_on_light = sensor_value >= config.MAX_VALUE_PHOTO_SENSOR

        self.__led.value(1 if turn_on_light else 0)

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

        return ServiceResponse(
            mqtt_topic=config.TOPIC_RECEIVING_INFRARED_SENSOR_DATA,
            mqtt_data={
                "sensor_value": sensor_value,
                "light_percentage": light_percentage,
                "light_on": light_on,
            },
            display_message=f"Luz: {light_percentage}\nLed: {'LIGADO' if light_on else 'DESLIGADO'}",
        )
