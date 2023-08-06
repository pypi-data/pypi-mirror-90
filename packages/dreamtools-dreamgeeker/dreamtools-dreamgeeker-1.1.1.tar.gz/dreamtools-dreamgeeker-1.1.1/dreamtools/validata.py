# -*- coding: utf-8 -*-
# dreamtools/validata.py

from urllib.parse import unquote

from cerberus.validator import Validator, schema_registry

from . import cfgloader
from . import dtemng
from . import tools
from . import tracker
from .features import test_http_link
from .logmng import CError

schema_registry.add('email scheme', {'email': {'type': 'string', 'regex': tools.RGX_EMAIL}})
schema_registry.add('passowrd scheme', {'password': {'type': 'string', 'regex': tools.RGX_PWD}})
schema_registry.add('phone scheme', {'phone': {'type': 'string', 'regex': tools.RGX_PHONE}})

liste_categorie = []


class Validata(Validator):
    """
    Validators
    """
    __normalisator = cfgloader.normalizor()
    __validators = cfgloader.validator()

    def __init__(self, scheme, *args, **kwargs):
        dic = self.__validators.get(scheme)
        dic['creation_date'] = {'type': 'integer', 'default_setter': 'utcnow'}

        super().__init__(dic, *args, **kwargs)

    def _normalize_default_setter_utcnow(self, document):
        """Initialisateur date par defaut"""
        return dtemng.utcnow_ts()

    def _normalize_coerce_utcts(self, value):
        """Transforme une date valide en timestamp"""
        try:
            dte = dtemng.isotodate(value)  # str -> date
            dte = dtemng.datetime_from_local_to_utc(dte)  # local -> utc
        except:
            return None
        else:
            return dtemng.dtets(dte)  # dte ->timestamp

    def _normalize_coerce_int(self, value):
        """Transforme un nombre au format chaine en entier"""
        return int(value)

    def _normalize_coerce_clean_string(self, value):
        """Nettoyeur de chaine"""
        return tools.clean_space(value)

    def _normalize_coerce_event(self, value):
        """Validation de date au format '%d.%m.%Y %H:%M'"""
        try:
            dte = dtemng.strdate(value, '%d.%m.%Y %H:%M')
            dte = dtemng.dtets(dte)

            return dte
        except Exception as ex:
            tracker.exception_tracking(ex, 'validata.validata._normalize_coerce_event')
            return None

    def _check_with_validte(self, field, value):
        if dtemng.datestr(value) is None:
            self._error(field, "Date not valid")

    def _check_with_categorie(self, field, value):
        if value not in liste_categorie:
            self._error(field, "value not valid")

    def _check_with_url(self, field, value):
        from dreamtools import features
        try:
            if value and not features.test_http_link(value):
                self._error(field, "lient url non valid")
        except Exception as ex:
            self._error(field, "lient url non valid")
            tracker.exception_tracking(ex, 'validata.validata._normalize_coerce_event')

    def validation(self, document, *args, **kwargs):
        """

        :param document:
        :param args:
        :param kwargs:
        :return:
        """
        if self.validate(document, *args, **kwargs):
            return self.validated(document)
        return None

    def normalisation(self, document):
        """

        :param document:
        :param args:
        :param kwargs:
        :return:
        """
        return Validator(self.__normalisator).normalized(document)

    @staticmethod
    def check_post_data(data, form_ref):
        """ verification donnees formulaire recu

        :param dict data: formulaire de données
        :param str form_ref: reference validateur

        :return: formulaire traité
        """

        def fn():
            """
            function interne
            :return:
            """
            o = Validata(form_ref, purge_unknown=True)
            d = {k: unquote(tools.clean_space(v)) for k, v in data.items()}

            d = o.validation(d)
            if d: return d

            d = o.normalisation(o.errors)
            print(d)
            raise CError(','.join(d.keys()), 400, "VALIDATA.CHECK_POST_DATA")

        reponce = tracker.fntracker(fn, 'VALIDATA.CHECK_POST_DATA')

        if not reponce.ok and type(reponce.message).__name__ == 'dict':
            reponce.message = reponce.message.values()

        return reponce
