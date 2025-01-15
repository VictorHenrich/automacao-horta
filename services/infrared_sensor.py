from machine import Pin, ADC
from utils.patterns import BaseService
from utils.mqtt import MQTTIntegration
from utils.exceptions import ServiceError
from utils import config


class InfraredSensorService(BaseService):
    def __init__(self, port=config.INFRARED_SENSOR_PORT):
        self.__pin = Pin(port, Pin.IN)

        self.__sensor = ADC(self.__pin)

        self.__mqtt_client = MQTTIntegration()

    def __capture_sensor_value(self):
        try:
            return self.__sensor.read()

        except Exception as error:
            raise ServiceError(self, "Falha ao realizar leitura do sensor!", error)

    def __send_message_to_mqtt(self, sensor_value):
        try:
            data = {"sensor_value": sensor_value}

            self.__mqtt_client.publish(config.TOPIC_SENDING_INFRARED_SENSOR_DATA, data)

        except Exception as error:
            raise ServiceError(self, "Falha ao enviar mensagem ao MQTT!", error)

    def execute(self):
        sensor_value = self.__capture_sensor_value()

        try:
            self.__send_message_to_mqtt(sensor_value)

        except ServiceError as error:
            print(str(error))
