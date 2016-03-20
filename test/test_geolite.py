# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from unittest import TestCase
from decimal import Decimal


class TestGeolite(TestCase):

    def test_latphi2latlng(self):
        import math
        from editolido.geolite import LatPhi, LatLng, latphi2latlng
        latphi = LatPhi(0.3, -1.0)
        latlng = latphi2latlng(latphi)
        self.assertIsInstance(latlng, LatLng)
        self.assertIsInstance(latlng.latitude, Decimal)
        self.assertIsInstance(latlng.longitude, Decimal)
        self.assertAlmostEqual(latlng.latitude, math.degrees(latphi.rlat))
        self.assertAlmostEqual(latlng.longitude, math.degrees(latphi.phi))

    def test_rad_to_nm(self):
        from editolido.geolite import rad_to_nm, R, NM
        self.assertAlmostEqual(rad_to_nm(1), R / NM)
        self.assertAlmostEqual(rad_to_nm(1. / 3600), 0.95557355)

    def test_nm_to_rad(self):
        from editolido.geolite import nm_to_rad, R, NM
        self.assertAlmostEqual(nm_to_rad(0.95557355), 1. / 3600)
        self.assertAlmostEqual(nm_to_rad(R / NM), 1)

    def test_rad_to_km(self):
        from editolido.geolite import rad_to_km
        self.assertAlmostEqual(rad_to_km(1), 6371)

    def test_km_to_nm(self):
        from editolido.geolite import km_to_nm
        self.assertAlmostEqual(km_to_nm(1.852), 1)

    def test_latlng_normalizer(self):
        from editolido.geolite import LatLng
        from editolido.geopoint import latlng_normalizer
        v = (1, 2)
        latlng = latlng_normalizer(v)
        self.assertIsInstance(latlng, LatLng)
        self.assertIsInstance(latlng[0], Decimal)
        self.assertIsInstance(latlng[1], Decimal)

    def test_dm2decimal(self):
        from editolido.geolite import dm2decimal
        self.assertIsInstance(dm2decimal('N5500.0'), Decimal)
        self.assertEqual(dm2decimal('N5530.3'), Decimal('55.505'))
        self.assertEqual(dm2decimal('S5530.3'), Decimal('-55.505'))
        self.assertEqual(dm2decimal('E05530.3'), Decimal('55.505'))
        self.assertEqual(dm2decimal('W05530.3'), Decimal('-55.505'))
        with self.assertRaises(AssertionError):
            dm2decimal('U05530.3')

    def test_arinc_normalizer(self):
        from editolido.geolite import LatLng
        from editolido.geopoint import arinc_normalizer
        self.assertIsInstance(arinc_normalizer('55N020W'), LatLng)
        self.assertEqual(arinc_normalizer('55N020W'), LatLng(55, -20))
        self.assertEqual(arinc_normalizer('55S020W'), LatLng(-55, -20))
        self.assertEqual(arinc_normalizer('55S020E'), LatLng(-55, 20))
        self.assertEqual(arinc_normalizer('55N020E'), LatLng(55, 20))
        self.assertEqual(arinc_normalizer('N5520'), LatLng(55.5, -20))
        self.assertEqual(arinc_normalizer('E5520'), LatLng(55.5, 20))
        self.assertEqual(arinc_normalizer('S5520'), LatLng(-55.5, 20))
        self.assertEqual(arinc_normalizer('5N520'), LatLng(55.5, -120))
        self.assertEqual(arinc_normalizer('5E520'), LatLng(55.5, 120))
        self.assertEqual(arinc_normalizer('5S520'), LatLng(-55.5, 120))
        self.assertEqual(arinc_normalizer('5W520'), LatLng(-55.5, -120))
        self.assertEqual(arinc_normalizer('5530N020W'), LatLng(55.5, -20))
        self.assertEqual(arinc_normalizer('5530N02000W'), LatLng(55.5, -20))
        with self.assertRaises(AssertionError):
            arinc_normalizer('5U520')
        with self.assertRaises(AssertionError):
            arinc_normalizer('U55520')

    def test_dm_normalizer(self):
        from editolido.geolite import LatLng
        from editolido.geopoint import dm_normalizer
        self.assertEqual(
            dm_normalizer('N5530.3E01030.3'),
            LatLng(Decimal('55.505'), Decimal('10.505')))

    def test_latlng2dm(self):
        from editolido.geolite import latlng2dm, LatLng
        self.assertEqual(
            latlng2dm(LatLng(0, 0)),
            'N0000.0W00000.0'
        )
        self.assertEqual(
            latlng2dm(LatLng(45, 0)),
            'N4500.0W00000.0'
        )
        self.assertEqual(
            latlng2dm(LatLng(-45, 1)),
            'S4500.0E00100.0'
        )
        self.assertEqual(
            latlng2dm(LatLng(-45.508333, 1.3)),
            'S4530.5E00118.0'
        )
        self.assertEqual(
            latlng2dm(LatLng(45.55, 1.55)),
            'N4533.0E00133.0'
        )
