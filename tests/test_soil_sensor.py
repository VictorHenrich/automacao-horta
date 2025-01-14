from services.soil_sensor import SoilSensorService
from utils import config


soil_sensor_service = SoilSensorService(
    soil_sensor_port=config.SOIL_SENSOR_PORT, water_pump_port=config.WATER_PUMP_PORT
)

while True:
    soil_sensor_service.execute()
