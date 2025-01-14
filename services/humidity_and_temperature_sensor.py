from machine import Pin
from dht import DHT22
from utils.patterns import BaseService
from utils.mqtt import MQTTIntegration
from utils.exceptions import ServiceError
from utils import config


class HumidityAndTemperatureSensorService(BaseService):
    def __init__(self, port, sensor_class=DHT22):
        self.__pin = Pin(port, Pin.IN)

        self.__sensor = sensor_class(self.__pin)

        self.__mqtt_client = MQTTIntegration()

    def __get_humidity_and_temperature(self):
        try:
            self.__sensor.measure()

            temperature = self.__sensor.temperature()

            humidity = self.__sensor.humidity()

            return humidity, temperature

        except Exception as error:
            raise ServiceError(
                self, "Falha ao realizar captura de umidade e temperatura!", error
            )

    def __send_message_to_mqtt(self, humidity, temperature):
        try:
            data = {"humidity": humidity, "temperature": temperature}

            self.__mqtt_client.publish(
                config.TOPIC_SENDING_HUM_AND_TEMP_SENSOR_DATA, data
            )

        except Exception as error:
            raise ServiceError(self, "Falha ao enviar mensagem ao cliente MQTT!", error)

    def execute(self):
        humidity, temperature = self.__get_humidity_and_temperature()

        try:
            self.__send_message_to_mqtt(humidity, temperature)

        except ServiceError as error:
            print(str(error))
