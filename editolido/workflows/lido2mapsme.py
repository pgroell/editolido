# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from editolido.constants import NAT_POSITION_ENTRY, PIN_NONE
from editolido.geopoint import GeoPoint
from editolido.kml import KMLGenerator
from editolido.ofp import OFP
from editolido.route import Route
from editolido.ogimet import ogimet_route


def lido2mapsme(action_in, params, debug=False):
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
        kml.add_line('ogimet', ogimet_route(route, debug=debug))

    return kml.render(
        name=ofp.description,
        nat_color=params['Couleur NAT'] or '60DA25A8',
        ogimet_color=params['Couleur Ogimet'] or '50FF0000',
        greatcircle_color=params['Couleur Ortho'] or '5F1478FF',
        route_color=params['Couleur Route'] or 'FFDA25A8'
    )
