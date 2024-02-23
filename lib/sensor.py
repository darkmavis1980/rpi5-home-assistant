"""Sensor class module"""
import bme680
from smbus2 import SMBus
from bme280 import BME280

class Sensor:
    """Sensor class to handle both bme280 and bme680 sensors"""
    bme_sensor = None
    temperature = 0
    humidity = 0
    pressure = 0

    def __init__(self, sensor_type: str):
        self.sensor_type = sensor_type.lower()
        self.import_sensor_library()

    def get_sensor_reading(self):
        """Get the reading from the sensor"""
        if self.sensor_type == 'bme280':
            self.temperature = self.bme_sensor.get_temperature()
            self.pressure = self.bme_sensor.get_pressure()
            self.humidity = self.bme_sensor.get_humidity()

        if self.sensor_type == 'bme680':
            self.temperature = self.bme_sensor.data.temperature
            self.pressure = self.bme_sensor.data.pressure
            self.humidity = self.bme_sensor.data.humidity

    def import_sensor_library(self):
        """Initialize the appropriate library"""
        if self.sensor_type == 'bme280':
            # Initialise the BME280
            bus = SMBus(1)
            self.bme_sensor = BME280(i2c_dev=bus)

        if self.sensor_type == 'bme680':
            # Initialise the BME680
            try:
                self.bme_sensor = bme680.BME680(bme680.I2C_ADDR_PRIMARY)
            except (RuntimeError, IOError):
                self.bme_sensor = bme680.BME680(bme680.I2C_ADDR_SECONDARY)
            self.bme_sensor.set_humidity_oversample(bme680.OS_2X)
            self.bme_sensor.set_pressure_oversample(bme680.OS_4X)
            self.bme_sensor.set_temperature_oversample(bme680.OS_8X)
            self.bme_sensor.set_filter(bme680.FILTER_SIZE_3)
