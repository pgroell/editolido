# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from editolido import OFP, Route, GeoPoint
from editolido.constants import NAT_POSITION_ENTRY, PIN_NONE
from editolido.kml import KMLGenerator


def lido2mapsme(action_in, params):
	ofp = OFP(action_in)
	kml = KMLGenerator()

	kml.add_folders('greatcircle', 'ogimet', 'rnat', 'rmain')
	route_name = "{departure}-{destination}".format(**ofp.infos)
	route = Route(ofp.wpt_coordinates,
	              name=route_name,
	              description=ofp.description)

	natmarks = []
	if params['Couleur NAT']:
		index = 0 if params['Position repère'] == NAT_POSITION_ENTRY else -1
		for track in ofp.tracks:
			kml.add_line('rnat', track)
			if params['Repère NAT'] != PIN_NONE:
				p = GeoPoint(track[index], name=track.name,
				             description=track.description)
				natmarks.append(p)
				kml.add_point('rnat', p, style=params['Repère NAT'])

	if params['Couleur Ortho']:
		greatcircle = Route((route[0], route[-1])).split(300)
		greatcircle.name = "Ortho %s" % route_name
		kml.add_line('greatcircle', greatcircle)

	if params['Couleur Route']:
		kml.add_line('rmain', route)

	if params['Point Route'] != PIN_NONE:
		kml.add_points('rmain', route,
		               excluded=natmarks, style=params['Point Route'])

	return kml.render(
		name=ofp.description,
		nat_color=params['Couleur NAT'],
		ogimet_color=params['Couleur Ogimet'],
		greatcircle_color=params['Couleur Ortho'],
		route_color=params['Couleur Route']
	)
