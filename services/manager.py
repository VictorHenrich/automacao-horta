import _thread as thread
import time
from utils.patterns import BaseService
from utils.exceptions import ServiceError
from utils.mqtt import MQTTIntegration
from utils import config
from utils.net import Network


class ServiceManager(BaseService):
    def __init__(self, *services, send_to_mqtt=True, execution_time=None):
        self.__services = list(services)

        self.__mqtt_client = MQTTIntegration()

        self.__params = {"send_to_mqtt": send_to_mqtt, "execution_time": execution_time}

    def __perform_service(self, service):
        while True:
            response = service.execute()

            if not response:
                continue

            if self.__params["send_to_mqtt"] is True:
                self.__send_message_to_mqtt(response.topic, response.data)

            if isinstance(self.__params["execution_time"], (float, int)):
                time.sleep(self.__params["execution_time"])

    def __send_message_to_mqtt(self, topic, data):
        try:
            self.__mqtt_client.publish(topic, data)

        except Exception as error:
            raise ServiceError(self, "Falha ao enviar mensagem ao MQTT!", error)

    def add_service(self, service):
        self.__services.append(service)

    def execute(self):
        Network.connect_to_wifi(config.WIFI_NAME, config.WIFI_PASSWORD)

        for service in self.__services:
            thread.start_new_thread(self.__perform_service, (service,))

        while True:
            continue
