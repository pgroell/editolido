# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import math
from decimal import Decimal
from editolido.geolite import LatLng, LatPhi, latphi2latlng, dm2decimal


# Normalizers
def latlng_normalizer(v):
	"""
	Normalize value into LatLng by converting values into Decimal
	Useful for testing (it is the default normalizer)
	:param v:
	:return:
	"""
	return LatLng(*map(Decimal, v))


def dm_normalizer(v):
	"""
	Normalize degrees minute value into LatLng
	accepts: 'N4038.4W07346.7' or ('N4038.4', 'W07346.7') values
	:param v: str or tuple
	:return: LatLng
	"""
	try:
		lat, lng = v
	except ValueError:
		lat, lng = v[:7], v[7:]
	return LatLng(dm2decimal(lat), dm2decimal(lng))


def arinc_normalizer(s):
	"""
	Normalize ARINC point into LatLng
	:param s:
	:return:
	"""

	# noinspection PyShadowingNames
	def signed(letter, lat, lng):
		assert letter in 'NSEW'
		if letter == 'N':  # NW +-
			return LatLng(lat, -lng)
		elif letter == 'E':  # NE ++
			return LatLng(lat, lng)
		elif letter == 'S':  # SE -+
			return LatLng(-lat, lng)
		elif letter == 'W':  # SW --
			return LatLng(-lat, -lng)

	if s[0] in 'NESW':
		# N5520  lon<100
		lat = Decimal(s[1:3]) + Decimal(0.5)
		lng = Decimal(s[3:5])
		return signed(s[0], lat, lng)
	elif s[1] in 'NESW':
		# 5N520  lon>=100
		lat = Decimal(s[0] + s[2]) + Decimal(0.5)
		lng = Decimal('1' + s[3:5])
		return signed(s[1], lat, lng)
	else:
		# 55N020W => N5500.0W02000.0 => (-20.0, 55.0)
		lat = dm2decimal(s[2:3] + s[0:2] + '00.0')
		lng = dm2decimal(s[6:7] + s[3:6] + '00.0')
		return LatLng(lat, lng)


class GeoPoint(object):
	"""
	The GeoPoint class is used to store geographical points
	"""
	__slots__ = ('latlng', 'name', 'description', '_latphi')

	def __init__(
		self, value, name=None, description=None,
		normalizer=latlng_normalizer):
		"""
		A GeoPoint value might be:
		- a LatLng with normalizer=None
		- a tuple with the latlng_normalizer
		- a degrees minutes coordinates with the dm2decimal_normalizer
		- a string in ARINC format with the arinc_normalizer

		:param value: LatLng or tuple or str
		:param name: optional name for the point
		:param description: optional description
		:param normalizer: function to use to get a LatLng from value
		"""
		self.latlng = normalizer(value) if normalizer else value
		assert isinstance(self.latlng, LatLng)
		self.name = name
		self.description = description
		self._latphi = None

	@property
	def latitude(self):
		return self.latlng.latitude

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
		Check if other point has almost the same coordinates.
		"""
		try:
			return (
				"{0:.6f}".format(self.latitude) == "{0:.6f}".format(
					other.latitude) and
				"{0:.6f}".format(self.longitude) == "{0:.6f}".format(
					other.longitude)
			)
		except AttributeError:
			raise ValueError(
				'can not compare %s and %s'
				% (self.__class__.__name__, type(other)))

	def __ne__(self, other):
		return not self.__eq__(other)

	def __repr__(self):
		"""
		Machine representation of GeoPoint instance.
		"""
		return '{klass}({ref}({lat:.6f}, {lng:.6f}))'.format(
			lat=self.latitude,
			lng=self.longitude,
			klass=self.__class__.__name__,
			ref=self.name or '')

	__str__ = __repr__
	__str__.__doc__ = 'String representation of GeoPoint instance.'

	@staticmethod
	def distance(geopoint1, geopoint2, converter=None):
		"""
		Get the spherical distance between two GeoPoints
		:param geopoint1: GeoPoint
		:param geopoint2: GeoPoint
		:param converter: unit to use (default = radians)
		:return: float the distance in the unit defined by the converter
		"""
		return geopoint1.distance_to(geopoint2, converter=converter)

	def distance_to(self, other, converter=None):
		"""
		Get the spherical distance from another GeoPoint
		:param other: GeoPoint
		:param converter: unit to use (default = radians)
		:return: float the distance in the unit defined by the converter
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
		if distance=None, the required distance will be computed
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
		x = a * math.cos(rlat1) * math.cos(phi1) \
			+ b * math.cos(rlat2) * math.cos(phi2)
		y = a * math.cos(rlat1) * math.sin(phi1) \
			+ b * math.cos(rlat2) * math.sin(phi2)
		z = a * math.sin(rlat1) + b * math.sin(rlat2)
		rlat = math.atan2(z, math.sqrt(math.pow(x, 2) + math.pow(y, 2)))
		phi = math.atan2(y, x)
		return self.__class__((rlat, phi), normalizer=latphi2latlng)

	def as_kml(self, template, **kwargs):
		"""
		Render name, description and coordinates in a suitable format for .kml
		:param template: str the template file to use
		:param kwargs: optional arguments passed to the template
		:return: str
		"""
		coordinates = "{lng:.6f},{lat:.6f}".format(
			lat=self.latitude, lng=self.longitude)
		variables = dict(
			name=self.name or '',
			description=self.description or '')
		variables.update(kwargs)
		return template.format(
			coordinates=coordinates,
			**variables)
