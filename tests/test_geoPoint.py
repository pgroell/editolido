# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from unittest import TestCase

from editolido import GeoPoint


class TestGeoPoint(TestCase):
	def test_latphi(self):
		from editolido import LatLng, latlng2latphi
		latlng = LatLng(45, -100)
		geopoint = GeoPoint(latlng)
		self.assertEqual(geopoint.latphi, latlng2latphi(latlng))

	def test_distance(self):
		from editolido import latlng_normalizer, rad_to_nm
		geopoint1 = GeoPoint((30, 13), normalizer=latlng_normalizer)
		geopoint2 = GeoPoint((50, -77), normalizer=latlng_normalizer)
		self.assertEqual(
			GeoPoint.distance(geopoint1, geopoint2),
			geopoint1.distance_to(geopoint2),
			msg='unit radians'
		)
		self.assertEqual(
			GeoPoint.distance(geopoint1, geopoint2, converter=rad_to_nm),
			geopoint1.distance_to(geopoint2, converter=rad_to_nm)
		)

	def test_distance_to(self):
		import math
		from editolido import latlng_normalizer, rad_to_nm, rad_to_km
		geopoint1 = GeoPoint((0, 90), normalizer=latlng_normalizer)
		self.assertAlmostEqual(geopoint1.distance_to(geopoint1), 0, msg="distance to self")
		geopoint2 = GeoPoint((0, -90), normalizer=latlng_normalizer)
		self.assertAlmostEqual(geopoint1.distance_to(geopoint2), math.pi, msg="points on equator")
		geopoint2 = GeoPoint((90, -90), normalizer=latlng_normalizer)
		self.assertAlmostEqual(geopoint1.distance_to(geopoint2), math.pi/2, msg="pole to equator")
		geopoint1 = GeoPoint((0, 179), normalizer=latlng_normalizer)
		geopoint2 = GeoPoint((0, -179), normalizer=latlng_normalizer)
		self.assertAlmostEqual(geopoint1.distance_to(geopoint2), 2 * math.pi / 180, msg="date line boundary")
		geopoint1 = GeoPoint((0, 1), normalizer=latlng_normalizer)
		geopoint2 = GeoPoint((0, -1), normalizer=latlng_normalizer)
		self.assertAlmostEqual(geopoint1.distance_to(geopoint2), 2 * math.pi / 180, msg="greenwich boundary")
		geopoint1 = GeoPoint((1, 0), normalizer=latlng_normalizer)
		geopoint2 = GeoPoint((-1, 0), normalizer=latlng_normalizer)
		self.assertAlmostEqual(geopoint1.distance_to(geopoint2), 2 * math.pi / 180, msg="equator boundary")
		geopoint1 = GeoPoint((30, 13), normalizer=latlng_normalizer)
		geopoint2 = GeoPoint((50, -77), normalizer=latlng_normalizer)
		self.assertAlmostEqual(
			geopoint1.distance_to(geopoint2, converter=rad_to_nm), 4051, places=0)
		self.assertAlmostEqual(
			geopoint1.distance_to(geopoint2, converter=rad_to_km), 7503, places=0)

	def test_at_fraction(self):
		from editolido import latlng_normalizer
		geopoint1 = GeoPoint((30, 13), normalizer=latlng_normalizer)
		geopoint2 = GeoPoint((50, -77), normalizer=latlng_normalizer)
		expected = GeoPoint((49.5732910, -23.5838094), normalizer=latlng_normalizer)
		self.assertEqual(geopoint1.at_fraction(geopoint2, 0.5), expected)


	def test_equality(self):
		from editolido import latlng_normalizer, LatLng
		geopoint1 = GeoPoint((30, 13), normalizer=latlng_normalizer)
		geopoint2 = GeoPoint((30, 13), normalizer=latlng_normalizer)
		self.assertEqual(geopoint1, geopoint2)
		self.assertTrue(geopoint1 == geopoint1)
		self.assertEqual(geopoint1, LatLng(30., 13.))
		geopoint3 = GeoPoint((50, -77), normalizer=latlng_normalizer)
		self.assertFalse(geopoint1 == geopoint3)
		self.assertFalse(geopoint1 == (30, 13))
