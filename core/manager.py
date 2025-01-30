import _thread as thread
import time
from core.patterns import BaseService
from core.exceptions import ServiceError
from utils.mqtt import MQTTIntegration
from utils.net import Network
from utils.lcd import LCDDisplay


class ServiceManager(BaseService):
    def __init__(
        self,
        *services,
        send_to_mqtt=True,
        connect_to_wifi=True,
        show_message_in_console=True,
        show_message_in_display=True,
        service_execution_time=None,
        display_execution_time=None,
    ):
        self.__services = list(services)

        self.__mqtt_client = MQTTIntegration()

        self.__params = {
            "service_execution_time": float(service_execution_time or 0),
            "display_execution_time": float(display_execution_time or 1),
            "send_to_mqtt": bool(send_to_mqtt),
            "show_message_in_console": bool(show_message_in_console),
            "show_message_in_display": bool(show_message_in_display),
            "connect_to_wifi": bool(connect_to_wifi),
        }

        self.__lock = thread.allocate_lock()

        self.__messages = []

    def __add_message_in_display(self, response):
        with self.__lock:
            self.__messages.append(response.display_message)

    def __perform_service(self, service):
        while True:
            response = service.execute()

            service_execution_time = self.__params["service_execution_time"]

            if response:
                if self.__params["send_to_mqtt"] is True:
                    self.__send_message_to_mqtt(response.mqtt_topic, response.mqtt_data)

                if self.__params["show_message_in_console"] is True:
                    print(f"{response.display_message}\n")

                if (
                    self.__params["show_message_in_display"] is True
                    and response.display_message is not None
                ):
                    self.__add_message_in_display(response)

            if service_execution_time:
                time.sleep(service_execution_time)

    def __send_message_to_mqtt(self, topic, data):
        try:
            self.__mqtt_client.publish(topic, data)

        except Exception as error:
            raise ServiceError(self, "Falha ao enviar mensagem ao MQTT!", error)

    def add_service(self, service):
        self.__services.append(service)

    def execute(self):
        if self.__params["connect_to_wifi"] is True:
            Network.connect_to_wifi()

        for service in self.__services:
            thread.start_new_thread(self.__perform_service, (service,))

        lcd_display = (
            LCDDisplay() if self.__params["show_message_in_display"] is True else None
        )

        while True:
            if lcd_display and len(self.__messages) >= len(self.__services):
                with self.__lock:
                    for message in self.__messages:
                        lcd_display.print_message(message)

                        time.sleep(self.__params["display_execution_time"])

                    self.__messages = []
