# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import shutil
import tempfile
from distutils.version import StrictVersion
from unittest import TestCase
import mock


class TestCore(TestCase):

    def test_raw_content_url(self):
        from editolido.core import raw_content_url
        self.assertEqual(
            raw_content_url(
                'https://github.com/flyingeek/editolido/archive/1.0.0b7.zip'),
            'https://raw.githubusercontent.com/flyingeek/editolido/master'
            '/editolido/bootstrap_editorial.py'
        )
        self.assertEqual(
            raw_content_url(
                'https://github.com/flyingeek/editolido/archive/mybranch.zip',
                'test.json'),
            'https://raw.githubusercontent.com/flyingeek/editolido/mybranch'
            '/editolido/test.json'
        )
        self.assertEqual(
            raw_content_url(
                'https://github.com/another/editolido2/archive/mybranch.zip'),
            'https://raw.githubusercontent.com/another/editolido2/mybranch'
            '/editolido2/bootstrap_editorial.py'
        )

    @mock.patch('editolido.core.logger')
    def test_raw_content_url_using_latest(self, logger):
        from editolido.core import raw_content_url
        self.assertEqual(
            raw_content_url(''),
            'https://raw.githubusercontent.com/flyingeek/editolido/master'
            '/editolido/bootstrap_editorial.py'
        )
        logger.info.assert_not_called()

    @mock.patch('editolido.core.logger')
    def test_raw_content_url_default(self, logger):
        from editolido.core import raw_content_url
        self.assertEqual(
            raw_content_url('blabla'),
            'https://raw.githubusercontent.com/flyingeek/editolido/master'
            '/editolido/bootstrap_editorial.py'
        )
        logger.info.assert_called_with('using default bootstrap url')

    @mock.patch('editolido.core.logger')
    def test_get_latest_version_infos_404(self, logger):
        from editolido.core import get_latest_version_infos
        import requests
        with self.assertRaises(requests.exceptions.RequestException):
            get_latest_version_infos(
                'https://github.com/flyingeek/editolido/archive/1.0.0b7.zip',
                'doesnotexists'
            )
        logger.error.assert_called_with('status code 404')

    @mock.patch('editolido.core.logger')
    def test_get_latest_version_infos(self, logger):
        from editolido.core import get_latest_version_infos
        from editolido.bootstrap_editorial import VERSION
        url = 'https://github.com/flyingeek/editolido/archive/{0}.zip'.format(
            VERSION)
        get_latest_version_infos(url)
        self.assertTrue(logger.info.called)
        self.assertFalse(logger.error.called)

    def test_needs_update_to_same_version(self):
        from editolido.core import needs_update, infos_from_giturl
        loc = infos_from_giturl(
            'https://github.com/flyingeek/editolido/archive/1.0.0b7.zip')
        rem = infos_from_giturl(
            'https://github.com/flyingeek/editolido/archive/1.0.0b7.zip')
        self.assertFalse(needs_update(loc, rem))

    def test_needs_update_to_same_version_another_owner(self):
        from editolido.core import needs_update, infos_from_giturl
        loc = infos_from_giturl(
            'https://github.com/flyingeek/editolido/archive/1.0.0b7.zip')
        rem = infos_from_giturl(
            'https://github.com/eric/editolido/archive/1.0.0b7.zip')
        self.assertTrue(needs_update(loc, rem))

    def test_needs_update_to_lower_version(self):
        from editolido.core import needs_update, infos_from_giturl
        loc = infos_from_giturl(
            'https://github.com/flyingeek/editolido/archive/1.0.0b7.zip')
        rem = infos_from_giturl(
            'https://github.com/flyingeek/editolido/archive/1.0.0b6.zip')
        self.assertFalse(needs_update(loc, rem))

    def test_needs_update_to_greater_version(self):
        from editolido.core import needs_update, infos_from_giturl
        loc = infos_from_giturl(
            'https://github.com/flyingeek/editolido/archive/1.0.0b7.zip')
        rem = infos_from_giturl(
            'https://github.com/flyingeek/editolido/archive/1.0.0b8.zip')
        self.assertTrue(needs_update(loc, rem))

    def test_needs_update_to_branch(self):
        from editolido.core import needs_update, infos_from_giturl
        loc = infos_from_giturl(
            'https://github.com/flyingeek/editolido/archive/1.0.0b7.zip')
        rem = infos_from_giturl(
            'https://github.com/flyingeek/editolido/archive/master.zip')
        self.assertTrue(needs_update(loc, rem))

    def test_needs_update_from_branch(self):
        from editolido.core import needs_update, infos_from_giturl
        loc = infos_from_giturl(
            'https://github.com/flyingeek/editolido/archive/master.zip')
        rem = infos_from_giturl(
            'https://github.com/flyingeek/editolido/archive/1.0.0b7.zip')
        self.assertTrue(needs_update(loc, rem))

    def test_needs_update_to_same_branch(self):
        from editolido.core import needs_update, infos_from_giturl
        loc = infos_from_giturl(
            'https://github.com/flyingeek/editolido/archive/master.zip')
        rem = infos_from_giturl(
            'https://github.com/flyingeek/editolido/archive/master.zip')
        self.assertFalse(needs_update(loc, rem))

    def test_needs_update_to_other_branch(self):
        from editolido.core import needs_update, infos_from_giturl
        loc = infos_from_giturl(
            'https://github.com/flyingeek/editolido/archive/master.zip')
        rem = infos_from_giturl(
            'https://github.com/flyingeek/editolido/archive/another.zip')
        self.assertTrue(needs_update(loc, rem))

    def test_read_local_config_utf8(self):
        from editolido.core import read_local_config
        json = b'{"test": "éè"}'
        with mock.patch('editolido.core.open',
                        mock.mock_open(read_data=json), create=True) as m:
            data = read_local_config()
        self.assertTrue(m.called)
        self.assertEqual(data['test'], 'éè')

    def test_read_local_config_null_version(self):
        from editolido.core import read_local_config
        json = b'{"version": null}'
        with mock.patch('editolido.core.open',
                        mock.mock_open(read_data=json), create=True) as m:
            data = read_local_config()
        self.assertTrue(m.called)
        self.assertIs(data['version'], None)

    def test_read_local_config_strictversion(self):
        from editolido.core import read_local_config
        json = b'{"version": "1.0b7"}'
        with mock.patch('editolido.core.open',
                        mock.mock_open(read_data=json), create=True) as m:
            data = read_local_config()
        self.assertTrue(m.called)
        self.assertEqual(data['version'], StrictVersion('1.0.0b7'))


