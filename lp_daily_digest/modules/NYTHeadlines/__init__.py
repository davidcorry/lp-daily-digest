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
from flask import current_app as app
import requests

class NYTHeadlines(Module):
    def render(self):
        r = requests.get(
            'https://api.nytimes.com/svc/topstories/v2/home.json',
            params={'api-key': app.config['NYT_API_KEY']}
        )

        results = r.json()['results'][:5]
        headlines = self.simplify_results(results)

        return self.render_template('headlines.html', headlines=headlines)

    def simplify_results(self, results):
        import pyphen

        def hyphenate(text):
            return ' '.join([dict.inserted(word, "&shy;") for word in text.split()])

        headlines = []

        for result in results:
            dict = pyphen.Pyphen(lang='en_US')
            headline = {}
            headline['title'] = hyphenate(result['title'])
            headline['section'] = "%s %s" % (result['section'], result['subsection']) if result['subsection'] is not '' else result['section']
            headline['abstract'] = hyphenate(result['abstract'])
            headline['imageURL'] = result['multimedia'][-1]['url'] if len(result['multimedia']) > 0 else None
            headlines.append(headline)

        return headlines
