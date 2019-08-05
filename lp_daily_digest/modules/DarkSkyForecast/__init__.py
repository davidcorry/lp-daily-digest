# lp-daily-digest
# Copyright (C) 2019 David Corry
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
from pydarksky.darksky import DarkSky
from flask import current_app as app
from datetime import datetime
from memoization import cached

class DarkSkyForecast(Module):
    @cached(ttl=3600)
    def get_weather(self):
        darksky = DarkSky(app.config['DARK_SKY_API_KEY'])

        # Set the info we want (or, rather, exclude it and invert the exclusion)
        darksky.exclude = ['currently', 'daily', 'hourly']
        darksky.exclude_invert()

        # Get weather.
        weather = darksky.weather(
            latitude=app.config['DARK_SKY_LATITUDE'],
            longitude=app.config['DARK_SKY_LONGITUDE'],
            date=datetime.now()
        )

        # Send Jinja the info that matters.
        today = weather.daily[0]
        hourly = [
            weather.hourly[9],
            weather.hourly[12],
            weather.hourly[15],
            weather.hourly[18],
            weather.hourly[21]
        ]

        return today, hourly

    def render(self):
        today, hourly = self.get_weather()
        return self.render_template('darksky.html', today=today, hourly=hourly)

    def get_filters(self):
        # Takes an int and returns a strftime-formatted time.
        def strftime(timestamp, format):
            from datetime import datetime
            return datetime.fromtimestamp(timestamp).strftime(format)

        # Shortcut that shows just the hour and am/pm - e.g. 9AM.
        def hour_format(timestamp):
            return strftime(timestamp, '%-I<span class="darkskyampm">%p</span>')

        # There were instances where precipType raised an exception, so this is for safety
        def has_precipitation(day):
            try:
                return day.precipType
            except:
                return False

        return {
            'strftime': strftime,
            'hour_format': hour_format,
            'has_precipitation': has_precipitation
        }