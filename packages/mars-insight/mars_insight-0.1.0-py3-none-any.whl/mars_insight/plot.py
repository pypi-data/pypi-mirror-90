"""Plotting."""
import numpy as np
import matplotlib.pyplot as plt


def plot_wind_rose(weather, normalise=False):
    """Plot Wind Rose."""

    if weather.wind_direction is None:
        raise ValueError('InsightWeather objects has no Wind Direction data.')

    values = [
        key for key in weather.wind_direction.keys() if key.isdigit()
    ]
    values.sort()

    radians = np.radians(
        [weather.wind_direction[val]['compass_degrees'] for val in values]
    )
    height = [weather.wind_direction[val]['ct'] for val in values]

    if normalise:
        height = height / np.max(height)

    # Choose minimum available resolution for plots.
    radian_diff = np.abs(radians[1:-1] - np.roll(radians, 1)[1:-1])
    width = np.min(radian_diff)

    fig = plt.figure()
    axes = fig.add_axes([0, 0, 1, 1], projection='polar')
    # Add 90 degrees to data when plotting to account for different
    # coordinate definitions.
    axes.bar(radians + 90, height, width=width, bottom=0.0)

    axes.set_xticklabels(['E', 'NE', 'N', 'NW', 'W', 'SW', 'S', 'SE'])

    title_str = f'Wind Distribution - Sol {weather.sol}\n'
    title_str += f'{weather.first_utc} - {weather.last_utc}'
    plt.title(title_str)

    return fig, axes
