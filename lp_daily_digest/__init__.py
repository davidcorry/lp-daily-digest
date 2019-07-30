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

from flask import Flask, render_template, jsonify
from lp_daily_digest.config import Config
import datetime
import requests

app = Flask(__name__)
app.config.from_object(Config)

@app.route('/')
def index():
    return 'Hello.'

# A preview of the HTML output that gets sent to the Little Printer.
@app.route('/preview/')
def preview():
    return render_template(
        'output.html',
        preview=True,
        date=datetime.datetime.now(),
        from_name=from_name
    )

# Output the JSON that you would send to the Sirius server.
@app.route('/json/')
def json():
    return jsonify(html=render_template('output.html'))

# Print!
@app.route('/print/')
def send_print():
    r = requests.post(
        "%s?from=%s" % (app.config['PRINT_KEY'], app.config['FROM_NAME']),
        json={"html": render_template('output.html')}
    )
    return jsonify(r.json())
