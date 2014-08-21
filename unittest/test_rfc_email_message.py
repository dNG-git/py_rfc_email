# -*- coding: utf-8 -*-
##j## BOF

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

from os import path
import re
import sys
import unittest

from dNG.data.rfc.email.message import Message
from dNG.data.rfc.email.part import Part

class TestRfcEMailPart(unittest.TestCase):
#
	def test_plain(self):
	#
		"""
Test basic methods for an ASCII attachment.
		"""

		part = Part(Part.TYPE_MESSAGE_BODY, "text/plain", "Hello world")

		message = Message()
		message.add_body(part)

		self.assertEqual(
			"""MIME-Version: 1.0
Content-Transfer-Encoding: quoted-printable
Content-Type: text/plain; charset="UTF-8"

Hello world""",
			message.as_string()
		)
	#

	def test_multipart_alternative(self):
	#
		"""
Test basic methods for an ASCII attachment.
		"""

		part = Part(Part.TYPE_MESSAGE_BODY, "text/plain", "Hello world")

		message = Message()
		message.add_body(part)

		part = Part(Part.TYPE_MESSAGE_BODY, "application/xhtml+xml", "<p>This is broken by design</p>")
		message.add_body(part)

		self.assertEqual(
			"""MIME-Version: 1.0
Content-Type: multipart/alternative; boundary="===============x=="

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
	#
		"""
Test basic methods for an ASCII attachment.
		"""

		part = Part(Part.TYPE_MESSAGE_BODY, "text/plain", "Hello world")

		message = Message()
		message.add_body(part)

		part = Part(Part.TYPE_INLINE, "text/plain", "Hello world", filename = "test.txt")
		message.add_body_related_attachment(part)

		part = Part(Part.TYPE_ATTACHMENT, "text/plain", "Hello world", filename = "test.txt")
		message.add_attachment(part)

		part = Part(Part.TYPE_ATTACHMENT, "text/plain", "Hello world 2", filename = "test2.txt")
		message.add_attachment(part)
		self.maxDiff = None

		self.assertEqual(
			"""MIME-Version: 1.0
Content-Type: multipart/mixed; boundary="===============x=="

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
	#
		"""
Returns the message in a unified (but not standard conform) way.

:return: (str) Unified formatted message
		"""

		_return = re.sub("===============\\d+==", "===============x==", message.as_string())
		_return = re.sub("\n boundary=\"===============x==\"\n", " boundary=\"===============x==\"\n", _return)
		_return = re.sub("^Content-ID: <cid\\d+@mail>$", "Content-ID: <cidx@mail>", _return, flags = re.M)

		return _return
	#
#

if (__name__ == "__main__"):
#
	sys.path.append(path.normpath("../src"))
	unittest.main()
#

##j## EOF