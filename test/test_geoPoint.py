# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from unittest import TestCase

from editolido.geopoint import GeoPoint


class TestGeoPoint(TestCase):
    def test_latphi(self):
        from editolido.geolite import LatLng, LatPhi
        latlng = LatLng(45, -100)
        geopoint = GeoPoint(latlng)
        expected = LatPhi(rlat=0.7853981633974483, phi=-1.7453292519943295)
        self.assertEqual(geopoint.latphi, expected)

    def test_distance(self):
        from editolido.geolite import rad_to_nm
        geopoint1 = GeoPoint((30, 13))
        geopoint2 = GeoPoint((50, -77))
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
        from editolido.geolite import rad_to_nm, rad_to_km
        geopoint1 = GeoPoint((0, 90))
        self.assertAlmostEqual(
            geopoint1.distance_to(geopoint1),
            0, msg="distance to self")
        geopoint2 = GeoPoint((0, -90))
        self.assertAlmostEqual(
            geopoint1.distance_to(geopoint2),
            math.pi, msg="points on equator")
        geopoint2 = GeoPoint((90, -90))
        self.assertAlmostEqual(
            geopoint1.distance_to(geopoint2),
            math.pi / 2, msg="pole to equator")
        geopoint1 = GeoPoint((0, 179))
        geopoint2 = GeoPoint((0, -179))
        self.assertAlmostEqual(
            geopoint1.distance_to(geopoint2),
            2 * math.pi / 180, msg="date line boundary")
        geopoint1 = GeoPoint((0, 1))
        geopoint2 = GeoPoint((0, -1))
        self.assertAlmostEqual(
            geopoint1.distance_to(geopoint2),
            2 * math.pi / 180, msg="greenwich boundary")
        geopoint1 = GeoPoint((1, 0))
        geopoint2 = GeoPoint((-1, 0))
        self.assertAlmostEqual(
            geopoint1.distance_to(geopoint2),
            2 * math.pi / 180, msg="equator boundary")
        geopoint1 = GeoPoint((30, 13))
        geopoint2 = GeoPoint((50, -77))
        self.assertAlmostEqual(
            geopoint1.distance_to(geopoint2, converter=rad_to_nm),
            4051, places=0)
        self.assertAlmostEqual(
            geopoint1.distance_to(geopoint2, converter=rad_to_km),
            7503, places=0)

    def test_at_fraction(self):
        geopoint1 = GeoPoint((30, 13))
        geopoint2 = GeoPoint((50, -77))
        expected = GeoPoint((49.5732910, -23.5838094))
        self.assertEqual(geopoint1.at_fraction(geopoint2, 0.5), expected)

    def test_equality(self):
        from editolido.geolite import LatLng
        geopoint1 = GeoPoint((30, 13))
        geopoint2 = GeoPoint((30, 13))
        self.assertEqual(geopoint1, geopoint2)
        self.assertTrue(geopoint1 == geopoint1)
        self.assertEqual(geopoint1, LatLng(30., 13.))
        geopoint3 = GeoPoint((50, -77))
        self.assertFalse(geopoint1 == geopoint3)
        self.assertNotEqual(geopoint1, geopoint3)
        with self.assertRaises(ValueError):
            geopoint1 == (30, 13)
        self.assertEqual(GeoPoint((0, 46.6822)), GeoPoint((0, 46.6822001)))

    def test_repr(self):
        self.assertEqual(
            "%s" % GeoPoint((10, 20)),
            'GeoPoint((10.000000, 20.000000))')
        self.assertEqual(
            "%s" % GeoPoint((10, 20), name="WPT"),
            'GeoPoint(WPT(10.000000, 20.000000))')

    def test_init_value_is_geopoint(self):
        geopoint1 = GeoPoint((30, 13))
        geopoint2 = GeoPoint(geopoint1, name='P2', description='D2')
        self.assertEqual(geopoint1, geopoint2)
        self.assertEqual(geopoint2.name, 'P2')
        self.assertEqual(geopoint2.description, 'D2')

    def test_creation_from_latphi(self):
        from editolido.geolite import latphi2latlng
        a = GeoPoint((0.7853981633974483, -1.7453292519943295),
                     normalizer=latphi2latlng)
        self.assertEqual(a, GeoPoint((45, -100)))
