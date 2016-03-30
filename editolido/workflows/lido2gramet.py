# -*- coding: utf-8 -*-
from __future__ import unicode_literals, print_function
import requests


def get_sigmets_json():
    r = requests.get(
        'http://www.aviationweather.gov/gis/scripts/IsigmetJSON.php'
        '?type=all&bbox=-180,-90,180,90')
    return r.json() or {}


def add_sigmets(kml, folder, jsondata, pin):
    from editolido.geopoint import GeoPoint
    from editolido.route import Route
    from editolido.constants import PIN_NONE
    for d in jsondata['features']:
        props = d['properties']
        geom = d['geometry']
        name = "{firName}: {qualifier} {hazard}".format(**props)
        description = "{rawSigmet}".format(**props)
        if geom['type'] == 'LineString':
            geom['coordinates'] = [geom['coordinates']]
        if geom['type'] in ('Polygon', 'LineString'):
            for area in geom['coordinates']:
                route = Route(
                    [GeoPoint((lat, lon)) for lon, lat in area],
                    name=name,
                    description=description
                )
                kml.add_line(folder, route)
                if pin != PIN_NONE:
                    kml.add_point(
                        folder,
                        GeoPoint.get_center(
                            route,
                            name=name, description=description),
                        style=pin
                    )
        elif geom['type'] == 'Point':
            if pin != PIN_NONE:
                kml.add_point(
                    folder,
                    GeoPoint(
                        (geom['coordinates'][1], geom['coordinates'][0]),
                        name=name, description=description),
                    style=pin
                )
        else:
            print(d)
            print('unknown geometry type: %s' % geom['type'])
            raise ValueError


def lido2gramet(action_in, params=None, debug=False):
    """
     Puts the Ogimet/Gramet route in the clipboard
     Output kml route if params['Afficher Ogimet'] is True
    :param action_in: the OFP text
    :param params: workflow action parameters
    :param debug: bool switch to output debug info
    :return: unicode kml or None

    Usage from Editorial is:

    # -*- coding: utf-8 -*-
    from __future__ import unicode_literals
    import workflow
    from editolido.workflows.lido2gramet import lido2gramet


    params = workflow.get_parameters()
    action_in = workflow.get_input()
    workflow.set_output(lido2gramet(action_in, params=params))
    """
    import datetime
    import calendar
    import time
    from editolido.ofp import OFP, utc
    from editolido.kml import KMLGenerator
    from editolido.ogimet import ogimet_route
    from editolido.constants import PIN_ORANGE
    import re
    params = params or {}
    ofp = OFP(action_in)
    kml = KMLGenerator()
    ogimet_url = "http://www.ogimet.com/display_gramet.php?" \
                 "lang=en&hini={hini}&tref={tref}&hfin={hfin}&fl={fl}" \
                 "&hl=3000&aero=yes&wmo={wmo}&submit=submit"
    hini = 0
    hfin = ofp.infos['duration'].hour + 1
    taxitime = int(params.get('Temps de roulage', '') or '15')
    # timestamp for departure
    takeoff = ofp.infos['datetime'] + datetime.timedelta(minutes=taxitime)
    # http://stackoverflow.com/questions/15447632
    ts =  calendar.timegm(takeoff.timetuple())
    # http://stackoverflow.com/questions/13890935
    now_ts = int(time.time())
    tref = max(now_ts, ts)  # for old ofp timeref=now
    # average flight level
    levels = map(int, re.findall(r'F(\d{3})\s', ofp.raw_fpl_text()))
    if levels:
        fl = sum(levels)/float(len(levels))
        fl = 10 * int(fl /10)
    else:
        if debug:
            print('using default flight level')
        fl = 300
    route = ogimet_route(route = ofp.route, debug=debug, name="Ogimet Route")
    url = ogimet_url.format(
        hini=hini, tref=tref, hfin=hfin, fl=fl,
        wmo='_'.join([p.name for p in route if p.name]))
    try:
        # noinspection PyUnresolvedReferences
        import clipboard  # EDITORIAL module
        clipboard.set(url)
    except ImportError:
        pass
    if debug:
        print(url)
    if params.get('Générer KML', False):
        kml.add_folder('ogimet')
        kml.add_line('ogimet', route)
        tref_dt = datetime.datetime.fromtimestamp(tref, tz=utc)
        name = ("Route Gramet {flight} {departure}-{destination} "
                "{tref_dt:%d%b%Y %H:%M}z OFP {ofp}"
                .format(tref_dt=tref_dt, **ofp.infos))
        if params.get('Inclure SIGMETs', True):
            pin_sigmets = params.get('Label SIGMET', PIN_ORANGE)
            kml.add_folder('SIGMETs', pin=pin_sigmets)
            try:
                jsondata = get_sigmets_json() or {}
            except requests.exceptions.RequestException:
                pass
            else:
                try:
                    add_sigmets(kml, 'SIGMETs', jsondata, pin_sigmets)
                except ValueError:
                    pass
        return kml.render(
            name=name,
            ogimet_color=params.get('Couleur Ogimet', '') or '50FF0000',
            SIGMETs_color=params.get('Couleur SIGMET', '') or '50143CFA')
    return ''

