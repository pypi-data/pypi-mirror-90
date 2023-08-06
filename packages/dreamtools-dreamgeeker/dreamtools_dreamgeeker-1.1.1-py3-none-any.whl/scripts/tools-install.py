#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# app_tools.py

from dreamtools import cfgloader
from dreamtools import tools
from source import source


def set_project():
    base = tools.dirproject()

    print('[dreamtools-install] Création architecture')

    print('\t Répertoire configuration')
    tools.makedirs(tools.path_build(base, 'cfg'))

    print('\tRépertoire logs')
    tools.makedirs(tools.path_build(base, 'logs'))

    print('[dreamtools-install] Export configuration de base')
    src = tools.path_build(base, 'cfg')

    for files, data in source.items():
        cfgloader.save_cfg(eval(data), tools.path_build(src, files))
