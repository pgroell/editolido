# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from unittest import TestCase
import math
from editolido.route import Route
from editolido.geopoint import GeoPoint


class TestRoute(TestCase):
	def test_segments(self):
		a = GeoPoint((0, 0))
		b = GeoPoint((0, 90))
		c = GeoPoint((0, 180))
		route = Route([a, b, c],)
		self.assertEqual(list(route.segments), [(a, b), (b, c)])
		route = Route([a, b],)
		self.assertEqual(list(route.segments), [(a, b)])
		route = Route()
		self.assertEqual(list(route.segments), [])
		route = Route([a, c])
		self.assertEqual(list(route.segments), [(a, c)])

	def test_distance(self):
		route = Route()
		self.assertAlmostEqual(route.distance(converter=None), 0)
		a = GeoPoint((0, 0))
		b = GeoPoint((0, 90))
		c = GeoPoint((0, 180))
		route = Route([a, b, c])
		self.assertAlmostEqual(route.distance(converter=None), math.pi)
		route = Route([c, b, a])
		self.assertAlmostEqual(route.distance(converter=None), math.pi)
		route = Route([a, c])
		self.assertAlmostEqual(route.distance(converter=None), math.pi)
		d = GeoPoint((-90, 0))
		route = Route([a, d, c])
		self.assertAlmostEqual(route.distance(converter=None), math.pi)

	def test_equal(self):
		self.assertEqual(
			Route([GeoPoint((0, 0)), GeoPoint((0, 90))]),
			Route([GeoPoint((0.0000001, 0.0000001)), GeoPoint((0, 90))]),
		)
		self.assertNotEqual(
			Route([GeoPoint((0, 0)), GeoPoint((0, 90))]),
			Route([GeoPoint((0.1, 0)), GeoPoint((0, 90))]),
		)
		self.assertNotEqual(
			Route([GeoPoint((0, 0)), GeoPoint((0, 90))]),
			Route([GeoPoint((0, 0.1)), GeoPoint((0, 90))]),
		)
		self.assertNotEqual(
			Route([GeoPoint((0, 0)), GeoPoint((0, 90))]),
			Route([GeoPoint((0, 0)), GeoPoint((0, 90)), GeoPoint((0, 180))]),
		)
		self.assertNotEqual(
			Route([GeoPoint((0, 0)), GeoPoint((0, 90)), GeoPoint((0, 180))]),
			Route([GeoPoint((0, 0)), GeoPoint((0, 90))]),
		)

	def test_split(self):
		route = Route()
		self.assertEqual(list(route.split(60).segments), [])
		start = GeoPoint((0, 0))
		end = GeoPoint((0, 90))
		route = Route([start, end])
		size = route.distance() / 2
		middle = GeoPoint((0, 45))
		self.assertEqual(
			list(route.split(size).segments),
			[(start, middle), (middle, end)])
		a = GeoPoint((0, 10))
		b = GeoPoint((0, 55))
		route = Route([start, a, end])
		self.assertEqual(
			list(route.split(size).segments),
			[(start, middle), (middle, end)])
		self.assertEqual(
			list(route.split(size, preserve=True).segments),
			[(start, a), (a, b), (b, end)])
		route = Route([start, a, middle, end])
		self.assertEqual(
			list(route.split(size).segments),
			[(start, middle), (middle, end)])
		self.assertEqual(
			list(route.split(size, preserve=True).segments),
			[(start, a), (a, middle), (middle, end)])

		# check we yield the last point
		p = GeoPoint((0, 46.66554361))
		self.assertEqual(route.split(size + 100), Route([start, p, end]))

	def test_as_kml_line(self):
		start = GeoPoint((0, 0))
		end = GeoPoint((0, 90))
		route = Route(
			[start, end], name="route_name", description="route_description")
		self.assertEqual(
			route.as_kml_line(
				'{name}/{style}/{description}/{coordinates}',
				style='route_style'),
			'route_name/route_style/route_description/'
			'0.000000,0.000000 90.000000,0.000000'
		)

	def test_as_kml_points(self):
		start = GeoPoint((0, 0), name="P1")
		end = GeoPoint((0, 90), name="P2", description="D2")
		route = Route(
			[start, end], name="route_name", description="route_description")
		self.assertEqual(
			route.as_kml_points(
				'{name}/{style}/{description}/{coordinates}',
				style='point_style'),
			'P1/point_style//0.000000,0.000000\n'
			'P2/point_style/D2/90.000000,0.000000'
		)

	def test_get_item(self):
		route = Route([GeoPoint((0, 0)), GeoPoint((0, 90))])
		self.assertEqual(route[0], GeoPoint((0, 0)))
		self.assertEqual(route[-1], GeoPoint((0, 90)))
