import _thread as thread
from services.infrared_sensor import InfraredSensorService
from services.water_sensor import WaterSensorService
from services.soil_sensor import SoilSensorService
from services.humidity_and_temperature_sensor import HumidityAndTemperatureSensorService
from utils.patterns import BaseService
from utils import config
from utils.exceptions import ServiceError
from utils.net import Network


class GeneralGardenService(BaseService):
    def __init__(self):
        self.__infrared_sensor_service = InfraredSensorService(
            config.INFRARED_SENSOR_PORT
        )

        self.__water_sensor_service = WaterSensorService(config.INFRARED_SENSOR_PORT)

        self.__soil_sensor_service = SoilSensorService(
            config.SOIL_SENSOR_PORT, config.WATER_PUMP_PORT
        )

        self.__hum_and_temp_service = HumidityAndTemperatureSensorService(
            config.HUM_AND_TEMP_SENSOR_PORT
        )

    def __connect_to_wifi(self):
        try:
            Network.connect_to_wifi(config.WIFI_NAME, config.WIFI_PASSWORD)

        except Exception as error:
            raise ServiceError(self, "Falha ao se conectar ao wifi!", error)

    def __perform_service(self, service):
        while True:
            service.execute()

    def execute(self):
        self.__connect_to_wifi()

        services = [
            self.__infrared_sensor_service,
            self.__water_sensor_service,
            self.__soil_sensor_service,
            self.__hum_and_temp_service,
        ]

        [
            thread.start_new_thread(self.__perform_service, (service,))
            for service in services
        ]

        while True:
            continue
