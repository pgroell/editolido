# -*- coding: utf-8 -*-
from __future__ import unicode_literals, print_function

import pytest

from editolido.workflows.editorial.workflow import Workflow
from editolido.workflows.lido2gramet import lido2gramet

from editolido.utils import get_ofp_testfiles

@pytest.mark.parametrize('datafile', get_ofp_testfiles())
def test_output_is_kml(datafile):
    workflow = Workflow(datafile)
    output = lido2gramet(
        workflow.get_input(), {'Générer KML' : True}, debug=False)
    assert '<kml ' in output

