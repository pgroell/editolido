# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from unittest import TestCase

import pytest

from editolido.workflows.editorial.workflow import Workflow
from editolido.workflows.lido2mapsme import lido2mapsme
from editolido.utils import get_ofp_testfiles

@pytest.mark.parametrize('datafile', get_ofp_testfiles())
def test_output_is_kml(datafile):
    workflow = Workflow(datafile)
    output = lido2mapsme(
        workflow.get_input(), workflow.get_parameters(), debug=False)
    assert '<kml ' in output

