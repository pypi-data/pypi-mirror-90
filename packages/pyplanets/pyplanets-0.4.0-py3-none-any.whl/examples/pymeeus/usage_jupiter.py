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


from pyplanets.core.epoch import Epoch
from pyplanets.core.constellation import Constellation
from pyplanets.planets.earth import Earth

from pyplanets.planets.jupiter import Jupiter


def main():
    # Let's define a small helper function
    def print_me(msg, val):
        print("{}: {}".format(msg, val))

    # Let's show some uses of Jupiter class
    print("\n" + 35 * "*")
    print("*** Use of Jupiter class")
    print(35 * "*" + "\n")

    # Let's now compute the heliocentric position for a given epoch
    epoch = Epoch(2018, 10, 27.0)
    lon, lat, r = Jupiter(epoch).geometric_heliocentric_position()
    print_me("Geometric Heliocentric Longitude", lon.to_positive())
    print_me("Geometric Heliocentric Latitude", lat)
    print_me("Radius vector", r)

    print("")

    # Compute the geocentric position for 1992/12/20:
    epoch = Epoch(1992, 12, 20.0)
    constellation = Constellation(Earth(epoch), Jupiter(epoch))
    ra, dec, elon = constellation.geocentric_position()
    print_me("Right ascension", ra.ra_str(n_dec=1))
    print_me("Declination", dec.dms_str(n_dec=1))
    print_me("Elongation", elon.dms_str(n_dec=1))

    print("")

    # Print mean orbital elements for Jupiter at 2065.6.24
    epoch = Epoch(2065, 6, 24.0)
    l, a, e, i, ome, arg = Jupiter(epoch).orbital_elements_mean_equinox()
    print_me("Mean longitude of the planet", round(l, 6))       # 222.433723
    print_me("Semimajor axis of the orbit (UA)", round(a, 8))   # 5.20260333
    print_me("Eccentricity of the orbit", round(e, 7))          # 0.0486046
    print_me("Inclination on plane of the ecliptic", round(i, 6))   # 1.29967
    print_me("Longitude of the ascending node", round(ome, 5))  # 101.13309
    print_me("Argument of the perihelion", round(arg, 6))       # -85.745532

    print("")

    # Compute the time of the conjunction close to 1993/10/1
    epoch = Epoch(1993, 10, 1.0)
    conj = Jupiter(epoch).conjunction()
    y, m, d = conj.get_date()
    d = round(d, 4)
    date = "{}/{}/{}".format(y, m, d)
    print_me("Conjunction date", date)

    # Compute the time of the opposition close to -6/9/1
    epoch = Epoch(-6, 9, 1.0)
    oppo = Jupiter(epoch).opposition()
    y, m, d = oppo.get_date()
    d = round(d, 4)
    date = "{}/{}/{}".format(y, m, d)
    print_me("Opposition date", date)

    print("")

    # Compute the time of the station in longitude #1 close to 2018/11/1
    epoch = Epoch(2018, 11, 1.0)
    sta1 = Jupiter(epoch).station_longitude_1()
    y, m, d = sta1.get_date()
    d = round(d, 4)
    date = "{}/{}/{}".format(y, m, d)
    print_me("Date of station in longitude #1", date)

    # Compute the time of the station in longitude #2 close to 2018/11/1
    epoch = Epoch(2018, 11, 1.0)
    sta2 = Jupiter(epoch).station_longitude_2()
    y, m, d = sta2.get_date()
    d = round(d, 4)
    date = "{}/{}/{}".format(y, m, d)
    print_me("Date of station in longitude #2", date)

    print("")

    # Find the epoch of the Aphelion closer to 1981/6/1
    epoch = Epoch(1981, 6, 1.0)
    e = Jupiter(epoch).aphelion()
    y, m, d, h, mi, s = e.get_full_date()
    peri = str(y) + '/' + str(m) + '/' + str(d) + ' at ' + str(h) + ' hours'
    print_me("The Aphelion closest to 1981/6/1 will happen on", peri)

    print("")

    # Compute the time of passage through an ascending node
    epoch = Epoch(2019, 1, 1)
    time, r = Jupiter(epoch).passage_nodes()
    y, m, d = time.get_date()
    d = round(d, 1)
    print("Time of passage through ascending node: {}/{}/{}".format(y, m, d))
    # 2025/9/15.6
    print("Radius vector at ascending node: {}".format(round(r, 4)))  # 5.1729


if __name__ == "__main__":
    main()
