# -*- coding: utf-8 -*-


# PyPlanets: Object-oriented refactoring of PyMeeus, a Python library implementing astronomical algorithms.
# Copyright (C) 2020  Martin Fünffinger
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.


from pyplanets.core.base import TOL
from pyplanets.planets.pluto import Pluto
from pyplanets.core.epoch import Epoch


# Pluto class

def test_pluto_geometric_heliocentric_position():
    """Tests the geometric_heliocentric_position() method of Pluto class"""

    epoch = Epoch(1992, 10, 13.0)
    lon, lat, r = Pluto(epoch).geometric_heliocentric_position()

    assert abs(round(lon.to_positive(), 5) - 232.74071) < TOL, \
        "ERROR: 1st geometric_heliocentric_position() test doesn't match"

    assert abs(round(lat, 5) - 14.58782) < TOL, \
        "ERROR: 2nd geometric_heliocentric_position() test doesn't match"

    assert abs(round(r, 6) - 29.711111) < TOL, \
        "ERROR: 3rd geometric_heliocentric_position() test doesn't match"


def test_pluto_geocentric_position():
    """Tests the geocentric_position() method of Pluto class"""

    epoch = Epoch(1992, 10, 13.0)
    ra, dec = Pluto(epoch).geocentric_position()

    assert ra.ra_str(n_dec=1) == "15h 31' 43.7''", \
        "ERROR: 1st geocentric_position() test doesn't match"

    assert dec.dms_str(n_dec=0) == "-4d 27' 29.0''", \
        "ERROR: 2nd geocentric_position() test doesn't match"