class TestCoreUpdate(TestCase):
    def setUp(self):
        # Create a temporary directory
        self.test_dir = tempfile.mkdtemp()

        def clean_dir():
            shutil.rmtree(self.test_dir)
        self.addCleanup(clean_dir)

        patcher1 = mock.patch('editolido.core.get_install_dir')
        self.get_install_dir = patcher1.start()
        self.get_install_dir.return_value = self.test_dir
        self.addCleanup(patcher1.stop)
        patcher2 = mock.patch('editolido.core.download_package')
        self.download_package = patcher2.start()
        self.addCleanup(patcher2.stop)
        patcher3 = mock.patch('editolido.core.get_latest_version_infos')
        self.json = patcher3.start()
        self.addCleanup(patcher3.stop)
        patcher4 = mock.patch('editolido.core.save_local_config')
        self.cfg = patcher4.start()
        self.addCleanup(patcher4.stop)

    def test_get_install_dir(self):
        from editolido.core import get_install_dir
        self.assertEqual(get_install_dir(), self.test_dir)

    def test_reload_editolido(self):
        from editolido.core import reload_editolido
        reload_editolido(self.test_dir)

    @mock.patch('editolido.core.logger')
    def test_update_editolido_empty_url(self, logger):
        from editolido.core import update_editolido
        self.json.return_value = dict(
            version='1.0.0b7',
            url='https://github.com/flyingeek/editolido/archive/1.0.0b7.zip')
        update_editolido('')
        self.download_package.assert_not_called()  # up to date
        logger.error.assert_not_called()
        self.json.return_value = dict(
            version='99.99.99',
            url='https://github.com/flyingeek/editolido/archive/99.99.99.zip')
        update_editolido('')
        self.assertTrue(self.download_package.called)
        logger.error.assert_not_called()

    @mock.patch('editolido.core.logger')
    def test_update_editolido_bad_url(self, logger):
        from editolido.core import update_editolido
        self.json.return_value = dict(
            version='1.0.0b7',
            url='https://github.com/flyingeek/editolido/archive/1.0.0b7.zip')
        update_editolido('http://www.example.com')
        self.download_package.assert_not_called()
        logger.error.assert_called_with('invalid url http://www.example.com')

    @mock.patch('editolido.core.logger')
    def test_update_editolido(self, logger):
        from editolido.core import update_editolido
        from editolido.bootstrap_editorial import VERSION
        self.json.return_value = dict(
            version='1.0.0b7',
            url='https://github.com/flyingeek/editolido/archive/1.0.0b7.zip')
        url = "https://github.com/flyingeek/editolido/archive/1.0.0b7.zip"
        update_editolido(url)
        expected = [
            mock.call('remote version: 1.0.0b7'),
            mock.call('remote zipball url: https://github.com/flyingeek'
                      '/editolido/archive/1.0.0b7.zip'),
            mock.call('local version {0} up to date'.format(VERSION)), ]
        self.assertTrue(logger.info.mock_calls == expected)
        self.download_package.assert_not_called()

    @mock.patch('editolido.core.read_local_config')
    @mock.patch('editolido.bootstrap_editorial.workflow')
    @mock.patch('editolido.core.logger')
    def test_update_editolido_using_branch(self, logger, workflow, cfg):
        from editolido.core import update_editolido, infos_from_giturl
        from editolido.bootstrap_editorial import VERSION, AUTO_UPDATE_KEY
        workflow.get_parameters.return_value = {AUTO_UPDATE_KEY: False}
        url = "https://github.com/flyingeek/editolido/archive/master.zip"
        cfg.return_value = infos_from_giturl(url)
        self.json.return_value = dict(
            version='1.0.0b7',
            url='https://github.com/flyingeek/editolido/archive/1.0.0b7.zip')
        update_editolido(url)
        expected = [
            mock.call(u'auto update is disabled'),
            mock.call('remote version: master'),
            mock.call('remote zipball url: https://github.com/flyingeek'
                      '/editolido/archive/master.zip'),
            mock.call('local version is {0}'.format(VERSION)),
            mock.call('local branch status unknown, [master] expected')]
        self.assertEqual(logger.info.mock_calls, expected)
        self.download_package.assert_not_called()

    @mock.patch('editolido.core.read_local_config')
    @mock.patch('editolido.core.logger')
    def test_update_editolido_bad_json(self, logger, cfg):
        from editolido.core import update_editolido, infos_from_giturl
        from editolido.bootstrap_editorial import VERSION
        call = mock.call
        self.json.return_value = dict(
            version='invalid',
            url='https://github.com/flyingeek/editolido/archive/invalid.zip')
        url = "https://github.com/flyingeek/editolido/archive/1.0.0b6.zip"
        cfg.return_value = infos_from_giturl(
            "https://github.com/flyingeek/editolido/archive/1.0.0b7.zip")
        update_editolido(url)
        self.assertIn('json rejected', repr(logger.error.call_args))
        expected = [
            call('remote version: 1.0.0b6'),
            call('remote zipball url: https://github.com/flyingeek'
                 '/editolido/archive/1.0.0b6.zip'),
            call(u'local version %s up to date' % VERSION)]
        self.assertEqual(logger.info.mock_calls, expected)
        self.download_package.assert_not_called()

    @mock.patch('editolido.core.read_local_config')
    @mock.patch('editolido.core.logger')
    def test_update_editolido_params_greater_json(self, logger, cfg):
        from editolido.core import update_editolido, infos_from_giturl
        self.json.return_value = dict(
            version='1.0.0b7',
            url='https://github.com/flyingeek/editolido/archive/1.0.0b7.zip')
        url = "https://github.com/flyingeek/editolido/archive/1.0.0b8.zip"
        cfg.return_value(infos_from_giturl(
            'https://github.com/flyingeek/editolido/archive/1.0.0b7.zip'))
        update_editolido(url)
        logger.info.assert_any_call('remote version: 1.0.0b8')
        self.assertTrue(self.download_package.called)

    @mock.patch('editolido.core.read_local_config')
    @mock.patch('editolido.core.logger')
    def test_update_editolido_json_greater_params(self, logger, cfg):
        from editolido.core import update_editolido, infos_from_giturl
        self.json.return_value = dict(
            version='1.0.0b8',
            url='https://github.com/flyingeek/editolido/archive/1.0.0b8.zip')
        url = "https://github.com/flyingeek/editolido/archive/1.0.0b7.zip"
        cfg.return_value(infos_from_giturl(url))
        update_editolido(url)
        logger.info.assert_any_call('remote version: 1.0.0b8')
        self.assertTrue(self.download_package.called)

    @mock.patch('editolido.bootstrap_editorial.workflow')
    @mock.patch('editolido.core.logger')
    def test_update_editolido_update_logic(self, logger, workflow):
        from editolido.bootstrap_editorial import VERSION, AUTO_UPDATE_KEY
        from editolido.core import update_editolido
        workflow.get_parameters.return_value = {AUTO_UPDATE_KEY: True}
        self.json.return_value = dict(
            version='99.99.99',
            url='https://github.com/flyingeek/editolido/archive/99.99.99.zip')
        url = "https://github.com/flyingeek/editolido/archive/1.0.0b7.zip"
        update_editolido(url)
        # install from remote when greater than current
        logger.info.assert_any_call('editolido module %s installed' % VERSION)
        self.assertTrue(self.download_package.called)
        self.download_package.reset_mock()
        logger.reset_mock()

        self.json.return_value = dict(
            version=VERSION,
            url='https://github.com/flyingeek/editolido/archive/%s.zip'
                % VERSION)
        url = "https://github.com/flyingeek/editolido/archive/%s.zip" % VERSION
        update_editolido(url)
        # consider up to date if same version
        logger.info.assert_any_call('local version %s up to date' % VERSION)
        self.download_package.assert_not_called()
        self.download_package.reset_mock()
        logger.reset_mock()

        url = "https://github.com/flyingeek/editolido/archive/99.99.99.zip"
        update_editolido(url)
        # update from URL if bigger than current
        logger.info.assert_any_call('editolido module %s installed' % VERSION)
        self.assertTrue(self.download_package.called)
        self.download_package.reset_mock()
        logger.reset_mock()

        self.json.return_value = dict(
            version=VERSION,
            url="https://github.com/flyingeek/editolido/archive/%s.zip"
                % VERSION)
        url = "https://github.com/flyingeek/editolido/archive/master.zip"
        update_editolido(url)
        # update if branch in URL
        logger.info.assert_any_call('editolido [master] %s installed'
                                    % VERSION)
        self.assertTrue(self.download_package.called)
        self.download_package.reset_mock()
        logger.reset_mock()

    @mock.patch('editolido.bootstrap_editorial.workflow')
    @mock.patch('editolido.core.logger')
    def test_update_editolido_update_logic_not_auto(self, logger, workflow):
        from editolido.core import update_editolido
        from editolido.bootstrap_editorial import VERSION, AUTO_UPDATE_KEY
        workflow.get_parameters.return_value = {AUTO_UPDATE_KEY: False}
        self.json.return_value = dict(
            version='99.99.99',
            url="https://github.com/flyingeek/editolido/archive/99.99.99.zip")
        url = "https://github.com/flyingeek/editolido/archive/{0}.zip"\
            .format(VERSION)
        update_editolido(url)
        # does not install current version
        self.download_package.assert_not_called()
        self.download_package.reset_mock()
        logger.reset_mock()

        url = "https://github.com/flyingeek/editolido/archive/99.99.99.zip"
        update_editolido(url)
        # install bigger version if in URL
        logger.info.assert_any_call('editolido module %s installed' % VERSION)
        self.assertTrue(self.download_package.called)
        self.download_package.reset_mock()
        logger.reset_mock()

    @mock.patch('editolido.core.read_local_config')
    @mock.patch('editolido.bootstrap_editorial.workflow')
    @mock.patch('editolido.core.logger')
    def test_update_lido_logic_not_auto_same_branch(
            self, logger, workflow, cfg):
        from editolido.core import update_editolido, infos_from_giturl
        from editolido.bootstrap_editorial import AUTO_UPDATE_KEY
        workflow.get_parameters.return_value = {AUTO_UPDATE_KEY: False}
        url = "https://github.com/flyingeek/editolido/archive/master.zip"
        cfg.return_value = infos_from_giturl(url)
        update_editolido(url)
        # branch are installed only when auto-update is on
        self.download_package.assert_not_called()
        logger.error.assert_not_called()

    @mock.patch('editolido.core.read_local_config')
    @mock.patch('editolido.bootstrap_editorial.workflow')
    @mock.patch('editolido.core.logger', create=False)
    def test_update_lido_logic_not_auto_tag_to_branch(
            self, logger, workflow, cfg):
        from editolido.core import update_editolido, infos_from_giturl
        from editolido.bootstrap_editorial import AUTO_UPDATE_KEY
        workflow.get_parameters.return_value = {AUTO_UPDATE_KEY: False}
        url = "https://github.com/flyingeek/editolido/archive/master.zip"
        cfg.return_value = infos_from_giturl(
            "https://github.com/flyingeek/editolido/archive/1.0.0b7.zip")
        update_editolido(url)
        # even with auto off upgrade to branch if not on same branch
        self.assertTrue(self.download_package.called)
        logger.error.assert_not_called()

    @mock.patch('editolido.core.read_local_config')
    @mock.patch('editolido.bootstrap_editorial.workflow')
    @mock.patch('editolido.core.logger', create=False)
    def test_update_lido_logic_auto_same_branch(
            self, logger, workflow, cfg):
        from editolido.core import update_editolido, infos_from_giturl
        from editolido.bootstrap_editorial import AUTO_UPDATE_KEY
        workflow.get_parameters.return_value = {AUTO_UPDATE_KEY: True}
        url = "https://github.com/flyingeek/editolido/archive/master.zip"
        cfg.return_value = infos_from_giturl(url)
        update_editolido(url)
        # branch are installed only when auto-update is on
        self.assertTrue(self.download_package.called)
        logger.error.assert_not_called()
