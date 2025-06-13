# -*- coding: utf-8 -*-
import smtplib
from email.mime.text import MIMEText
import requests

from src.commons.exception import ServiceError
from src.helpers.base_helper import BaseHelper


class MailHelper(BaseHelper):

    def __init__(self, app):
        super().__init__()
        self._app = app
        self._mail_driver = app.config["MAIL_DRIVER"]
        self._mail_host = app.config["MAIL_HOST"]
        self._mail_port = app.config["MAIL_PORT"]
        self._mail_username = app.config["MAIL_USERNAME"]
        self._mail_password = app.config["MAIL_PASSWORD"]
        self._mail_encryption = app.config["MAIL_ENCRYPTION"]
        self._mail_from_address = app.config["MAIL_FROM_ADDRESS"]
        self._mail_from_name = app.config["MAIL_FROM_NAME"]
        self._mail_mailgun_domain = app.config["MAILGUN_DOMAIN"]
        self._mail_mailgun_secret = app.config["MAILGUN_SECRET"]

    def send(self, schema):
        if self._mail_driver == "mailgun":
            self.mailgun_send(schema=schema)
        elif self._mail_driver == "smtp":
            self.smtp_send(schema=schema)
        else:
            pass

    def mailgun_send(self, schema):
        try:
            requests.post(
                "https://api.mailgun.net/v3/" + self._mail_mailgun_domain + "/messages",
                auth=("api", self._mail_mailgun_secret),
                data={"from": self._mail_from_name + " <" + self._mail_from_address + ">",
                      "to": [schema["recipient"]],
                      "subject": schema["subject"],
                      "text": schema["text"]})
        except Exception as e:
            raise ServiceError(code="mail.service.error", message="Mail service error")
        return True

    def smtp_send(self, schema):
        try:
            msg = MIMEText(schema["text"])
            msg["Subject"] = schema["subject"]
            msg["From"] = self._mail_from_name + " <" + self._mail_from_address + ">"
            msg["To"] = schema["recipient"]
            s = smtplib.SMTP(self._mail_host, self._mail_port)
            s.login(self._mail_username, self._mail_password)
            s.sendmail(msg["From"], msg["To"], msg.as_string())
            s.quit()
        except Exception as e:
            raise ServiceError(code="mail.service.error", message="Mail service error")
        return True
