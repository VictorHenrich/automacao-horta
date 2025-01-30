from core.patterns import BaseService, ServiceResponse
from core.exceptions import ServiceError
from core import config
from utils.pins import AnalogPin, PinTypes


class WaterSensorService(BaseService):
    def __init__(self, analog_port=config.WATER_SENSOR_PORT):
        self.__sensor = AnalogPin(analog_port, PinTypes.IN)

    def __capture_sensor_value(self):
        try:
            return self.__sensor.read()

        except Exception as error:
            raise ServiceError(self, "Falha ao realizar leitura do sensor!", error)

    def execute(self):
        sensor_value = self.__capture_sensor_value()

        return ServiceResponse(
            mqtt_topic=config.TOPIC_SENDING_WATER_SENSOR_DATA,
            mqtt_data={"sensor_value": sensor_value},
            display_message=f"Sensor Agua: {sensor_value}",
        )
