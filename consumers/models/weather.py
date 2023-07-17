"""Contains functionality related to Weather"""
import json
import logging

logger = logging.getLogger(__name__)


class Weather:
    """Defines the Weather model"""

    def __init__(self):
        """Creates the weather model"""
        self.temperature = 70.0
        self.status = "sunny"

    def process_message(self, message):
        """Handles incoming weather data"""
        if message.topic() == "org.chicago.cta.weather.v1":
            json_data = json.loads(message.value())
            self.temperature = json_data.get("temperature")
            self.status = json_data.get("status")
