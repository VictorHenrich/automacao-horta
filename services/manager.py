import _thread as thread
import time
from services.lcd_display import LCDDisplayService
from utils.patterns import BaseService
from utils.exceptions import ServiceError
from utils.mqtt import MQTTIntegration
from utils import config
from utils.net import Network


class ServiceManager(BaseService):
    def __init__(
        self,
        *services,
        send_to_mqtt=True,
        execution_time=None,
        show_message_in_console=True,
        show_message_in_display=True,
    ):
        self.__services = list(services)

        self.__mqtt_client = MQTTIntegration()

        self.__params = {
            "send_to_mqtt": send_to_mqtt,
            "execution_time": execution_time,
            "show_message_in_console": show_message_in_console,
            "show_message_in_display": show_message_in_display,
        }

        self.__lock = thread.allocate_lock()

        self.__messages = []

    def __perform_service(self, service):
        while True:
            response = service.execute()

            exec_time = float(self.__params["execution_time"] or 0)

            if response:
                if self.__params["send_to_mqtt"] is True:
                    self.__send_message_to_mqtt(response.mqtt_topic, response.mqtt_data)

                if self.__params["show_message_in_console"] is True:
                    print(f"{response.display_message}\n")

                if (
                    self.__params["show_message_in_display"] is True
                    and response.display_message is not None
                ):
                    with self.__lock:
                        self.__messages.append(response.display_message)

            time.sleep(exec_time)

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
            if self.__params["show_message_in_display"] is True:
                lcd_display_service = LCDDisplayService()

                message = "\n".join(self.__messages)

                lcd_display_service.set_message(message).execute()

                self.__messages = []
