# -*- coding: utf-8 -*-
from __future__ import unicode_literals


def lido2mapsme(action_in, params, debug=False):
    """
    Lido2Mapsme KML rendering action
    :param action_in: unicode action input
    :param params: dict action's parameters
    :param debug: bool determines wether or not to print ogimet debug messages
    :return:
    """
    from editolido.constants import NAT_POSITION_ENTRY, PIN_NONE, PIN_PINK
    from editolido.geopoint import GeoPoint
    from editolido.kml import KMLGenerator
    from editolido.ofp import OFP
    from editolido.route import Route
    from editolido.ogimet import ogimet_route
    ofp = OFP(action_in)
    kml = KMLGenerator()

    kml.add_folders('greatcircle', 'ogimet', 'rnat', 'ralt', 'rmain')
    route_name = "{departure}-{destination}".format(**ofp.infos)
    route = Route(ofp.wpt_coordinates,
                  name=route_name,
                  description=ofp.description)

    natmarks = []
    if params['Afficher NAT']:
        index = 0 if params['Position repère'] == NAT_POSITION_ENTRY else -1
        for track in ofp.tracks:
            if track:
                kml.add_line('rnat', track)
                if params['Repère NAT'] != PIN_NONE:
                    p = GeoPoint(track[index], name=track.name,
                                 description=track.description)
                    natmarks.append(p)
                    kml.add_point('rnat', p, style=params['Repère NAT'])
            else:
                print "empty track found %s" % track.name

    if params['Afficher Ortho']:
        greatcircle = Route((route[0], route[-1])).split(300)
        greatcircle.name = "Ortho %s" % route_name
        kml.add_line('greatcircle', greatcircle)

    kml.add_line('rmain', route)
    if params['Point Route'] != PIN_NONE:
        kml.add_points('rmain', route,
                       excluded=natmarks, style=params['Point Route'])

    if params.get('Afficher Dégagement', False):
        alt_route = Route(ofp.wpt_coordinates_alternate,
                          name="Route Dégagement")
        kml.add_line('ralt', alt_route)
        if params.get('Point Dégagement', PIN_NONE) != PIN_NONE:
            kml.add_points(
                'ralt', alt_route,
                excluded=[alt_route.route[0]] if alt_route.route else [],
                style=params.get('Point Dégagement', PIN_PINK))

    if params['Afficher Ogimet']:
        kml.add_line('ogimet', ogimet_route(route, debug=debug))

    return kml.render(
        name=ofp.description,
        rnat_color=params['Couleur NAT'] or '60DA25A8',
        ogimet_color=params['Couleur Ogimet'] or '50FF0000',
        greatcircle_color=params['Couleur Ortho'] or '5F1478FF',
        rmain_color=params['Couleur Route'] or 'FFDA25A8',
        ralt_color=params.get('Couleur Dégagement', 'FFFF00FF')
    )
