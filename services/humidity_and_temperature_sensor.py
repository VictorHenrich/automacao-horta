from core.patterns import BaseService, ServiceResponse
from core.exceptions import ServiceError
from core import config
from utils.dht import DHTSensor, DHTTypes


class HumidityAndTemperatureSensorService(BaseService):
    def __init__(
        self, port=config.HUM_AND_TEMP_SENSOR_PORT, sensor_type=DHTTypes.DHT11
    ):
        self.__sensor = DHTSensor(port, sensor_type)

    def __get_humidity_and_temperature(self):
        try:
            sensor_data = self.__sensor.measure()

            temperature = sensor_data["temperature"]

            humidity = sensor_data["humidity"]

            return f"{humidity}%", f"{temperature}C°"

        except Exception as error:
            raise ServiceError(
                self, "Falha ao realizar captura de umidade e temperatura!", error
            )

    def execute(self):
        humidity, temperature = self.__get_humidity_and_temperature()

        return ServiceResponse(
            mqtt_topic=config.TOPIC_SENDING_HUM_AND_TEMP_SENSOR_DATA,
            mqtt_data={"humidity": humidity, "temperature": temperature},
            display_message=f"Hum.: {humidity}\nTemp.: {temperature}",
        )
