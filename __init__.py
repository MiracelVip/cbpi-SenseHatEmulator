# -*- coding: utf-8 -*-
from modules import cbpi
from modules.core.hardware import  SensorPassive
from modules import cbpi
from modules.core.props import Property

from sense_emu import SenseHat

@cbpi.sensor
class sense_emu(SensorPassive):
    type = Property.Select("TYPE", options=["humidity", "temperature"])

    def get_unit(self):
        '''
        :return: Unit of the sensor as string. Should not be longer than 3 characters
        '''

        if self.type == "humidity":
            return "%"
        if self.type == "temperature":
            return "°C" if self.get_config_parameter("unit", "C") == "C" else "°F"
                
    def read(self):
        
        self.api.app.logger.info("Sense HAT Emulator")
        sensor = SenseHat()
        try:
            humidity = 64 * sensor.humidity / 100
            temperature = sensor.temp
            self.api.app.logger.info(humidity)
            self.api.app.logger.info(temperature)
            
            
            if self.type == "humidity":
                self.data_received(round(humidity, 2))
            if self.type == "temperature":
                if self.get_config_parameter("unit", "C") == "C":
                    self.data_received(round(temperature, 2))
                else:
                    self.data_received(round((9.0 / 5.0 * temperature) + 32, 2))
        except Exception as e:
            self.api.app.logger.error("Sense Hat Emulator error")