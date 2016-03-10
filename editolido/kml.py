# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import os
from collections import OrderedDict
from editolido.workflows import PINS


class KMLGenerator(object):
	def __init__(self, template=None, point_template=None, line_template=None,
	             folder_template=None):
		datadir = os.path.join(
			os.path.dirname(os.path.abspath(__file__)), 'data')
		self.template = template
		if template is None:
			with open(os.path.join(datadir, 'mapsme_template.kml')) as f:
				self.template = f.read()
		self.point_template = point_template
		if point_template is None:
			with open(os.path.join(datadir, 'mapsme_point_tpl.kml')) as f:
				self.point_template = f.read()
		self.line_template = line_template
		if line_template is None:
			with open(os.path.join(datadir, 'mapsme_line_tpl.kml')) as f:
				self.line_template = f.read()
		self.folder_template = folder_template
		if folder_template is None:
			with open(os.path.join(datadir, 'mapsme_folder_tpl.kml')) as f:
				self.folder_template = f.read()
		self.folders = OrderedDict()

	def add_folder(self, name):
		self.folders[name] = []

	def add_folders(self, *names):
		for name in names:
			self.add_folder(name)

	@staticmethod
	def _update_kwargs(folder, kwargs):
		"""
		Apply style value based on context
		- if style is not set, uses folder name
		- if style is integer, replace with the style's name
		:param folder: str
		:param kwargs: list
		"""
		style = kwargs.get('style', None)
		if style is None:
			kwargs['style'] = '#' + folder
		elif isinstance(style, int):
			kwargs['style'] = PINS[style]

	def add_line(self, folder, route, **kwargs):
		"""
		Add a route as a LineString in the .kml
		:param folder: folder name
		:param route: Route
		:param kwargs: optional args passed to the renderer
		"""
		self._update_kwargs(folder, kwargs)
		self.folders[folder].append(
			route.as_kml_line(self.line_template, **kwargs))

	def add_points(self, folder, route, **kwargs):
		"""
		Add a route as a Points in the .kml
		:param folder: folder name
		:param route: Route
		:param kwargs: optional args passed to the renderer
		"""
		self._update_kwargs(folder, kwargs)
		self.folders[folder].append(
			route.as_kml_points(self.point_template, **kwargs))

	def add_point(self, folder, geopoint, **kwargs):
		"""
		Add a GeoPoint in the .kml
		:param folder: folder name
		:param geopoint: GeoPoint
		:param kwargs: optional args passed to the renderer
		"""
		self._update_kwargs(folder, kwargs)
		self.folders[folder].append(
			geopoint.as_kml(self.point_template, **kwargs))

	def render(self, **kwargs):
		return self.template.format(
			folders=self.render_folders(),
			**kwargs
		)

	def render_folder(self, folder):
		"""
		Render a folder content
		:param folder:
		:return: str
		"""
		return self.folder_template.format(
			name=folder,
			open=1,
			content='\n'.join(self.folders[folder]),
		)

	def render_folders(self):
		"""
		Render all folders
		:return: str
		"""
		return '\n'.join(
			[self.render_folder(folder) for folder in self.folders.iterkeys()])
