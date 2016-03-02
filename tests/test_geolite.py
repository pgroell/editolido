# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from unittest import TestCase


class TestGeolite(TestCase):
	def test_latlng2latphi(self):
		import math
		from editolido import LatPhi, LatLng, latlng2latphi
		latlng = LatLng(45.0, 50.0)
		latphi = latlng2latphi(latlng)
		self.assertIsInstance(latphi, LatPhi)
		self.assertIsInstance(latphi.rlat, float)
		self.assertIsInstance(latphi.phi, float)
		self.assertAlmostEqual(latphi.rlat, math.radians(latlng.latitude))
		self.assertAlmostEqual(latphi.phi, math.radians(latlng.longitude))


	def test_latphi2latlng(self):
		import math
		from decimal import Decimal
		from editolido import LatPhi, LatLng, latphi2latlng
		latphi = LatPhi(0.3, -1.0)
		latlng = latphi2latlng(latphi)
		self.assertIsInstance(latlng, LatLng)
		self.assertIsInstance(latlng.latitude, Decimal)
		self.assertIsInstance(latlng.longitude, Decimal)
		self.assertAlmostEqual(latlng.latitude, math.degrees(latphi.rlat))
		self.assertAlmostEqual(latlng.longitude, math.degrees(latphi.phi))


	def test_rad_to_nm(self):
		from editolido import rad_to_nm, R, NM
		self.assertAlmostEqual(rad_to_nm(1), R / NM)
		self.assertAlmostEqual(rad_to_nm(1./3600), 0.95557355)


	def test_nm_to_rad(self):
		from editolido import nm_to_rad, R, NM
		self.assertAlmostEqual(nm_to_rad(0.95557355), 1./3600)
		self.assertAlmostEqual(nm_to_rad(R / NM), 1)


	def test_rad_to_km(self):
		from editolido import rad_to_km
		self.assertAlmostEqual(rad_to_km(1), 6371)


	def test_km_to_nm(self):
		from editolido import km_to_nm
		self.assertAlmostEqual(km_to_nm(1.852), 1)


	def test_latlng_normalizer(self):
		from decimal import Decimal
		from editolido import latlng_normalizer, LatLng
		v = (1, 2)
		latlng = latlng_normalizer(v)
		self.assertIsInstance(latlng, LatLng)
		self.assertIsInstance(latlng[0], Decimal)
		self.assertIsInstance(latlng[1], Decimal)

