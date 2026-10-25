# lp-daily-digest
# Copyright (C) 2019-2026 David Corry
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

from lp_daily_digest.modules import Module
from flask import current_app as app
from datetime import datetime
from memoization import cached
import requests

# WMO weather code -> (icon base, summary).
# Icon names match the sprite classes in open_meteo.html.
# Codes: https://open-meteo.com/en/docs
WEATHER_CODES = {
    0: ('clear', 'Clear skies'),
    1: ('partly-cloudy', 'Mainly clear'),
    2: ('partly-cloudy', 'Partly cloudy'),
    3: ('cloudy', 'Overcast'),
    45: ('fog', 'Fog'),
    48: ('fog', 'Rime fog'),
    51: ('rain', 'Light drizzle'),
    53: ('rain', 'Drizzle'),
    55: ('rain', 'Dense drizzle'),
    56: ('sleet', 'Freezing drizzle'),
    57: ('sleet', 'Heavy freezing drizzle'),
    61: ('rain', 'Light rain'),
    63: ('rain', 'Rain'),
    65: ('rain', 'Heavy rain'),
    66: ('sleet', 'Freezing rain'),
    67: ('sleet', 'Heavy freezing rain'),
    71: ('snow', 'Light snow'),
    73: ('snow', 'Snow'),
    75: ('snow', 'Heavy snow'),
    77: ('snow', 'Snow grains'),
    80: ('rain', 'Light rain showers'),
    81: ('rain', 'Rain showers'),
    82: ('rain', 'Violent rain showers'),
    85: ('snow', 'Light snow showers'),
    86: ('snow', 'Snow showers'),
    95: ('rain', 'Thunderstorm'),
    96: ('rain', 'Thunderstorm with hail'),
    99: ('rain', 'Severe thunderstorm'),
}

PRECIP_LABELS = {'snow': 'Snow', 'sleet': 'Sleet'}


class OpenMeteoForecast(Module):
    # Hours of day shown in the hourly strip.
    HOURS = (9, 12, 15, 18, 21)

    @cached(ttl=3600)
    def get_weather(self):
        r = requests.get(
            'https://api.open-meteo.com/v1/forecast',
            params={
                'latitude': app.config['OPEN_METEO_LATITUDE'],
                'longitude': app.config['OPEN_METEO_LONGITUDE'],
                'daily': 'temperature_2m_max,temperature_2m_min,weather_code,'
                         'precipitation_sum,precipitation_probability_max,sunrise,sunset',
                'hourly': 'temperature_2m,uv_index,weather_code',
                'temperature_unit': 'fahrenheit',
                'precipitation_units': 'inch',
                'forecast_days': 1,
                'timezone': 'auto',
            },
            timeout=10,
        )
        r.raise_for_status()
        daily, hourly = r.json()['daily'], r.json()['hourly']

        sunrise = datetime.fromisoformat(daily['sunrise'][0])
        sunset = datetime.fromisoformat(daily['sunset'][0])
        base, summary = WEATHER_CODES.get(daily['weather_code'][0], ('cloudy', 'Unknown conditions'))

        today = {
            'icon': self._icon(base, daytime=True),
            'summary': summary,
            'temperature_min': daily['temperature_2m_min'][0],
            'temperature_max': daily['temperature_2m_max'][0],
            'precipitation': daily['precipitation_sum'][0] or 0,
            'precip_probability': daily['precipitation_probability_max'][0],
            'precip_label': PRECIP_LABELS.get(base, 'Rain'),
            'sunrise': sunrise,
            'sunset': sunset,
        }

        # hourly[i] is hour i in the location's local time (timezone=auto),
        # so picking by index selects that local hour.
        hourly_slots = []
        for i in self.HOURS:
            t = datetime.fromisoformat(hourly['time'][i])
            base, _ = WEATHER_CODES.get(hourly['weather_code'][i], ('cloudy', ''))
            hourly_slots.append({
                'time': t,
                'icon': self._icon(base, daytime=sunrise <= t < sunset),
                'temperature': hourly['temperature_2m'][i],
                'uv_index': hourly['uv_index'][i],
            })

        return today, hourly_slots

    @staticmethod
    def _icon(base, daytime):
        if base in ('clear', 'partly-cloudy'):
            return '%s-%s' % (base, 'day' if daytime else 'night')
        return base

    def render(self):
        today, hourly = self.get_weather()
        return self.render_template('open_meteo.html', today=today, hourly=hourly)

    def get_filters(self):
        # Shortcut that shows just the hour and am/pm - e.g. 9AM.
        def hour_format(dt):
            return '%d<span class="weatherampm">%s</span>' % (
                dt.hour % 12 or 12, 'AM' if dt.hour < 12 else 'PM')

        # Hour, minutes and am/pm - e.g. 7:27AM.
        def time_format(dt):
            return '%d:%s<span class="weatherampm">%s</span>' % (
                dt.hour % 12 or 12, dt.strftime('%M'), 'AM' if dt.hour < 12 else 'PM')

        return {
            'hour_format': hour_format,
            'time_format': time_format,
        }