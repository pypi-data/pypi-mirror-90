# Copyright 2020 Andrzej Cichocki

# This file is part of Cowpox.
#
# Cowpox is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Cowpox is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Cowpox.  If not, see <http://www.gnu.org/licenses/>.

# This file incorporates work covered by the following copyright and
# permission notice:

# Copyright (c) 2010-2017 Kivy Team and other contributors
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.

from cowpox import JavaSrc
from cowpox.pyrecipe import CythonRecipe
from cowpox.util import Contrib
from diapyr import types

class PyjniusRecipe(CythonRecipe, JavaSrc):

    from .genericndkbuild import GenericNDKBuildRecipe
    from .sdl2 import LibSDL2Recipe
    name = 'pyjnius'
    version = '1.2.1'
    depends = ('genericndkbuild', 'sdl2'), 'six'

    @types(GenericNDKBuildRecipe, LibSDL2Recipe)
    def __init(self, genericndkbuild = None, sdl2 = None):
        self.genericndkbuild = genericndkbuild
        self.sdl2 = sdl2

    def mainbuild(self):
        self.preparedir(f"https://github.com/kivy/pyjnius/archive/{self.version}.zip")
        if self.sdl2 is not None:
            self.apply_patches('sdl2_jnienv_getter.patch')
        if self.genericndkbuild is not None:
            self.apply_patches('genericndkbuild_jnienv_getter.patch')
        self.install_python_package()

    def javasrc(self):
        return Contrib([self.recipebuilddir / 'jnius' / 'src'])
