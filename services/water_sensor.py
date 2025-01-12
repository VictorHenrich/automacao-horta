from machine import Pin, ADC
from utils.patterns import BaseService
from utils.mqtt import MQTTIntegration
from utils import config


class WaterSensorService(BaseService):
    def __init__(self, port):
        self.__pin = Pin(port, Pin.IN)

        self.__sensor = ADC(self.__pin)

        self.__mqtt_client = MQTTIntegration()

    def execute(self):
        sensor_value = self.__sensor.read()

        data = {"sensor_value": sensor_value}

        self.__mqtt_client.publish(config.TOPIC_SENDING_WATER_SENSOR_DATA, data)
