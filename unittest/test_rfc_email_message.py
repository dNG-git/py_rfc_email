# -*- coding: utf-8 -*-

"""
RFC e-mail for Python
An abstracted programming interface to generate e-mails
----------------------------------------------------------------------------
(C) direct Netware Group - All rights reserved
https://www.direct-netware.de/redirect?rfc;email

This Source Code Form is subject to the terms of the Mozilla Public License,
v. 2.0. If a copy of the MPL was not distributed with this file, You can
obtain one at http://mozilla.org/MPL/2.0/.
----------------------------------------------------------------------------
https://www.direct-netware.de/redirect?licenses;mpl2
----------------------------------------------------------------------------
#echo(rfcEMailVersion)#
#echo(__FILEPATH__)#
"""

import re
import unittest

from dNG.data.rfc.email.message import Message
from dNG.data.rfc.email.part import Part

class TestRfcEMailPart(unittest.TestCase):
    def test_plain(self):
        """
Test basic methods for an ASCII attachment.
        """

        part = Part(Part.TYPE_MESSAGE_BODY, "text/plain", "Hello world")

        message = Message()
        message.set_subject("Test message")
        message.add_body(part)

        self.assertEqual(
            """MIME-Version: 1.0
Content-Transfer-Encoding: quoted-printable
Content-Type: text/plain; charset="UTF-8"
To: undisclosed-recipients
Date: Thu, 01 Jan 1970 00:00:00 GMT
Subject: Test message

Hello world""",
            TestRfcEMailPart._get_unified_message_as_string(message)
                        )
    #

    def test_multipart_alternative(self):
        """
Test basic methods for an ASCII attachment.
        """

        part = Part(Part.TYPE_MESSAGE_BODY, "text/plain", "Hello world")

        message = Message()
        message.set_subject("Test message")
        message.add_body(part)

        part = Part(Part.TYPE_MESSAGE_BODY, "application/xhtml+xml", "<p>This is broken by design</p>")
        message.add_body(part)

        self.assertEqual(
            """MIME-Version: 1.0
Content-Type: multipart/alternative; boundary="===============x=="
To: undisclosed-recipients
Date: Thu, 01 Jan 1970 00:00:00 GMT
Subject: Test message

--===============x==
MIME-Version: 1.0
Content-Transfer-Encoding: quoted-printable
Content-Type: text/plain; charset="UTF-8"

Hello world
--===============x==
MIME-Version: 1.0
Content-Transfer-Encoding: quoted-printable
Content-Type: application/xhtml+xml; charset="UTF-8"

<p>This is broken by design</p>
--===============x==--""",
            TestRfcEMailPart._get_unified_message_as_string(message)
                        )
    #

    def test_multipart_mixed(self):
        """
Test basic methods for an ASCII attachment.
        """

        part = Part(Part.TYPE_MESSAGE_BODY, "text/plain", "Hello world")

        message = Message()
        message.set_subject("We like German Umlauts to test UTF-8 öäü")
        message.add_body(part)

        part = Part(Part.TYPE_INLINE, "text/plain", "Hello world", file_name = "test.txt")
        message.add_body_related_attachment(part)

        part = Part(Part.TYPE_ATTACHMENT, "text/plain", "Hello world", file_name = "test.txt")
        message.add_attachment(part)

        part = Part(Part.TYPE_ATTACHMENT, "text/plain", "Hello world 2", file_name = "test2.txt")
        message.add_attachment(part)
        self.maxDiff = None

        self.assertEqual(
            """MIME-Version: 1.0
Content-Type: multipart/mixed; boundary="===============x=="
To: undisclosed-recipients
Date: Thu, 01 Jan 1970 00:00:00 GMT
Subject: =?utf-8?q?We_like_German_Umlauts_to_test_UTF-8_=C3=B6=C3=A4=C3=BC?=

--===============x==
MIME-Version: 1.0
Content-Type: multipart/related; boundary="===============x=="

--===============x==
MIME-Version: 1.0
Content-Transfer-Encoding: quoted-printable
Content-Type: text/plain; charset="UTF-8"

Hello world
--===============x==
MIME-Version: 1.0
Content-Transfer-Encoding: quoted-printable
Content-Type: text/plain; charset="UTF-8"
Content-ID: <cidx@mail>
Content-Disposition: inline; filename="test.txt"

Hello world
--===============x==--
--===============x==
MIME-Version: 1.0
Content-Transfer-Encoding: quoted-printable
Content-Type: text/plain; charset="UTF-8"
Content-ID: <cidx@mail>
Content-Disposition: attachment; filename="test.txt"

Hello world
--===============x==
MIME-Version: 1.0
Content-Transfer-Encoding: quoted-printable
Content-Type: text/plain; charset="UTF-8"
Content-ID: <cidx@mail>
Content-Disposition: attachment; filename="test2.txt"

Hello world 2
--===============x==--""",
            TestRfcEMailPart._get_unified_message_as_string(message)
                        )
    #

    @staticmethod
    def _get_unified_message_as_string(message):
        """
Returns the message in a unified (but not standard conform) way.

:return: (str) Unified formatted message
        """

        _return = re.sub("===============\\d+==", "===============x==", message.as_string())
        _return = re.sub("\n boundary=\"===============x==\"\n", " boundary=\"===============x==\"\n", _return)
        _return = re.sub("^Content-ID: <cid\\d+@mail>$", "Content-ID: <cidx@mail>", _return, flags = re.M)
        _return = re.sub("^Date: \\w{3}, \\d{2} \\w{3} \\d{4} \\d{2}:\\d{2}:\\d{2} GMT$", "Date: Thu, 01 Jan 1970 00:00:00 GMT", _return, flags = re.M)

        _return = _return.replace("--===============x==--\n\n", "--===============x==--\n")

        return _return.strip()
    #
#

if (__name__ == "__main__"):
    unittest.main()
#
