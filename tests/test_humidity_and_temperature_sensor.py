from services.humidity_and_temperature_sensor import HumidityAndTemperatureSensorService
from utils import config


hum_and_temp_sensor_service = HumidityAndTemperatureSensorService(
    port=config.HUM_AND_TEMP_SENSOR_PORT
)

while True:
    hum_and_temp_sensor_service.execute()
