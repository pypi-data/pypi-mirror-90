from . import tools
from . import tracker


class CConfig:

    def __init__(self, app, mode="PROD"):
        """ Configuration des parametres d'accès relatif au projet en cours

        Parametres
        -----------
        :param str app: Nom de l'application
        :param str[PROD|DEV] mode: PRDO ou DEV

        """

        tools.APP_NAME = app
        tools.PROJECT_DIR = tools.dirproject()
        tools.APP_DIR = tools.path_build(tools.PROJECT_DIR, tools.APP_NAME)
        tools.TMP_DIR = tools.path_build(tools.PROJECT_DIR, 'tmp')

        tracker.config(mode)
