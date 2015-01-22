# -*- coding: utf-8 -*-
##j## BOF

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

# pylint: disable=invalid-name

from base64 import b64encode
from email.message import Message
from quopri import encodestring

try:
#
	_PY_BYTES = unicode.encode
	_PY_BYTES_TYPE = str
	_PY_STR = unicode.encode
	_PY_UNICODE_TYPE = unicode
#
except NameError:
#
	_PY_BYTES = str.encode
	_PY_BYTES_TYPE = bytes
	_PY_STR = bytes.decode
	_PY_UNICODE_TYPE = str
#

class Part(Message):
#
	"""
This is an e-mail mime part that can be attached to a message.

:author:    direct Netware Group
:copyright: (C) direct Netware Group - All rights reserved
:package:   rfc_email.py
:since:     v0.1.00
:license:   https://www.direct-netware.de/redirect?licenses;mpl2
            Mozilla Public License, v. 2.0
	"""

	TYPE_ATTACHMENT = 1
	"""
e-mail attachment
	"""
	TYPE_BINARY_ATTACHMENT = 2
	"""
Binary e-mail attachment
	"""
	TYPE_BINARY_INLINE = 4
	"""
Binary e-mail inline part
	"""
	TYPE_INLINE = 3
	"""
e-mail inline part
	"""
	TYPE_MESSAGE_BODY = 5
	"""
e-mail message body
	"""
	TYPE_MULTIPART = 6
	"""
e-mail multipart body
	"""

	def __init__(self, _type, mimetype, data = None, filename = None):
	#
		"""
Constructor __init__(Part)

:param url: URL to be called
:param timeout: Connection timeout in seconds
:param event_handler: EventHandler to use

:since: v0.1.00
		"""

		# global: _PY_BYTES, _PY_BYTES_TYPE, _PY_STR, _PY_UNICODE_TYPE

		Message.__init__(self)

		self.content_id = None
		"""
Defines what type the given data represents.
		"""
		self.part_type = _type
		"""
Defines what type the given data represents.
		"""

		self.set_type(mimetype)
		if (self.part_type != Part.TYPE_MULTIPART and data is None): raise TypeError("Given data type is not supported")

		payload = None

		if (self.part_type == Part.TYPE_BINARY_ATTACHMENT or self.part_type == Part.TYPE_BINARY_INLINE):
		#
			if (str is not _PY_BYTES_TYPE and type(data) is str): data = _PY_BYTES(data, "raw_unicode_escape")
			if (type(data) != _PY_BYTES_TYPE): raise TypeError("Given data type is not supported")

			self.add_header("Content-Transfer-Encoding", "base64")
			payload = b64encode(data)
		#
		elif (self.part_type == Part.TYPE_ATTACHMENT
		      or self.part_type == Part.TYPE_INLINE
		      or self.part_type == Part.TYPE_MESSAGE_BODY
		     ):
		#
			if (str is not _PY_BYTES_TYPE and type(data) is str): data = _PY_BYTES(data, "utf-8")
			if (type(data) is not _PY_BYTES_TYPE): raise TypeError("Given data type is not supported")

			self.add_header("Content-Transfer-Encoding", "quoted-printable")
			self.set_param("charset", "UTF-8", "Content-Type")
			payload = encodestring(data)
		#

		if (payload is not None):
		#
			if (type(payload) is not str): payload = _PY_STR(payload, "raw_unicode_escape")
			self.set_payload(payload)
		#

		if (self.part_type == Part.TYPE_ATTACHMENT
		    or self.part_type == Part.TYPE_BINARY_ATTACHMENT
		    or self.part_type == Part.TYPE_BINARY_INLINE
		    or self.part_type == Part.TYPE_INLINE
		   ):
		#
			if (str != _PY_UNICODE_TYPE and type(filename) is _PY_UNICODE_TYPE): filename = _PY_STR(filename, "utf-8")
			if (type(filename) is not str): raise TypeError("Given filename type is not supported")

			self.content_id = "cid{0:d}@mail".format(id(self))
			self.add_header("Content-ID", "<{0}>".format(self.content_id))

			disposition_type = ("attachment"
			                    if (self.part_type == Part.TYPE_ATTACHMENT or self.part_type == Part.TYPE_BINARY_ATTACHMENT) else
			                    "inline"
			                   )

			self.add_header("Content-Disposition", disposition_type, filename = filename)
		#
	#

	def get_content_id(self):
	#
		"""
Return the part type.

:return: (int) Part type
:since:  v0.1.00
		"""

		return self.content_id
	#

	def get_part_type(self):
	#
		"""
Return the part type.

:return: (int) Part type
:since:  v0.1.00
		"""

		return self.part_type
	#
#

##j## EOF