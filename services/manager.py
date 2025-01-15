import _thread as thread
from utils.patterns import BaseService
from utils import config
from utils.exceptions import ServiceError
from utils.net import Network


class ServiceManager(BaseService):
    def __init__(self, *services):
        self.__services = list(services)

    def __perform_service(self, service):
        while True:
            service.execute()

    def add_service(self, service):
        self.__services.append(service)

    def execute(self):
        Network.connect_to_wifi(config.WIFI_NAME, config.WIFI_PASSWORD)

        for service in self.__services:
            thread.start_new_thread(self.__perform_service, (service,))

        while True:
            continue
