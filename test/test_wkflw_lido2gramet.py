# -*- coding: utf-8 -*-
from __future__ import unicode_literals, print_function
from editolido.workflows.lido2gramet import lido2gramet


def test_lido2gramet_output_is_kml(ofp_text):
    output = lido2gramet(
        ofp_text, {'Générer KML' : True}, debug=False)
    assert '<kml ' in output

