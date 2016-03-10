# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from unittest import TestCase


class TestLido2Mapsme(TestCase):
	def test_no_error(self):
		from editolido.workflows.lido2mapsme import workflow
		self.assertTrue(workflow.output)
