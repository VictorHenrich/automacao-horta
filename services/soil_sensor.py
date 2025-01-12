from machine import ADC, Pin
from utils.patterns import BaseService
from utils import config
from utils.mqtt import MQTTIntegration


class SoilSensorService(BaseService):
    def __init__(self, soil_sensor_port, water_pump_port):
        self.__soil_pin = Pin(soil_sensor_port, Pin.IN)

        self.__soil_sensor = ADC(self.__soil_pin)

        self.__water_pump_pin = Pin(water_pump_port, Pin.OUT)

        self.__mqtt_client = MQTTIntegration()

    def __validate_soil_sensor_value(self, sensor_value):
        return sensor_value <= config.MIN_VALUE_SOIL_SENSOR

    def __send_message_to_mqtt(self, sensor_value, water_pump_activated):
        data = {
            "sensor_value": sensor_value,
            "water_pump_activated": water_pump_activated,
        }

        self.__mqtt_client.publish(config.TOPIC_SENDING_SOIL_SENSOR_DATA, data)

    def execute(self):
        sensor_value = self.__soil_sensor.read()

        activate_water_pump = self.__validate_soil_sensor_value(sensor_value)

        self.__water_pump_pin.value(activate_water_pump)

        self.__send_message_to_mqtt(sensor_value, activate_water_pump)
