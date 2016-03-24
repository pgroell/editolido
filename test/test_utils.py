# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from StringIO import StringIO
import shutil
import tempfile
from unittest import TestCase

import sys


class TestUtils(TestCase):
    def setUp(self):
        # Create a temporary directory
        self.test_dir = tempfile.mkdtemp()

    def tearDown(self):
        # Remove the directory after the test
        shutil.rmtree(self.test_dir)

    def test_reload_editolido(self):
        from editolido.utils import reload_editolido
        reload_editolido(self.test_dir)

    def test_update_editolido_bad_url(self):
        from editolido.utils import update_editolido
        output = StringIO()
        out = sys.stdout
        try:
            sys.stdout = output
            update_editolido(self.test_dir, fake=True)
        finally:
            sys.stdout = out
            self.assertIn('invalid url', output.getvalue())
            output.close()

    def test_update_editolido(self):
        from editolido.utils import update_editolido
        output = StringIO()
        out = sys.stdout
        try:
            sys.stdout = output
            url = "https://github.com/flyingeek/editolido/archive/1.0.0b7.zip"
            update_editolido(self.test_dir, url=url, fake=True)
        finally:
            sys.stdout = out
            self.assertIn('latest remote version is 1.0.0b7', output.getvalue())
            output.close()

    def test_update_editolido_using_branch(self):
        from editolido.utils import update_editolido
        output = StringIO()
        out = sys.stdout
        try:
            sys.stdout = output
            url = "https://github.com/flyingeek/editolido/archive/master.zip"
            update_editolido(self.test_dir, url=url, name='editolido',
                             fake=True)
        finally:
            sys.stdout = out
            self.assertIn('latest remote version is master', output.getvalue())
            output.close()
