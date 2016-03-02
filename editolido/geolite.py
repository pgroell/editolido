# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import math
import operator
from collections import namedtuple
from decimal import Decimal
from functools import partial

import itertools

"""
latitude is a Decimal and unit is degrees
longitude is a Decimal and unit is degrees

rlat is the float latitude in radians (rlat because lambda is a reserved name in python)
phi is the float longitude in radians

To store a tuple of (latitude, longitude), use the namedtuple LatLng
To store a tuple of (longitude, latitude), use the namedtuple LngLat
To store a tuple of (rlat, phi), use the namedtuple LatPhi

Although KML uses LngLat coordinates, in the code always use LatLng in "standard"

The GeoPoint class takes a LatLng as input and stores an optional reference, it also accepts a normalizer.
The normalizer is a way to transform anything into a something

"""
R = 6371000.0  # eath mean radius in meters
NM = 1852.0  # nm in meters

# Base points
LatLng = namedtuple('LatLng', ['latitude', 'longitude'])
LatPhi = namedtuple('LatPhi', ['rlat', 'phi'])
LngLat = namedtuple('LngLat', ['longitude', 'latitude'])

# Converters
rad_to_nm = partial(operator.mul, R / NM)
rad_to_km = partial(operator.mul, R / 1000.0)
nm_to_rad = partial(operator.mul, NM / R)
km_to_nm = partial(operator.mul, 1000.0 / NM)

def rounded(f):
	return Decimal(round(f, 7))

# Normalizers
def latlng_normalizer(v):
	return LatLng(*map(Decimal, v))


def latlng2latphi(latlng):
	"""
	Converts a LatLng to a LatPhi
	:param latlng: LatLng
	:return: LatPhi
	"""
	return LatPhi(*map(math.radians, latlng))


def latphi2latlng(latphi):
	"""
	Converts a LatPhi to a LatLng
	:param latphi: LatPhi
	:return: LatLng
	"""
	return LatLng(*map(Decimal, map(math.degrees, latphi)))


class GeoPoint(object):
	__slots__ = ('latlng', 'ref', '_latphi')

	def __init__(self, latlng, ref=None, normalizer=None):
		self.latlng = normalizer(latlng) if normalizer else latlng
		self.ref = ref
		self._latphi = None

	@property
	def latitude(self):
		return self.latlng.latitude

	@property
	def longitude(self):
		return self.latlng.longitude

	@property
	def longitude(self):
		return self.latlng.longitude

	@property
	def latphi(self):
		"""
		Lazy conversion LatPhi.
		:return: float
		"""
		if self._latphi is None:
			self._latphi = LatPhi(*map(math.radians, self.latlng))
		return self._latphi

	def __eq__(self, other):
		"""
		Check if other point has same coordinates to current or not.
		"""
		try:
			return (
				round(self.latitude, 6) == round(other.latitude, 6) and
				round(self.longitude, 6) == round(other.longitude, 6)
			)
		except AttributeError:
			return False

	def __repr__(self):
		"""
		Machine representation of GeoPoint instance.
		"""
		try:
			return '{2}({0:.6}, {1:.6})'.format(self.latitude, self.longitude, self.__class__.__name__)
		except AttributeError:
			return '{1}({0})'.format(self, self.__class__.__name__)

	__str__ = __repr__
	__str__.__doc__ = 'String representation of Point instance.'
	@staticmethod
	def distance(geopoint1, geopoint2, converter=None):
		return geopoint1.distance_to(geopoint2, converter=converter)

	def distance_to(self, other, converter=None):
		"""
		returns the distance in radians between 2 GeoPoints
		:param other: GeoPoint
		:param converter: function to convert distance in another unit
		:return: float
		"""
		rlat1, phi1 = self.latphi
		rlat2, phi2 = other.latphi
		sd = math.acos(
			math.sin(rlat1) * math.sin(rlat2) +
			math.cos(rlat1) * math.cos(rlat2) * math.cos(phi2 - phi1))
		if converter:
			return converter(sd)
		return sd

	def at_fraction(self, other, fraction, distance=None):
		"""
		computes intermediate point at fraction of other on great circle
		:param other: GeoPoint
		:param fraction: float between 0 and 1
		:param distance: float or None distance between self and other
		:return: GeoPoint
		"""
		d = distance
		if distance is None:
			d = self.distance_to(other, converter=None)
		rlat1, phi1 = self.latphi
		rlat2, phi2 = other.latphi
		a = math.sin((1 - fraction) * d) / math.sin(d)
		b = math.sin(fraction * d) / math.sin(d)
		x = a * math.cos(rlat1) * math.cos(phi1) + b * math.cos(rlat2) * math.cos(phi2)
		y = a * math.cos(rlat1) * math.sin(phi1) + b * math.cos(rlat2) * math.sin(phi2)
		z = a * math.sin(rlat1) + b * math.sin(rlat2)
		rlat = math.atan2(z, math.sqrt(math.pow(x, 2) + math.pow(y, 2)))
		phi = math.atan2(y, x)
		return self.__class__((rlat, phi), normalizer=latphi2latlng)


class Route(object):
	"""
	A collection of GeoPoints
	"""
	def __init__(self, points=None, name=None, description=None):
		self._route = points if points else []
		self.name = name
		self.description = description

	@property
	def segments(self):
		"""
		Iterator the route in pairs of GeoPoints
		:return: generator of GeoPoints
		"""
		a, b = itertools.tee(self._route)
		next(b, None)
		return itertools.izip(a, b)

	def _segment_distance(self, segment):
		return segment[0].distance_to(segment[1]) if segment else 0

	def distance(self, converter=rad_to_nm):
		d = sum(itertools.imap(self._segment_distance, self.segments))
		if converter:
			return converter(d)
		return d

	def split(self, max_length, converter=nm_to_rad, preserve=False):
		"""
		Split a route in smaller segments.
		The new Route is different from the original one as original start and end of
		segments are not preserved by default
		:param max_length: max segment lenght in radians unless a converter is used
		:param converter: a unit converter function, convert unit into radians
		:param preserve: always emit the GeoPoint from the original route
		:return: Route
		"""

		# noinspection PyShadowingNames
		def splitted_route_generator(max_radians, preserve):
			remaining = 0
			geopoint2 = None
			first = True
			for geopoint1, geopoint2 in self.segments:
				if first:
					first = False
					yield geopoint1  # first point
				segment_length = geopoint1.distance_to(geopoint2)
				d = remaining
				while d <= segment_length - max_radians:
					d += max_radians
					f = d / segment_length
					yield geopoint1.at_fraction(geopoint2, f, distance=segment_length)
				remaining = round(d - segment_length, 10)
				if preserve and remaining:
					yield geopoint2
					remaining = 0
			if remaining:
				yield geopoint2  # last if not yet emitted

		size = converter(max_length) if converter else max_length
		return self.__class__(splitted_route_generator(size, preserve))
