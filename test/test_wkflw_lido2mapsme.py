# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from unittest import TestCase
from editolido.workflows.editorial.workflow import Workflow
from editolido.workflows.lido2mapsme import lido2mapsme


class TestLido2Mapsme(TestCase):
	def test_no_error1(self):
		workflow = Workflow("KJFK-LFPG 27Mar2015 05:45z.txt")
		output = lido2mapsme(
			workflow.get_input(), workflow.get_parameters(), debug=True)
		self.assertTrue(output)

	def test_no_error2(self):
		workflow = Workflow("AF007_KJFK-LFPG_13Mar2016_00:15z_OFP_6_0_1.txt")
		output = lido2mapsme(
			workflow.get_input(), workflow.get_parameters(), debug=True)
		self.assertTrue(output)
