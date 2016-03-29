# -*- coding: utf-8 -*-
from __future__ import unicode_literals, print_function

from unittest import TestCase
from editolido.workflows.editorial.workflow import Workflow
from editolido.workflows.lido2gramet import lido2gramet


class TestLido2gramet(TestCase):
    def setUp(self):
        self.debug = False
        self.parameters = {'Générer KML' : True}

    def test_no_error1(self):
        workflow = Workflow("KJFK-LFPG 27Mar2015 05:45z.txt")
        output = lido2gramet(
            workflow.get_input(), self.parameters, debug=self.debug)
        self.assertTrue('<kml ' in output)

    def test_no_error2(self):
        workflow = Workflow("AF007_KJFK-LFPG_13Mar2016_00:15z_OFP_6_0_1.txt")
        output = lido2gramet(
            workflow.get_input(), self.parameters, debug=self.debug)
        self.assertTrue('<kml ' in output)

    def test_new_nat_format(self):
        workflow = Workflow("AF009_KJFK-LFPG_18Mar2016_04:55z_OFP_12_0_1.txt")
        output = lido2gramet(
            workflow.get_input(), self.parameters, debug=self.debug)
        self.assertTrue('<kml ' in output)

    def test_AF011_22Mar2016(self):
        workflow = Workflow("AF011_KJFK-LFPG_22Mar2016_02:45z_OFP_8_0_1.txt")
        output = lido2gramet(
            workflow.get_input(), self.parameters, debug=self.debug)
        self.assertTrue('<kml ' in output)

    def test_AF1753_28Mar2016(self):
        workflow = Workflow("AF1753_UKBB-LFPG_28Mar2016_12:15z_OFP13.txt")
        output = lido2gramet(
            workflow.get_input(), self.parameters, debug=self.debug)
        self.assertTrue('<kml ' in output)