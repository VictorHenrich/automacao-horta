from machine import Pin
from dht import DHT22
from utils.patterns import BaseService
from utils.mqtt import MQTTIntegration
from utils import config


class HumidityAndTemperatureSensorService(BaseService):
    def __init__(self, port, sensor_class=DHT22):
        self.__pin = Pin(port, Pin.IN)

        self.__sensor = sensor_class(self.__pin)

        self.__mqtt_client = MQTTIntegration()

    def __get_humidity_and_temperature(self):
        self.__sensor.measure()

        temperature = self.__sensor.temperature()

        humidity = self.__sensor.humidity()

        return humidity, temperature

    def __send_message_to_mqtt(self, humidity, temperature):
        data = {"humidity": humidity, "temperature": temperature}

        self.__mqtt_client.publish(config.TOPIC_SENDING_HUM_AND_TEMP_SENSOR_DATA, data)

    def execute(self):
        humidity, temperature = self.__get_humidity_and_temperature()

        self.__send_message_to_mqtt(humidity, temperature)
