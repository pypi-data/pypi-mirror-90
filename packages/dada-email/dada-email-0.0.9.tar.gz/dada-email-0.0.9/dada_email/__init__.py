import smtplib
import imaplib
from email.utils import make_msgid
from email.message import EmailMessage
from email.headerregistry import Address
from contextlib import contextmanager

from dada_types import T, SerializableObject

from dada_email.utils import *


class Email(SerializableObject):
    __module__ = "dada_email"

    def __init__(self, **kwargs):

        # from email
        self.from_user_email = kwargs.get("from_user")
        self.from_user_full_name = kwargs.get("from_user_full_name")
        self.from_user_name, self.domain = email_parse(self.from_user_email)

        self.password = kwargs.get("password")
        self.host = kwargs.get("host")
        self.smtp_port = kwargs.get("smtp_port")
        self.imap_port = kwargs.get("imap_port")

        # cache connections
        self._smtp = None
        self._imap = None

    # utils

    def _get_address(self, addr: str, name: str = "") -> Address:
        """
        Parse an email to an address field
        """
        user_name, domain(_addr)
        return Address(name, user_name, domain)

    # connections

    @property
    def smtp(self):
        """
        The SMTP connection
        ```
        m = Mailer()
        with m.smtp() as connection:
            connection.send_message('blah')
        ```
        """
        if self._smtp is None:
            self._smtp = smtplib.SMTP(self.host, port=self.smtp_port)
        return self._smtp

    def smtp_login(self):
        self.smtp.login(user=self.from_user, password=self.password)

    def smtp_logout(self):
        self.smtp.logout()

    @property
    def imap(self):
        """
        The IMAP connection: https://docs.python.org/3/library/imaplib.html
        """
        # if self._imap is None:
        #     self._imap = smtplib.SMTP(self.host, port=self.smtp_port)
        # return self._imap
        pass

    # send messages

    @property
    def default_from_address(self) -> Address:
        """
        The address to send the email from.
        """
        return Address(self.from_user_full_name, self.from_user_name, self.domain)

    def create_message(self, **kwargs: dict) -> EmailMessage:
        """
        Create an Email message
        See: https://docs.python.org/3/library/email.message.html#email.message.EmailMessage
        """
        msg = EmailMessage()
        msg_cid = make_msgid()

        # subject
        msg["Subject"] = kwargs.get("subject")

        # from addresses
        from_addr = [self._get_address(**e) for e in kwargs.get("from_email", [])]
        if kwargs.get("incl_internal", True):
            from_addr.extend(self.default_from_address)
        msg["From"] = from_addr

        # to addresses
        to_addr = [self._get_address(**e) for e in kwargs.get("to_email", [])]
        msg["To"] = to_addr

        # TODO: cc/bcc

        # content
        msg.set_content(kwargs.get("text", ""))
        _html_content = kwargs.get("html", kwargs.get("text", ""))
        msg.add_alternative(_html_content, subtype="html")

        # TOOD: attachements
        return msg

    def send(self, **kwargs):
        """
        Send a message
        """
        self.smtp.send_message(self.create_message(**kwargs))

    # search messages

    def search(self, query: str):
        """
        :param query: A query to use to search the inbox.
        """
        return []


def init_email_resource(**resource_config):
    """
    Initialize a marketo client via: https://github.com/jepcastelein/marketo-rest-python
    """
    return Email(**resource_config)


@resource(
    config_schema={
        "from_user": str,
        "from_user_full_name": str,
        "host": str,
        "smtp_port": int,
        "imap_port": int,
        "password": StringSource,
    }
)
def email_resource(ctx):
    """
    Ioby's Marketo Account, via: https://github.com/jepcastelein/marketo-rest-python
    """
    return init_email_resource(**ctx.resource_config)
