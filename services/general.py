from utils.patterns import BaseService
from utils import config
from services.infrared_sensor import InfraredSensorService
from services.water_sensor import WaterSensorService


class GeneralService(BaseService):
    def __init__(self):
        self.__infrared_sensor_service = InfraredSensorService(config.INFRARED_SENSOR_PORT)

        self.__water_sensor_service = WaterSensorService(config.INFRARED_SENSOR_PORT)

    def execute(self):
        pass