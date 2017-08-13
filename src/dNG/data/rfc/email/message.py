# -*- coding: utf-8 -*-

"""
RFC e-mail for Python
An abstracted programming interface to generate e-mails
----------------------------------------------------------------------------
(C) direct Netware Group - All rights reserved
https://www.direct-netware.de/redirect?py;rfc_email

This Source Code Form is subject to the terms of the Mozilla Public License,
v. 2.0. If a copy of the MPL was not distributed with this file, You can
obtain one at http://mozilla.org/MPL/2.0/.
----------------------------------------------------------------------------
https://www.direct-netware.de/redirect?licenses;mpl2
----------------------------------------------------------------------------
#echo(rfcEMailVersion)#
#echo(__FILEPATH__)#
"""

from email.header import Header
from email.utils import formataddr, parseaddr
from time import time
import re

try:
    _PY_STR = unicode.encode
    _PY_UNICODE_TYPE = unicode
except NameError:
    _PY_STR = bytes.decode
    _PY_UNICODE_TYPE = str
#

from dNG.data.rfc.basics import Basics
from .part import Part

class Message(object):
    """
An e-mail consists of at least one message body part and optional
attachments.

:author:    direct Netware Group
:copyright: (C) direct Netware Group - All rights reserved
:package:   rfc_email.py
:since:     v0.1.00
:license:   https://www.direct-netware.de/redirect?licenses;mpl2
            Mozilla Public License, v. 2.0
    """

    def __init__(self):
        """
Constructor __init__(Message)

:param url: URL to be called
:param timeout: Connection timeout in seconds
:param event_handler: EventHandler to use

:since: v0.1.00
        """

        self.attachment_list = [ ]
        """
List of attachments
        """
        self.body_list = [ ]
        """
List of message bodies added
        """
        self.body_related_list = [ ]
        """
List of attachments
        """
        self.headers = { }
        """
Dictionary of additional e-mail headers
        """
        self.message = None
        """
Populated message instance build by "_populate_message()"
        """
        self.recipients = [ ]
        """
Recipient e-mail addresses
        """
        self.recipients_bcc = [ ]
        """
Recipient bcc e-mail addresses
        """
        self.recipients_cc = [ ]
        """
Recipient cc e-mail addresses
        """
        self.reply_to_address = ""
        """
Reply-To e-mail address
        """
        self.sender_address = ""
        """
From e-mail address
        """
        self._subject = ""
        """
e-mail subject
        """
    #

    @property
    def bcc(self):
        """
Returns the "BCC" recipient address list.

:return: (list) ASCII e-mail addresses
:since:  v1.0.0
        """

        return self.recipients_bcc
    #

    @bcc.setter
    def bcc(self, address):
        """
Sets the bcc recipient address.

:param address: ASCII e-mail address

:since: v1.0.0
        """

        self.recipients_bcc = [ ]
        self.add_bcc(address)
    #

    @property
    def _body(self):
        """
Returns the populated body element.

:return: (mixed) Matching body multipart element; None if unneeded
:since:  v1.0.0
        """

        if (len(self.body_list) < 1): raise ValueError("No body has been defined")

        # First handle alternative representations of the body
        if (len(self.body_list) > 1):
            body_root = Part(Part.TYPE_MULTIPART, "multipart/alternative")
            for body_part in self.body_list: body_root.attach(body_part)
        else: body_root = self.body_list[0]

        # If related attachments are defined we will add them now
        if (len(self.body_related_list) > 0):
            _return = Part(Part.TYPE_MULTIPART, "multipart/related")
            _return.attach(body_root)
            for related_part in self.body_related_list: _return.attach(related_part)
        else: _return = body_root

        return _return
    #

    @property
    def cc(self):
        """
Returns the "CC" recipient address list.

:return: (list) ASCII e-mail addresses
:since:  v1.0.0
        """

        return self.recipients_cc
    #

    @cc.setter
    def cc(self, address):
        """
Sets the cc recipient address.

:param address: ASCII e-mail address

:since: v1.0.0
        """

        self.recipients_cc = [ ]
        self.add_cc(address)
    #

    @property
    def is_sender_set(self):
        """
Returns true if the sender address has been set.

:return: (bool) True if set
:since:  v1.0.0
        """

        return (self.sender_address != "")
    #

    @property
    def is_recipient_set(self):
        """
Returns true if at least one recipient has been defined.

:return: (bool) True if set
:since:  v1.0.0
        """

        return (len(self.recipients + self.recipients_bcc + self.recipients_cc) > 0)
    #

    @property
    def is_reply_to_set(self):
        """
Returns true if the "Reply-To" address has been set.

:return: (bool) True if set
:since:  v1.0.0
        """

        return (self.reply_to_address != "")
    #

    @property
    def is_subject_set(self):
        """
Returns true if the e-mail subject has been set.

:return: (bool) True if set
:since:  v1.0.0
        """

        return (self._subject != "")
    #

    @property
    def reply_to(self):
        """
Returns the "Reply-To" address.

:return: (str) ASCII e-mail address
:since:  v1.0.0
        """

        return self.reply_to_address
    #

    @reply_to.setter
    def reply_to(self, address):
        """
Sets the "Reply-To" address.

:param address: ASCII e-mail address

:since: v1.0.0
        """

        Message.validate_address(address)
        self.reply_to_address = address
    #

    @property
    def sender(self):
        """
Returns the sender address.

:return: (list) ASCII e-mail address
:since: v1.0.0
        """

        return self.sender_address
    #

    @sender.setter
    def sender(self, address):
        """
Sets the sender address.

:param address: ASCII e-mail address

:since: v1.0.0
        """

        Message.validate_address(address)
        self.sender_address = address
    #

    @property
    def subject(self):
        """
Returns the e-mail subject.

:return: (str) e-mail subject
:since:  v1.0.0
        """

        return self._subject
    #

    @subject.setter
    def subject(self, subject):
        """
Sets the e-mail subject.

:param subject: e-mail subject

:since: v1.0.0
        """

        self._subject = subject.strip()
    #

    @property
    def to(self):
        """
Returns the recipient address list.

:return: (list) ASCII e-mail addresses
:since:  v1.0.0
        """

        return self.recipients
    #

    @to.setter
    def to(self, address):
        """
Sets the recipient address.

:param address: ASCII e-mail address

:since: v1.0.0
        """

        self.recipients = [ ]
        self.add_to(address)
    #

    def add_attachment(self, part):
        """
Adds an e-mail attachment.

:param part: Message part

:since: v0.1.00
        """

        if ((not isinstance(part, Part))
            or (part.type != Part.TYPE_ATTACHMENT
                and part.type != Part.TYPE_BINARY_ATTACHMENT
                and part.type != Part.TYPE_BINARY_INLINE
                and part.type != Part.TYPE_INLINE
               )
           ):
            raise TypeError("Only parts of type attachment can be added as attachment elements")

        if (part not in self.attachment_list): self.attachment_list.append(part)
    #

    def _add_attachments_to_multipart(self, part):
        """
Appends previously added attachments to the given message part.

:param part: Message part

:since: v0.1.00
        """

        for attachment_part in self.attachment_list: part.attach(attachment_part)
    #

    def add_bcc(self, address):
        """
Adds the bcc recipient address.

:param address: ASCII e-mail address

:since: v0.1.00
        """

        Message.validate_address(address)
        if (address not in self.recipients_bcc): self.recipients_bcc.append(address)
    #

    def add_body(self, part):
        """
Adds an e-mail message body. Please note that RFC defines an increasing
priority for each body part added. That means the last body should be the
preferred representation.

:param part: Message part

:since: v0.1.00
        """

        if ((not isinstance(part, Part))
            or part.type != Part.TYPE_MESSAGE_BODY
           ): raise TypeError("Only parts of type message body can be added as body elements")

        if (part not in self.body_list): self.body_list.append(part)
    #

    def add_body_related_attachment(self, part):
        """
Adds an e-mail attachment related to the message body.

:param part: Message part

:since: v0.1.00
        """

        if ((not isinstance(part, Part))
            or (part.type != Part.TYPE_ATTACHMENT
                and part.type != Part.TYPE_BINARY_ATTACHMENT
                and part.type != Part.TYPE_BINARY_INLINE
                and part.type != Part.TYPE_INLINE
               )
           ):
            raise TypeError("Only parts of type attachment can be added as body related elements")

        if (part not in self.body_related_list): self.body_related_list.append(part)
    #

    def _add_body_to_multipart(self, part):
        """
Appends the body to the given message part.

:param part: Message part

:since: v0.1.00
        """

        part.attach(self._body)
    #

    def add_cc(self, address):
        """
Adds the cc recipient address.

:param address: ASCII e-mail address

:since: v0.1.00
        """

        Message.validate_address(address)
        if (address not in self.recipients_cc): self.recipients_cc.append(address)
    #

    def add_to(self, address):
        """
Adds the recipient address.

:param address: ASCII e-mail address

:since: v0.1.00
        """

        Message.validate_address(address)
        if (address not in self.recipients): self.recipients.append(address)
    #

    def _apply_headers(self, part):
        """
Sets the e-mail headers of the given message part.

:param part: Message part

:since: v0.1.00
        """

        if (self.sender_address != ""): part['From'] = self.sender_address
        part['To'] = (", ".join(self.recipients) if (len(self.recipients) > 0) else "undisclosed-recipients")
        if (len(self.recipients_cc) > 0): part['cc'] = ", ".join(self.recipients_cc)
        if (self.reply_to_address != ""): part['Reply-To'] = ", ".join(self.reply_to_address)

        if ("Date" not in part): part['Date'] = Basics.get_rfc5322_datetime(time())

        part['Subject'] = (self._subject
                           if (re.search("[\\x00-\\x19\\x22\\x28\\x29\\x2c\\x2e\\x3a-\\x3c\\x3e\\x40\\x5b-\\x5d\\x7f-\\xff]", self._subject) is None) else
                           Header(self._subject, "utf-8")
                          )

        for name in self.headers: part[name] = self.headers[name]
    #

    def as_string(self):
        """
python.org: Return the entire formatted message as a string.

:return: (str) Formatted message
:since:  v0.1.00
        """

        self._populate_message()
        return self.message.as_string()
    #

    def _populate_message(self):
        """
python.org: Return the entire formatted message as a string.

:since: v0.1.00
        """

        if (not self.is_subject_set): raise ValueError("No subject defined for e-mail")

        if (len(self.attachment_list) > 0):
            self.message = Part(Part.TYPE_MULTIPART, "multipart/mixed")
            self._apply_headers(self.message)
            self._add_body_to_multipart(self.message)
        else:
            self.message = self._body
            self._apply_headers(self.message)
        #

        self._add_attachments_to_multipart(self.message)
    #

    def set_header(self, name, value):
        """
Sets a header.

:param name: Header name
:param value: Header value as string

:since: v0.1.01
        """

        name = name.upper()

        if (value is None):
            if (name in self.headers): del(self.headers[name])
        elif (name not in self.headers): self.headers[name] = value
    #

    @staticmethod
    def format_address(value, email):
        """
Formats the given text value and e-mail address to an RFC compliant string.

:param value: Text value
:param email: E-Mail address

:return: (str) RFC compliant string
:since:  v0.1.00
        """

        return formataddr(( value, email ))
    #

    @staticmethod
    def validate_address(address):
        """
Validates the e-mail of the given address.
        """

        # global: _PY_STR, _PY_UNICODE_TYPE

        address_data = parseaddr(address)
        if (str is not _PY_UNICODE_TYPE and type(address_data[1]) is _PY_UNICODE_TYPE): address_data[1] = _PY_STR(address_data[1], "utf-8")

        if (address_data[1] == ""): raise TypeError("Given e-mail is not valid")
    #
#
