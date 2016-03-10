# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from unittest import TestCase

from editolido.kml import KMLGenerator


class TestKMLGenerator(TestCase):
	def test_add_folder(self):
		kml = KMLGenerator()
		self.assertFalse(kml.folders)
		kml.add_folder('first')
		self.assertFalse(kml.folders['first'], [])
		kml.add_folder('second')
		self.assertEqual(kml.folders.keys(), ['first', 'second'])

	def test_add_folders(self):
		kml = KMLGenerator()
		kml.add_folders('first', 'second')
		self.assertEqual(kml.folders.keys(), ['first', 'second'])

	def test__update_kwargs(self):
		fn = KMLGenerator._update_kwargs
		args = {}
		fn('folder', args)
		self.assertEqual(args['style'], '#folder')
		args = {'style': 'test'}
		fn('folder', args)
		self.assertEqual(args['style'], 'test')
		args = {'style': 0}
		fn('folder', args)
		self.assertEqual(args['style'], '#placemark-pink')
		args = {'style': '0'}
		fn('folder', args)
		self.assertEqual(args['style'], '#placemark-pink')

	def test_add_line(self):
		kml = KMLGenerator(line_template="{name} {color}")
		kml.add_folder('aFolder')
		from editolido import Route
		from editolido import GeoPoint
		route = Route([GeoPoint((0, 0)), GeoPoint((0, 90))], name="route")
		kml.add_line('aFolder', route, color="blouge")
		self.assertEqual(kml.folders['aFolder'][0], 'route blouge')

	def test_add_points(self):
		kml = KMLGenerator(point_template="{name}{color}")
		kml.add_folder('aFolder')
		from editolido import Route
		from editolido import GeoPoint
		route = Route([GeoPoint((0, 0)), GeoPoint((0, 90))], name="route")
		kml.add_points('aFolder', route, color="blouge")
		self.assertEqual(kml.folders['aFolder'][0], 'blouge\nblouge')

	def test_add_point(self):
		kml = KMLGenerator(point_template="{name} {color}")
		kml.add_folder('aFolder')
		from editolido import GeoPoint
		kml.add_point('aFolder', GeoPoint((0, 0), name="P1"), color="blouge")
		self.assertEqual(kml.folders['aFolder'][0], 'P1 blouge')

	def test_render(self):
		kml = KMLGenerator(folder_template="{name} {open} {content}",
		                   point_template="{name} {color}",
		                   template="{folders} {name} {extra}")
		kml.add_folder('aFolder')
		from editolido import GeoPoint
		kml.add_point('aFolder', GeoPoint((0, 0), name="P1"), color="blouge")
		self.assertEqual(kml.render(extra="what else ?", name='no name'),
		                 'aFolder 1 P1 blouge no name what else ?')

	def test_render_folder(self):
		kml = KMLGenerator(folder_template="{name} {open} {content}",
		                   point_template="{name} {color}")
		kml.add_folder('aFolder')
		from editolido import GeoPoint
		kml.add_point('aFolder', GeoPoint((0, 0), name="P1"), color="blouge")
		self.assertEqual(kml.render_folder('aFolder'), 'aFolder 1 P1 blouge')

	def test_render_folders(self):
		kml = KMLGenerator(folder_template="{name} {open} {content}",
		                   point_template="{name} {color}")
		kml.add_folders('aFolder', 'another')
		from editolido import GeoPoint
		kml.add_point('aFolder', GeoPoint((0, 0), name="P1"), color="blouge")
		kml.add_point('another', GeoPoint((0, 0), name="P2"), color="red")
		self.assertEqual(kml.render_folders(),
		                 'aFolder 1 P1 blouge\nanother 1 P2 red')
