# -*- coding: utf-8 -*-
# mailbot.py

"""
Module de Gestion de mail préparés

pathfile : dreamtools/mailbot.py

Pré-Requis
-------------
.. warning::

    Indiquer les parametres smtp dans le fichiers de configuration <PROJECT_NAME>/cfg/.app.yml

.. code-block:: YAML

    smtp:
     h: smtp-host_adresse
     po: port_smtp
     m: mail_authen
     pw: password_auth
     h_s : name_sender <email>


.. warning::

    Les mails sont à définir dans le ficchier <PROJECT_NAME>/cfg/mailing.yml au format suivant

.. code-block:: YAML

     footer:
      html: <Pied de mail unique pour tous les mails (signature, rgpd...)>
      text: <Pied de mail unique pour tous les mails (signature, rgpd...)>
     code_mail:
      html: <ici mail au format HTML>
      text : <Le mail au format texte>
      objt : <Objet du mail>

Class CMailer
--------------
"""

import smtplib
import ssl
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from . import cfgloader, tracker


class CMailer(object):
    smtp = cfgloader.app_cfg('smtp')
    footers = cfgloader.mailing_lib('footer')

    @staticmethod
    def __send_mail(subject, receivers, d_msg, to_receiver=None):
        """ Envoie du mail

        :param subject: Sujet du mail
        :param receivers: email destinataire
        :param d_msg: Message
        :param to_receiver: Nom destinataire
        :return:
        """

        tracker.flag("[dreamtools.mailbot] SEND_MAIL : Parametrage smtp")
        context = ssl.create_default_context()

        tracker.flag("[dreamtools.mailbot] SEND_MAIL:Parametrage message MIME")
        message = MIMEMultipart("alternative")
        message["Subject"] = subject
        message["From"] = CMailer.smtp['h_s']
        message["To"] = to_receiver or receivers

        tracker.flag("[dreamtools.mailbot] SEND_MAIL:Parametrage contenu mail")
        content = d_msg.get('text') + CMailer.footers['txt']
        content = MIMEText(content)
        message.attach(content)

        if d_msg.get('html'):
            content = d_msg.get('html') + CMailer.footers['html']
            content = MIMEText(content, "html")
            message.attach(content)

        tracker.flag("[dreamtools.mailbot] SEND_MAIL:Coonnexion SMTP")
        with smtplib.SMTP_SSL(CMailer.smtp['h'], CMailer.smtp['po'], context=context) as server:
            tracker.flag("[dreamtools.mailbot] SEND_MAIL:Authentification")
            server.login(CMailer.smtp['m'], CMailer.smtp['pw'])
            tracker.flag("[dreamtools.mailbot] SEND_MAIL: Sending")
            server.sendmail(CMailer.smtp['m'], receivers, message.as_string())

            return True

    @staticmethod
    def presend(email, code, name='', **data_field):
        """ Preparation pour envoi d'un message mail 
        
        :param str email: email destinataire
        :param str code: réfénce du mail à chargé
        :param str name: nom du destinataire
        :param dict data_field: liste de données relatif à des champs définis dans le mails

        
        """
        tracker.flag('[dreamtools.mailbot] PRESEND:Loading template {}'.format(code))
        mail = cfgloader.mailing_lib(code)

        tracker.flag('[dreamtools.mailbot] PRESEND: Preparation')

        part1 = mail['text'].format(**data_field)
        part2 = mail['html'].format(**data_field)
        to_receiver = r'{} <{mail}>'.format(name, mail=email)

        tracker.flag('[dreamtools.mailbot] PRESEND: Envoi ({}) -> {}'.format(code, email))
        send = tracker.fntracker(CMailer.__send_mail, 'Envoi ({}) -> {}'.format(code, email), mail.get('objt'),
                                 email, {'text': part1, 'html': part2}, to_receiver)

        return send.ok


__all__ = ['CMailer']
