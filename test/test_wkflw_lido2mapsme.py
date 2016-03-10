# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from unittest import TestCase
from editolido.workflows.editorial.workflow import Workflow


class TestLido2Mapsme(TestCase):
	def test_no_error(self):
		workflow = Workflow("KJFK-LFPG 27Mar2015 05:45z.txt")
		from editolido.workflows import lido2mapsme
		output = lido2mapsme(workflow.get_input(), workflow.get_parameters())
		self.assertTrue(output)
