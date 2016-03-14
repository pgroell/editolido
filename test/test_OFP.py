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

		with self.assertRaises(LookupError):
			ofp.get_between('####', '----')

		with self.assertRaises(EOFError):
			ofp.get_between('WPT COORDINATES', '****', end_is_optional=False)

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
		self.assertEqual(list(ofp.tracks), [])
		with self.assertRaises(LookupError):
			ofp.tracks_iterator()

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

	def test_fpl_lookup_error(self):
		ofp = OFP('')
		out, sys.stdout = sys.stdout, StringIO()
		self.assertEqual(ofp.fpl, [])
		sys.stdout = out
		ofp = OFP('ATC FLIGHT PLANblabla')
		output = StringIO()
		out, sys.stdout = sys.stdout, output
		self.assertEqual(ofp.fpl, [])
		self.assertIn('incomplete Flight Plan', output.getvalue())
		sys.stdout = out
		output.close()

	def test_fpl(self):
		with open(DATADIR + '/KJFK-LFPG 27Mar2015 05:45z.txt', 'r') as f:
			ofp = OFP(f.read())
		self.assertEqual(
			' '.join(ofp.fpl),
			"KJFK DCT GREKI DCT MARTN DCT EBONY/M084F350 N247A ALLRY/M084F370 "
			"DCT 51N050W 53N040W 55N030W 55N020W DCT RESNO DCT "
			"NETKI/N0479F350 DCT BAKUR/N0463F350 UN546 STU UP2 "
			"NIGIT UL18 SFD/N0414F250 UM605 BIBAX BIBAX7W LFPG"
		)

	def test_fpl_route(self):
		with open(DATADIR + '/KJFK-LFPG 27Mar2015 05:45z.txt', 'r') as f:
			ofp = OFP(f.read())
		self.assertEqual(
			' '.join(ofp.fpl_route),
			"KJFK DCT GREKI DCT MARTN DCT EBONY N247A ALLRY "
			"DCT 51N050W 53N040W 55N030W 55N020W DCT RESNO DCT "
			"NETKI DCT BAKUR UN546 STU UP2 "
			"NIGIT UL18 SFD UM605 BIBAX BIBAX7W LFPG"
		)

	def test_lido_route(self):
		with open(DATADIR + '/KJFK-LFPG 27Mar2015 05:45z.txt', 'r') as f:
			ofp = OFP(f.read())
		self.assertEqual(
			' '.join(ofp.lido_route),
			'KJFK GREKI DCT MARTN DCT EBONY N247A ALLRY DCT 51N050W '
			'53N040W 55N030W 55N020W DCT RESNO DCT NETKI DCT BAKUR UN546 '
			'STU UP2 NIGIT UL18 SFD UM605 BIBAX N4918.0E00134.2 '
			'N4917.5E00145.4 N4915.7E00223.3 N4915.3E00230.9 '
			'N4913.9E00242.9 LFPG'
		)

	def test_lido_route_no_tracksnat(self):
		with open(DATADIR + '/KJFK-LFPG 27Mar2015 05:45z.txt', 'r') as f:
			ofp = OFP(f.read())
		ofp.text = ofp.text.replace('TRACKSNAT', 'TRACKSNA*')
		self.assertEqual(
			' '.join(ofp.lido_route),
			'KJFK GREKI DCT MARTN DCT EBONY N247A ALLRY DCT 51N050W '
			'53N040W 55N030W 55N020W DCT RESNO DCT NETKI DCT BAKUR UN546 '
			'STU UP2 NIGIT UL18 SFD UM605 BIBAX N4918.0E00134.2 '
			'N4917.5E00145.4 N4915.7E00223.3 N4915.3E00230.9 '
			'N4913.9E00242.9 LFPG'
		)

	def test_lido_route_no_fpl(self):
		with open(DATADIR + '/KJFK-LFPG 27Mar2015 05:45z.txt', 'r') as f:
			ofp = OFP(f.read())
		ofp.text = ofp.text.replace('ATC FLIGHT PLAN', 'ATC*FLIGHT*PLAN')
		output = StringIO()
		out, sys.stdout = sys.stdout, output
		self.assertEqual(
			' '.join(ofp.lido_route),
			'KJFK GREKI MARTN EBONY ALLRY N5100.0W05000.0 N5300.0W04000.0 '
			'N5500.0W03000.0 N5500.0W02000.0 RESNO NETKI BAKUR STU NUMPO '
			'OKESI BEDEK NIGIT VAPID MID SFD WAFFU HARDY XIDIL PETAX BIBAX '
			'KOLIV MOPAR N4915.7E00223.3 CRL N4913.9E00242.9 LFPG'
		)
		sys.stdout = out
		output.close()

	def test_lido_route_with_naty(self):
		with open(DATADIR + '/AF007_KJFK-LFPG_13Mar2016_00:15z_OFP_6_0_1.txt',
		          'r') as f:
			ofp = OFP(f.read())
		self.assertEqual(
			' '.join(ofp.lido_route),
			'KJFK HAPIE DCT YAHOO DCT DOVEY 42N060W 43N050W 46N040W 49N030W '
			'49N020W BEDRA NERTU DCT TAKAS UN490 MOSIS UN491 BETUV UY111 '
			'JSY UY111 INGOR UM25 LUKIP N4918.0E00134.2 '
			'N4917.5E00145.4 N4910.2E00150.4 LFPG'
		)

	def test_lido_route_with_naty_no_fpl(self):
		with open(DATADIR + '/AF007_KJFK-LFPG_13Mar2016_00:15z_OFP_6_0_1.txt',
		          'r') as f:
			ofp = OFP(f.read())
		ofp.text = ofp.text.replace('ATC FLIGHT PLAN', 'ATC*FLIGHT*PLAN')
		output = StringIO()
		out, sys.stdout = sys.stdout, output
		self.assertEqual(
			' '.join(ofp.lido_route),
			'KJFK HAPIE YAHOO DOVEY N4200.0W06000.0 N4300.0W05000.0 '
			'N4600.0W04000.0 N4900.0W03000.0 N4900.0W02000.0 BEDRA NERTU '
			'TAKAS ALUTA MOSIS DEKOR NERLA RUSIB BETUV JSY INGOR LUKIP '
			'KOLIV MOPAR N4910.2E00150.4 LFPG'
		)
		sys.stdout = out
		output.close()

	def test_lido_route_with_naty_no_tracksnat(self):
		with open(DATADIR + '/AF007_KJFK-LFPG_13Mar2016_00:15z_OFP_6_0_1.txt',
		          'r') as f:
			ofp = OFP(f.read())
		ofp.text = ofp.text.replace('TRACKSNAT', 'TRACKSNA*')
		self.assertEqual(
			' '.join(ofp.lido_route),
			'KJFK HAPIE DCT YAHOO DCT DOVEY NATY NERTU DCT TAKAS UN490 '
			'MOSIS UN491 BETUV UY111 '
			'JSY UY111 INGOR UM25 LUKIP N4918.0E00134.2 '
			'N4917.5E00145.4 N4910.2E00150.4 LFPG'
		)
