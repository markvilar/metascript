"""
Copyright (c) 2014-2022 Michael Hirsch, Ph.D.
Copyright (c) 2013, Felipe Geremia Nievinski
Copyright (c) 2004-2007 Michael Kleder

Redistribution and use in source and binary forms, with or without modification, are permitted provided that the following conditions are met:

1. Redistributions of source code must retain the above copyright notice, this list of conditions and the following disclaimer.

2. Redistributions in binary form must reproduce the above copyright notice, this list of conditions and the following disclaimer in the documentation and/or other materials provided with the distribution.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
"""

import numpy as np

from .ellipsoid import Ellipsoid

def sanitize(lat, ell: Ellipsoid | None, deg: bool) -> tuple:
    if ell is None:
        ell = Ellipsoid.from_name("wgs84")

    try:
        lat = asarray(lat)
    except NameError:
        pass

    if deg:
        lat = np.radians(lat)

    try:
        if (abs(lat) > np.pi / 2).any():  # type: ignore
            raise ValueError("-pi/2 <= latitude <= pi/2")
    except AttributeError:
        if abs(lat) > np.pi / 2:  # type: ignore
            raise ValueError("-pi/2 <= latitude <= pi/2")

    return lat, ell

def uvw2enu(u, v, w, lat0, lon0, deg: bool = True) -> tuple:
    """
    Parameters
    ----------
    u
    v
    w
    Results
    -------
    East
        target east ENU coordinate (meters)
    North
        target north ENU coordinate (meters)
    Up
        target up ENU coordinate (meters)
    """
    if deg:
        lat0 = np.radians(lat0)
        lon0 = np.radians(lon0)

    t = np.cos(lon0) * u + np.sin(lon0) * v
    East = -np.sin(lon0) * u + np.cos(lon0) * v
    Up = np.cos(lat0) * t + np.sin(lat0) * w
    North = -np.sin(lat0) * t + np.cos(lat0) * w

    return East, North, Up


def geodetic2ecef(
        lats,
        lons,
        alts,
        ell: Ellipsoid = None,
        deg: bool = True,
    ) -> tuple:
    """
    point transformation from Geodetic of specified ellipsoid (default WGS-84) 
    to ECEF
    Parameters
    ----------
    lat
           target geodetic latitude
    lon
           target geodetic longitude
    h
         target altitude above geodetic ellipsoid (meters)
    ell : Ellipsoid, optional
          reference ellipsoid
    deg : bool, optional
          degrees input/output  (False: radians in/out)
    Returns
    -------
    ECEF (Earth centered, Earth fixed)  x,y,z
    x
        target x ECEF coordinate (meters)
    y
        target y ECEF coordinate (meters)
    z
        target z ECEF coordinate (meters)
    """
    lats, ell = sanitize(lats, ell, deg)
    if deg:
        lons = np.radians(lons)

    # radius of curvature of the prime vertical section
    N = ell.semimajor_axis**2 / np.sqrt(
            ell.semimajor_axis**2 * np.cos(lats) ** 2 \
            + ell.semiminor_axis**2 * np.sin(lats) ** 2
        )
    # Compute cartesian (geocentric) coordinates given (curvilinear) geodetic 
    # coordinates.
    x = (N + alts) * np.cos(lats) * np.cos(lons)
    y = (N + alts) * np.cos(lats) * np.sin(lons)
    z = (N * (ell.semiminor_axis / ell.semimajor_axis) ** 2 + alts) \
        * np.sin(lats)

    return x, y, z

def geodetic2enu(
        lats,
        lons,
        heights,
        ref_lat,
        ref_lon,
        ref_height,
        ell: Ellipsoid = None,
        deg: bool = True,
    ) -> tuple:
    """
    Parameters
    ----------
    lats : np.ndarray
        target geodetic latitude
    lons : np.ndarray
        target geodetic longitude
    heights : np.ndarray
        target altitude above ellipsoid  (meters)
    ref_lat : float
        observer geodetic latitude
    ref_lon : float
        observer geodetic longitude
    ref_height : float
        observer altitude above geodetic ellipsoid (meters)
    ell : Ellipsoid, optional
        reference ellipsoid
    deg : bool, optional
        degrees input/output  (False: radians in/out)
    Results
    -------
    easts : np.ndarray
        East ENU
    norths : np.ndarray
        North ENU
    ups : np.ndarray
        Up ENU
    """
    x1, y1, z1 = geodetic2ecef(lats, lons, heights, ell, deg=deg)
    x2, y2, z2 = geodetic2ecef(ref_lat, ref_lon, ref_height, ell, deg=deg)

    return uvw2enu(x1 - x2, y1 - y2, z1 - z2, ref_lat, ref_lon, deg=deg)


def geodetic2ned(
        lats,
        lons,
        heights,
        ref_lat,
        ref_lon,
        ref_height,
        ell: Ellipsoid = None,
        deg: bool = True,
    ) -> tuple:
    """
    convert latitude, longitude, altitude of target to North, East, Down from 
    observer
    Parameters
    ----------
    lats : np.ndarray
        target geodetic latitude
    lons : np.ndarray
        target geodetic longitude
    heights : np.ndarray
        target altitude above geodetic ellipsoid (meters)
    ref_lat : float
        observer geodetic latitude
    ref_lon : float
        observer geodetic longitude
    ref_height : float
         observer altitude above geodetic ellipsoid (meters)
    ell : Ellipsoid, optional
        reference ellipsoid
    deg : bool, optional
        degrees input/output  (False: radians in/out)
    Results
    -------
    norths : np.ndarray
        North NED coordinate (meters)
    easts : np.ndarray
        East NED coordinate (meters)
    downs : np.ndarray
        Down NED coordinate (meters)
    """
    assert lats.shape == lons.shape == heights.shape, \
        "unequal number of lats, lons, heights"
    easts, norths, ups = geodetic2enu(lats, lons, heights, ref_lat, ref_lon, 
        ref_height, ell, deg=deg)

    return norths, easts, -ups
