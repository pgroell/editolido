# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from editolido.constants import NAT_POSITION_ENTRY, PIN_NONE
from editolido.geoindex import GeoGridIndex
from editolido.geolite import km_to_rad, rad_to_km
from editolido.geopoint import GeoPoint
from editolido.kml import KMLGenerator
from editolido.ofp import OFP
from editolido.route import Route


def lido2mapsme(action_in, params):
	ofp = OFP(action_in)
	kml = KMLGenerator()

	kml.add_folders('greatcircle', 'ogimet', 'rnat', 'rmain')
	route_name = "{departure}-{destination}".format(**ofp.infos)
	route = Route(ofp.wpt_coordinates,
	              name=route_name,
	              description=ofp.description)

	natmarks = []
	if params['Afficher NAT']:
		index = 0 if params['Position repère'] == NAT_POSITION_ENTRY else -1
		for track in ofp.tracks:
			kml.add_line('rnat', track)
			if params['Repère NAT'] != PIN_NONE:
				p = GeoPoint(track[index], name=track.name,
				             description=track.description)
				natmarks.append(p)
				kml.add_point('rnat', p, style=params['Repère NAT'])

	if params['Afficher Ortho']:
		greatcircle = Route((route[0], route[-1])).split(300)
		greatcircle.name = "Ortho %s" % route_name
		kml.add_line('greatcircle', greatcircle)

	kml.add_line('rmain', route)
	if params['Point Route'] != PIN_NONE:
		kml.add_points('rmain', route,
		               excluded=natmarks, style=params['Point Route'])

	if params['Afficher Ogimet']:
		wmo_grid = GeoGridIndex()
		wmo_grid.load()
		start = route[0]
		end = route[-1]
		#d = start.distance_to(end, converter=rad_to_km)

		def build_ogimet(default_step):
			ogimet_sites = [start.name]
			previous = start
			ogimet_points = [start]
			sid = True
			for i, p in enumerate(route.split(60, converter=km_to_rad, preserve=True)):
				if i == 0:
					continue
				neighbours = sorted(
					wmo_grid.get_nearest_points(p, 30, converter=km_to_rad),
					key=lambda t: t[1])
				if neighbours:
					point, d = neighbours[0]
					if sid and point.distance_to(start, converter=rad_to_km) < 500:
						step = min(60, default_step)
					else:
						sid = False
						step = default_step
					if point.name not in ogimet_sites and previous.distance_to(
					        point, converter=rad_to_km) > step:
						previous = point
						ogimet_points.append(point)
						ogimet_sites.append(point.name)
			ogimet_points[-1] = end
			return ogimet_points
		step = start.distance_to(end, converter=rad_to_km) / 200
		ogimet_points = []
		while True:
			ogimet_points = build_ogimet(step)
			if len(ogimet_points) < 23:
				break
			ogimet_sites = [p.name for p in ogimet_points]
			print 'Route Ogimet (%s): %s' % (len(ogimet_sites), '_'.join(ogimet_sites))
			step *= 2
		ogimet_sites = [p.name for p in ogimet_points]
		# clipboard.set('_'.join(ogimet_sites))
		print 'Route Ogimet (%s): %s' % (len(ogimet_sites), '_'.join(ogimet_sites))
		ortho_ogimet = Route(ogimet_points).split(300, preserve=True)
		kml.add_line('ogimet', ortho_ogimet)

	return kml.render(
		name=ofp.description,
		nat_color=params['Couleur NAT'] or '60DA25A8',
		ogimet_color=params['Couleur Ogimet'] or '50FF0000',
		greatcircle_color=params['Couleur Ortho'] or '5F1478FF',
		route_color=params['Couleur Route'] or 'FFDA25A8'
	)
