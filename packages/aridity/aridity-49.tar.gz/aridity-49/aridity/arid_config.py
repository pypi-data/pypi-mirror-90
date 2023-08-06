# Copyright 2017, 2020 Andrzej Cichocki

# This file is part of aridity.
#
# aridity is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# aridity is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with aridity.  If not, see <http://www.gnu.org/licenses/>.

from .context import Context
from .model import Entry
import os, sys

def _configpath(configname):
    if os.sep in configname:
        return configname
    for parent in os.environ['PATH'].split(os.pathsep):
        path = os.path.join(parent, configname)
        if os.path.exists(path):
            return path
    raise Exception("Not found: %s" % configname)

def main_arid_config():
    context = Context()
    context.source(Entry([]), _configpath(sys.argv[1]))
    sys.stdout.write(context.resolved(*sys.argv[2:]).tobash(True))
