# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import os
from editolido.workflows.editorial.defaults import params


class Workflow(object):
    """
    Workflow Mock object
    """
    def __init__(self, input_filename=None, parameters=None):
        self.output = None
        self.input_filename = input_filename
        self.parameters = parameters if parameters is not None else params

    def get_parameters(self):
        return self.parameters

    def get_input(self):
        module_dir = os.path.dirname(
            os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        datadir = os.path.join(
            os.path.join(os.path.dirname(module_dir), 'test'), 'data')
        with open(os.path.join(datadir, self.input_filename), 'r') as f:
            action_in = f.read()
        return action_in

    def set_output(self, value):  # pragma: no cover
        self.output = value
