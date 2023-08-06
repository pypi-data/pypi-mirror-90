"""Insight Models."""
import json


# Set of allowed units for Insight measurements
UNITS = {
    'Temperature': 'F',
    'Pressure': 'Pa',
    'Wind Speed': 'm/s',
    'Wind Direction': 'degrees',
}


class InsightWeather():  # pylint: disable=R0902,R0903
    """Weather Object."""

    def __init__(self, sol, data):
        """Initialise."""
        self.sol = sol
        self.data = data

        if 'AT' in data:
            self.temperature = InsightMeasurement(data['AT'], 'Temperature')
        else:
            self.temperature = None

        if 'HWS' in data:
            self.wind_speed = InsightMeasurement(data['HWS'], 'Wind Speed')
        else:
            self.wind_speed = None

        if 'PRE' in data:
            self.pressure = InsightMeasurement(data['PRE'], 'Pressure')
        else:
            self.pressure = None

        if 'WD' in data:
            self.wind_direction = data['WD']
        else:
            self.wind_direction = None

        self.season = data['Season']
        self.first_utc = data['First_UTC']
        self.last_utc = data['Last_UTC']

    def __repr__(self):
        """Representation."""
        return f'Sol: {self.sol}'

    @classmethod
    def from_json(cls, file_path):
        """Load json."""
        with open(file_path, 'r') as json_fp:
            data = json.load(json_fp)
        return cls(data['sol'], data['data'])

    def to_json(self, file_path):
        """Save json."""
        with open(file_path, 'w') as json_fp:
            json.dump({'sol': self.sol, 'data': self.data}, json_fp)


class InsightMeasurement():
    """Measurement Object."""

    def __init__(self, data, weather_type):
        self._min = data['mn']
        self._max = data['mx']
        self._avg = data['av']
        self._num_measurements = data['ct']
        self._weather_type = weather_type
        self._unit = UNITS[weather_type]

    def __repr__(self):
        """Representation."""
        return f'{self._weather_type}: {self._avg} {self._unit}'

    @property
    def unit(self):
        """Unit."""
        return self._unit

    @property
    def max(self):
        """Maximum measurement."""
        return self._max

    @property
    def min(self):
        """Minimum measurement."""
        return self._min

    @property
    def avg(self):
        """Average measurement."""
        return self._avg

    @property
    def num_measurements(self):
        """Number of measurements."""
        return self._num_measurements

    @property
    def weather_type(self):
        """Type of weather measurement."""
        return self._weather_type
