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

from flask import Flask, render_template, jsonify, request, flash, redirect, url_for
from lp_daily_digest.config import Config
from lp_daily_digest.modules.NYTHeadlines import NYTHeadlines
from lp_daily_digest.modules.DarkSkyForecast import DarkSkyForecast
from lp_daily_digest.modules.Amazing import Amazing
import datetime
import requests
from apscheduler.schedulers.background import BackgroundScheduler

scheduler = BackgroundScheduler()
scheduler.start()

app = Flask(__name__)
app.config.from_object(Config)

modules = [
    DarkSkyForecast(),
    NYTHeadlines(),
    Amazing()
]

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
        modules=modules,
        from_name=app.config['FROM_NAME']
    )

# Output the JSON that you would send to the Sirius server.
@app.route('/json/')
def json():
    return jsonify(html=render_template('output.html', modules=modules))

def submit_print():
    try: app
    except:
        app = Flask(__name__)
        app.config.from_object(Config)

    with app.app_context():
        r = requests.post(
            "%s?from=%s" % (app.config['PRINT_KEY'], app.config['FROM_NAME']),
            json={"html": render_template('output.html', modules=modules)}
        )
    return r

# Print!
@app.route('/print/', methods=['GET', 'POST'])
def lp_print():
    if request.method == 'POST':
        if request.form['preview'] == 'true':
            r = submit_print()
            status = r.json()['status']
            if status == 'sent':
                flash('Printed.')
            else:
                flash('Submitted a print, but got this response: %s' % status)
            return redirect(url_for('preview'))
        return jsonify(r.json())
    else:
        return render_template('print.html')

if app.config['ENV'] == 'production':
    scheduler.add_job(submit_print, trigger='cron', hour='9', minute='30')
