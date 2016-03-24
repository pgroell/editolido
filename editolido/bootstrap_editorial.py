# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import os
import re
import requests
try:
    import workflow
except ImportError:
    from editolido.workflows.editorial.workflow import Workflow
    workflow = Workflow()


class _Logger(object):
    def __init__(self, threshold):
        self.threshold = threshold

    def log(self, message, level=0):
        if level or (self.threshold and self.threshold >= level):
            print message

    def info(self, message):
        self.log(message, 1)

    def error(self, message):
        self.log(message, 2)

logger = _Logger(workflow.get_parameters().get('Log', 2L))

try:
    import console
except ImportError:
    from editolido.workflows.editorial.console import Console
    console = Console(logger)


def download_package(github_url, zip_folder, install_dir, name="editolido",
                     timeout=None, fake=False):
    import shutil
    import zipfile
    from contextlib import closing
    from cStringIO import StringIO
    logger.info('downloading %s' % github_url)
    try:
        r = requests.get(github_url, verify=True, stream=True, timeout=timeout)
        r.raise_for_status()
        with closing(r), zipfile.ZipFile(StringIO(r.content)) as z:
            base = '%s/%s/' % (zip_folder, name)
            logger.info('extracting data')
            if not fake:
                z.extractall(
                    os.getcwd(),
                    filter(lambda m: m.startswith(base), z.namelist()))
    except requests.HTTPError:
        # noinspection PyUnboundLocalVariable
        logger.error('status code %s' % r.status_code)
    except requests.Timeout:
        logger.error('download timeout... aborting update')
    except requests.ConnectionError:
        logger.error('download connection error... aborting update')
    except requests.TooManyRedirects:
        logger.error('too many redirects... aborting update')
    except requests.exceptions.RequestException:
        logger.error('download fail... aborting update')
    else:
        logger.info('installing %s' % name)
        if not os.path.exists(install_dir):
            logger.info('print creating directory %s' % install_dir)
            os.makedirs(install_dir)
        dest = os.path.join(install_dir, name)
        try:
            if dest and name and os.path.exists(dest):
                shutil.rmtree(dest)
        except OSError:
            logger.error('could not remove %s' % dest)
            raise
        if zip_folder and not fake:
            shutil.move(os.path.join(zip_folder, name), install_dir)
            if not os.path.exists(os.path.join(install_dir, name)):
                logger.error('%s/%s directory missing' % (install_dir, name))
            logger.info('cleaning')
            try:
                shutil.rmtree(zip_folder)
            except OSError:
                logger.error('could not remove %s/%s'
                             % (os.getcwd(), zip_folder))
                raise


def tagname_from_url(url):
    pattern = re.compile(r'/([^/]+)\.zip')
    m = pattern.search(url)
    if m:
        return m.group(1)
    return False


def install_editolido(install_dir, boot_url=None, url=None, name='editolido',
                      fake=False):
    try:
        tagname = tagname_from_url(url)
        if tagname:
            download_package(
                url,
                '%s-%s' % (name, tagname),
                install_dir,
                name=name,
                fake=fake,
            )
        else:
            logger.error('invalid url %s' % url)
            raise IOError
    except (IOError, OSError):
        logger.error('install failed')
    else:
        try:
            # noinspection PyUnresolvedReferences
            import editolido
            reload(editolido)
        except ImportError:
            console.alert(
                'Module editolido manquant',
                "Assurez vous d'avoir une connexion internet et recommencez "
                "pour tenter un nouveau téléchargement",
                'OK',
                hide_cancel_button=True, )
            raise KeyboardInterrupt
        else:
            console.hud_alert(
                'module editolido %s installé' % editolido.__version__)
