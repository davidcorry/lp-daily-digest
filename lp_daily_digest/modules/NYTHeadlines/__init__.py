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
from memoization import cached
import requests

class NYTHeadlines(Module):
    @cached(ttl=3600)
    def get_headlines(self):
        r = requests.get(
            'https://api.nytimes.com/svc/topstories/v2/home.json',
            params={'api-key': app.config['NYT_API_KEY']}
        )

        results = r.json()['results'][:5]
        return self.simplify_results(results)

    def render(self):
        headlines = self.get_headlines()
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

    def get_filters(self):
        @cached(max_size=10)
        def black_and_white(url, width=384):
            from PIL import Image, ImageEnhance, ImageStat
            import math
            import requests
            from io import BytesIO
            import base64

            # Download the image
            response = requests.get(url)
            img = Image.open(BytesIO(response.content))

            # Resize
            img.thumbnail((width, 1000))

            # Drop the contrast of the image a bit.
            img = ImageEnhance.Contrast(img).enhance(0.95)

            # Get the preceived brightness of the image so we can adjust accordingly.
            # Perceived brightness algorithm from https://alienryderflex.com/hsp.html
            stat = ImageStat.Stat(img)
            r,g,b = stat.mean
            brightness = math.sqrt(0.299*(r**2) + 0.587*(g**2) + 0.114*(b**2))

            # Adjust brightness accordingly. I'm not really sure if this is a reasonable
            # way to adjust brightness, so it'll be a bit of trial and error. This just
            # pushes the overall percieved brightness closer to 128ish.
            factor = 1/(brightness/256)/2
            img = ImageEnhance.Brightness(img).enhance(factor)

            # Convert to black and white.
            img = img.convert('1')

            # Convert the image to base64 text
            img_buffer = BytesIO()
            img.save(img_buffer, format='PNG')
            img_base64 = base64.b64encode(img_buffer.getvalue())

            return 'data:image/png;base64,%s' % img_base64.decode('utf-8')

        return {'black_and_white': black_and_white}
