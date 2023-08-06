#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# __main__.py

import shutil
import sys

from dreamtools import tools


def setproject():
    """
    Intialisation du projet
    """

    base = tools.dirproject()
    print(base)
    return False
    dest = tools.path_build(base, 'cfg')

    print('**************************************************************************')
    print('** Création architecture')
    print('** -----------------------------------------------------------------------')
    print('** Répertoire logs ')
    tools.makedirs(tools.path_build(base, 'logs'))
    print('**\t>> Répertoire créé : ', tools.path_build(base, 'logs'))
    print('** Répertoire configuration')
    src = pkg_resources.resource_filename('dreamtools', 'cfg')
    shutil.copytree(src, dest)
    print('**\t>> Répertoire créé : ', dest)
    print('**=======================================================================-')


if __name__ == "__main__":
    sys.exit(setproject())
