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

import os, sys

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

class Module():
    # Init and set the template_dir relative to the actual module's folder.
    def __init__(self):
        self.template_dir = os.path.join(
            os.path.dirname(
                sys.modules[self.__class__.__module__].__file__
            ), 'templates'
        )

    def render_template(self, file, **kwargs):
        import jinja2

        with open(os.path.join(self.template_dir, file)) as f:
            template = f.read()

        env = jinja2.Environment()
        env.filters['black_and_white'] = black_and_white
        template = env.from_string(template)
        return template.render(**kwargs)

    def render():
        raise NotImplementedError
