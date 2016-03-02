# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import math
from unittest import TestCase
from editolido import Route, GeoPoint, latlng_normalizer

class TestRoute(TestCase):
	def test_segments(self):
		a = GeoPoint((0, 0), normalizer=latlng_normalizer)
		b = GeoPoint((0, 90), normalizer=latlng_normalizer)
		c = GeoPoint((0, 180), normalizer=latlng_normalizer)
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
		a = GeoPoint((0, 0), normalizer=latlng_normalizer)
		b = GeoPoint((0, 90), normalizer=latlng_normalizer)
		c = GeoPoint((0, 180), normalizer=latlng_normalizer)
		route = Route([a, b, c])
		self.assertAlmostEqual(route.distance(converter=None), math.pi)
		route = Route([c, b, a])
		self.assertAlmostEqual(route.distance(converter=None), math.pi)
		route = Route([a, c])
		self.assertAlmostEqual(route.distance(converter=None), math.pi)
		d = GeoPoint((-90, 0), normalizer=latlng_normalizer)
		route = Route([a, d, c])
		self.assertAlmostEqual(route.distance(converter=None), math.pi)

	def test_split(self):
		route = Route()
		self.assertEqual(list(route.split(60).segments), [])
		start = GeoPoint((0, 0), normalizer=latlng_normalizer)
		end = GeoPoint((0, 90), normalizer=latlng_normalizer)
		route = Route([start, end])
		size = route.distance() / 2
		middle = GeoPoint((0, 45), normalizer=latlng_normalizer)
		self.assertEqual(list(route.split(size).segments), [(start, middle), (middle, end)])
		a = GeoPoint((0, 10), normalizer=latlng_normalizer)
		b = GeoPoint((0, 55), normalizer=latlng_normalizer)
		route = Route([start, a, end])
		self.assertEqual(list(route.split(size).segments), [(start, middle), (middle, end)])
		self.assertEqual(list(route.split(size, preserve=True).segments), [(start, a), (a, b), (b, end)])
		route = Route([start, a, middle, end])
		self.assertEqual(list(route.split(size).segments), [(start, middle), (middle, end)])
		self.assertEqual(list(route.split(size, preserve=True).segments), [(start, a), (a, middle), (middle, end)])
