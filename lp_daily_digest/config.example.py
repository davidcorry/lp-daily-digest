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

class Config(object):
    APPLICATION_ROOT = '' # If your instance is running in a subdirectory, add it here. (e.g. '/lp-daily-digest')
    SECRET_KEY = '' # This is Flask's secret key to create sessions. For advice on how to create one, see:
                    # https://flask.palletsprojects.com/en/1.1.x/quickstart/#sessions
    PRINT_KEY = 'https://device.li/abcdefg' # Replace this with your own Print Key.
    FROM_NAME = 'Daily Digest' # The name that goes at the header.
    NYT_API_KEY = 'abcdefg' # Replace this with your own NYT API key.
    DARK_SKY_API_KEY = 'abcdefg' # Replace this with your own Dark Sky API key.
    DARK_SKY_LATITUDE = 0.0 # Latitude of the location you want to pull weather data for.
    DARK_SKY_LONGITUDE = 0.0 # Longitude of the location you want to pull weather data for.
