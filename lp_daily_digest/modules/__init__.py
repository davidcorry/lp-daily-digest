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
        template = env.from_string(template)
        return template.render(**kwargs)

    def render():
        raise NotImplementedError