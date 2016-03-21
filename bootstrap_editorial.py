# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import os
import requests


# This file is executed within a context:
EDITOLIDO = globals()['EDITOLIDO']
params = globals()['params']


def logme(message, level=0):
    # noinspection PyUnresolvedReferences
    threshold = params.get('Log')
    if level == 0 or (threshold and threshold >= level):
        print(message)


def log_error(message):
    logme(message, 1)


def log_info(message):
    logme(message, 2)


def get_latest_release():
    r = requests.get('https://api.github.com/repos/flyingeek/editolido/tags')
    data = r.json()
    try:
        url = 'https://github.com/flyingeek/editolido/archive/{0}.zip'.format(
            data[0]['name']
        )
        r.close()
        return data[0]['name'], url
    except (IndexError, KeyError):
        pass
    return None, None


def download_package(github_url, zip_folder, install_dir, name="editolido"):
    log_info('downloading %s' % github_url)
    r = requests.get(github_url, verify=True, stream=True)
    try:
        r.raise_for_status()
    except requests.HTTPError:
        log_error('status code %s' % r.status_code)
    except requests.Timeout:
        log_error('download timeout... aborting update')
    except requests.ConnectionError:
        log_error('download connection error... aborting update')
    except requests.TooManyRedirects:
        log_error('too many redirects... aborting update')
    except requests.exceptions.RequestException:
        log_error('download fail... aborting update')
    else:
        log_info('extracting data')
        import shutil
        import zipfile
        from contextlib import closing
        from cStringIO import StringIO
        with closing(r), zipfile.ZipFile(StringIO(r.content)) as z:
            base = '%s/%s/' % (zip_folder, name)
            z.extractall(os.getcwd(),
                         filter(lambda m: m.startswith(base), z.namelist()))
        log_info('installing %s' % name)
        if not os.path.exists(install_dir):
            log_info('print creating directory %s' % install_dir)
            os.makedirs(install_dir)
        dest = os.path.join(install_dir, name)
        try:
            if dest and name and os.path.exists(dest):
                shutil.rmtree(dest)
        except OSError:
            log_error('could not remove %s' % dest)
            raise
        if zip_folder:
            shutil.move(os.path.join(zip_folder, name), install_dir)
            if not os.path.exists(os.path.join(install_dir, name)):
                log_error('%s/%s directory missing' % (install_dir, name))
            log_info('cleaning')
            try:
                shutil.rmtree(zip_folder)
            except OSError:
                log_error('could not remove %s/%s' % (os.getcwd(), zip_folder))
                raise


def show_editolido_status():
    # console is an Editorial module
    # noinspection PyUnresolvedReferences
    import console
    try:
        # noinspection PyUnresolvedReferences
        import editolido
        reload(editolido)
    except ImportError:
        try:
            # noinspection PyUnresolvedReferences
            console.alert(
                'Module editolido manquant',
                "Assurez vous d'avoir une connexion internet et recommencez "
                "pour tenter un nouveau téléchargement",
                'OK', hide_cancel_button=True)
        except NameError:
            pass
        log_error('editolido module is missing, aborting !')
        raise KeyboardInterrupt
    try:
        # noinspection PyUnresolvedReferences
        console.hud_alert(
            'module editolido %s installé' % editolido.__version__, 'success')
    except NameError:
        log_info('module editolido %s installé' % editolido.__version__)


try:
    tagname, zipball_url = get_latest_release()
    if tagname and zipball_url:
        download_package(
            zipball_url,
            'editolido-%s' % tagname,
            os.path.dirname(EDITOLIDO)
        )
    else:
        log_error('no editolido release available')
except (IOError, OSError):
    log_error('install failed')
else:
    show_editolido_status()
