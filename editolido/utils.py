# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import os
import sys
from distutils.version import StrictVersion
import editolido
from editolido.bootstrap_editorial import logger, tagname_from_url, \
    download_package


def reload_editolido(install_dir, name='editolido'):
    for module in sys.modules.values():
        try:
            if os.path.realpath(module.__file__).startswith(
                    os.path.join(install_dir, name) + '/'):
                if module.__name__ == 'editolido':
                    reload(module)
                    logger.info('Reloaded %s' % module.__name__)
                else:
                    raise ImportError
        except AttributeError:
            pass
        except ImportError:
            logger.info('deleting module %s' % module.__name__)
            del sys.modules[module.__name__]


def update_editolido(install_dir, boot_url='', url='', name=None,
                     fake=False):
    local_version = StrictVersion(editolido.__version__)
    tagname = tagname_from_url(url)
    if tagname:
        logger.info('latest remote version is %s' % tagname)
        # download when local < remote
        # or when remote is a branch (master, beta...)
        if '.' not in tagname:
            logger.info('branch are always downloaded')
        if '.' not in tagname or local_version < StrictVersion(tagname):
            try:
                download_package(
                    url,
                    '%s-%s' % (name, tagname),
                    install_dir,
                    name=name,
                    fake=fake,
                )
            except (IOError, OSError):
                logger.error('install failed')
            else:
                reload_editolido(install_dir, name)
                try:
                    import console
                except ImportError:
                    from editolido.workflows.editorial.console import Console
                    console = Console(logger)
                logger.info('editolido module %s installed'
                            % editolido.__version__)
                console.hud_alert('module editolido %s installé'
                                  % editolido.__version__)
        else:
            logger.info('local version up to date')
    else:
        logger.error('invalid url %s' % url)
