"""Mars Insight API Client."""
import requests

from .models import InsightWeather


__all__ = ['Client']

URL = 'https://api.nasa.gov/insight_weather/'
FEEDTYPE = 'json'
VER = '1.0'


class Client():
    """Client."""

    def __init__(self, api_key: str):
        """Initalise."""
        self._api_key = api_key

    def get_data(self):
        """GET data."""
        req = requests.get(
            URL,
            params={
                'api_key': self._api_key,
                'feedtype': FEEDTYPE,
                'ver': VER,
            },
        )

        req.raise_for_status()

        data = req.json()
        return data

    def get_recent_weather(self):
        """GET data for most recent Sol in a InsightWeather object."""
        data = self.get_data()
        most_recent_sol = max(data['sol_keys'])
        weather = InsightWeather(most_recent_sol, data[most_recent_sol])
        return weather

    def get_weather(self):
        """GET data for all Sols in an array of InsightWeather objects."""
        data = self.get_data()
        weather = []
        for sol in data['sol_keys']:
            sol_weather = InsightWeather(sol, data[sol])
            weather.append(sol_weather)
        return weather
