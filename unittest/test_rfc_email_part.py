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
import sys
import unittest

from dNG.data.rfc.email.part import Part

class TestRfcEMailPart(unittest.TestCase):
#
	def test_ascii_attachment(self):
	#
		"""
Test basic methods for an ASCII attachment.
		"""

		part = Part(Part.TYPE_ATTACHMENT, "text/plain", "Hello world", filename = "hello_world.txt")
		self.assertEqual(Part.TYPE_ATTACHMENT, part.get_part_type())

		_exception = None

		try: Part(Part.TYPE_ATTACHMENT, "text/plain", "Hello world")
		except TypeError as handled_exception: _exception = handled_exception

		self.assertTrue(isinstance(_exception, TypeError))

		# This test uses German special characters

		part = Part(Part.TYPE_ATTACHMENT, "text/plain", "Hallo Welt, schön das du dich drehst.", filename = "hallo_welt_öäü.txt")
		self.assertEqual("Hallo Welt, sch=C3=B6n das du dich drehst.", part.get_payload())
	#

	def test_ascii_inline(self):
	#
		"""
Test basic methods for an ASCII inline part.
		"""

		part = Part(Part.TYPE_INLINE, "text/plain", "Hello world", filename = "hello_world.txt")
		self.assertEqual(Part.TYPE_INLINE, part.get_part_type())

		_exception = None

		try: Part(Part.TYPE_ATTACHMENT, "text/plain", "Hello world")
		except TypeError as handled_exception: _exception = handled_exception

		self.assertTrue(isinstance(_exception, TypeError))
	#
#

if (__name__ == "__main__"):
#
	sys.path.append(path.normpath("../src"))
	unittest.main()
#

##j## EOF