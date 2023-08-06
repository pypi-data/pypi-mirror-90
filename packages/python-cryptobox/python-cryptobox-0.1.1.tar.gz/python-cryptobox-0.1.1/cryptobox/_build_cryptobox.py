#!/usr/env python

#  Copyright (c) 2021. Alexander Eisele <alexander@eiselecloud.de>
#
#  This program is free software: you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program.  If not, see <https://www.gnu.org/licenses/>.

from cffi import FFI
from subprocess import Popen, PIPE


ffi = FFI()

header_path = "/usr/include/cbox.h"

process = Popen(["gcc", "-E", header_path], stdout=PIPE)
stdout, stderr = process.communicate()
stdout = stdout.decode("utf-8")
ffi.cdef(stdout)

ffi.set_source("cryptobox._cbox",
               '#include "cbox.h"',
               libraries=["cryptobox"],
               )

if __name__ == "__main__":
    ffi.compile(verbose=True)
