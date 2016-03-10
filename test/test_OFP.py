# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from cStringIO import StringIO
from unittest import TestCase
import os
import sys

from editolido import OFP
from editolido.route import Route
from editolido.geopoint import GeoPoint, dm_normalizer

DATADIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'data')


class TestOFP(TestCase):
	def test_get_between(self):
		with open(DATADIR + '/KJFK-LFPG 27Mar2015 05:45z.txt', 'r') as f:
			ofp = OFP(f.read())

		s = ofp.get_between('WPT COORDINATES', '----')
		self.assertEqual(s[:4], 'KJFK')
		self.assertEqual(s[-21:-17], 'LFPG')

		s = ofp.get_between('WPT COORDINATES', '----', inclusive=True)
		self.assertTrue(s.startswith('WPT COORDINATES'))
		self.assertTrue(s.endswith('----'))
		self.assertEqual(s[15:19], 'KJFK')
		self.assertEqual(s[-25:-21], 'LFPG')

		out, sys.stdout = sys.stdout, StringIO()
		with self.assertRaises(EOFError):
			ofp.get_between('####', '----')
		sys.stdout = out

		out, sys.stdout = sys.stdout, StringIO()
		with self.assertRaises(EOFError):
			ofp.get_between('WPT COORDINATES', '****', end_is_optional=False)
		sys.stdout = out

		s = ofp.get_between('WPT COORDINATES', '****')
		self.assertTrue(s.endswith('STANDARD\n'))

		s = ofp.get_between('WPT COORDINATES', '****', inclusive=True)
		self.assertTrue(s.endswith('****'))

		s = ofp.get_between(None, 'KJFK/LFPG')
		self.assertEqual(s, 'retrieved: 27Mar/0429zAF  009  ')

		s = ofp.get_between('USED AS A ', None)
		self.assertEqual(s, 'STANDARD\n')

		s = ofp.get_between(None, None)
		self.assertEqual(s, ofp.text)

	def test_wpt_coordinates(self):
		with open(DATADIR + '/KJFK-LFPG 27Mar2015 05:45z.txt', 'r') as f:
			ofp = OFP(f.read())
		points = list(ofp.wpt_coordinates)
		self.assertEqual(len(points), 31)
		self.assertEqual(points[0].name, 'KJFK')
		self.assertEqual(points[-1].name, 'LFPG')
		self.assertEqual(points[5].name, '')
		self.assertEqual(
			points[0],
			GeoPoint('N4038.4W07346.7', normalizer=dm_normalizer))
		self.assertEqual(
			points[-1],
			GeoPoint('N4900.6E00232.9', normalizer=dm_normalizer))
		self.assertEqual(
			points[5],
			GeoPoint('N5100.0W05000.0', normalizer=dm_normalizer))

	def test_missing_wpt_coordinates(self):
		ofp = OFP('blabla blabla')
		out, sys.stdout = sys.stdout, StringIO()
		with self.assertRaises(SystemExit):
			list(ofp.wpt_coordinates)
		sys.stdout = out

	def test_missing_tracks(self):
		ofp = OFP('blabla blabla')
		out, sys.stdout = sys.stdout, StringIO()
		self.assertEqual(list(ofp.tracks), [])
		sys.stdout = out

	def test_tracks(self):
		with open(DATADIR + '/KJFK-LFPG 27Mar2015 05:45z.txt', 'r') as f:
			ofp = OFP(f.read())
		tracks = list(ofp.tracks)
		self.assertEqual(len(tracks), 9)
		self.assertEqual(
			tracks[0],
			Route([
				GeoPoint((56.000000, -20.000000)),
				GeoPoint((57.000000, -30.000000)),
				GeoPoint((58.000000, -40.000000)),
				GeoPoint((58.000000, -50.000000))])
		)
		self.assertEqual(
			tracks[-1],
			Route([
				GeoPoint((42.000000, -40.000000)),
				GeoPoint((38.000000, -50.000000)),
				GeoPoint((33.000000, -60.000000))])
		)
		self.assertTrue(tracks[0].name.endswith('A'))
		self.assertTrue(tracks[-1].name.endswith('J'))

	def test_infos(self):
		from datetime import datetime, timedelta
		from editolido.ofp import utc
		with open(DATADIR + '/KJFK-LFPG 27Mar2015 05:45z.txt', 'r') as f:
			ofp = OFP(f.read())
		expected = {
			'flight': 'AF009',
			'destination': 'LFPG',
			'departure': 'KJFK',
			'datetime': datetime(2015, 3, 27, 5, 45, tzinfo=utc),
			'ofp': '9/0/1',
			'date': '27Mar2015'
		}
		self.assertDictEqual(ofp.infos, expected)
		dt = ofp.infos['datetime']
		self.assertEqual(dt.tzname(), 'UTC')
		self.assertEqual(dt.utcoffset(), timedelta(0))

	def test_filename(self):
		with open(DATADIR + '/KJFK-LFPG 27Mar2015 05:45z.txt', 'r') as f:
			ofp = OFP(f.read())
		self.assertEqual(
			ofp.filename,
			"AF009 KJFK-LFPG 27Mar2015 05:45z OFP 9_0_1.txt"
		)

	def test_description(self):
		with open(DATADIR + '/KJFK-LFPG 27Mar2015 05:45z.txt', 'r') as f:
			ofp = OFP(f.read())
		self.assertEqual(
			ofp.description,
			"AF009 KJFK-LFPG 27Mar2015 05:45z OFP 9/0/1"
		)
