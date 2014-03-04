# -*- coding: utf-8 -*-
##j## BOF

"""
RFC e-Mail for Python
"""
"""n// NOTE
----------------------------------------------------------------------------
direct PAS
Python Application Services
----------------------------------------------------------------------------
(C) direct Netware Group - All rights reserved
http://www.direct-netware.de/redirect.py?py;rfc_email

This Source Code Form is subject to the terms of the Mozilla Public License,
v. 2.0. If a copy of the MPL was not distributed with this file, You can
obtain one at http://mozilla.org/MPL/2.0/.
----------------------------------------------------------------------------
http://www.direct-netware.de/redirect.py?licenses;mpl2
----------------------------------------------------------------------------
#echo(rfcEMailVersion)#
#echo(__FILEPATH__)#
----------------------------------------------------------------------------
NOTE_END //n"""

from .part import Part

class Message(object):
#
	"""
An e-Mail consists of at least one message body part and optional attachments.

:author:    direct Netware Group
:copyright: (C) direct Netware Group - All rights reserved
:package:   rfc_email.py
:since:     v0.1.00
:license:   http://www.direct-netware.de/redirect.py?licenses;mpl2
            Mozilla Public License, v. 2.0
	"""

	def __init__(self):
	#
		"""
Constructor __init__(Message)

:param url: URL to be called
:param timeout: Connection timeout in seconds
:param event_handler: EventHandler to use

:since: v0.1.00
		"""

		# global: _PY_STR, _PY_UNICODE_TYPE

		self.attachment_list = [ ]
		"""
List of attachments
		"""
		self.body_list = [ ]
		"""
List of message bodies added
		"""
		self.message = None
		"""
Underlying Python message instance
		"""
		self.body_related_list = [ ]
		"""
List of attachments
		"""
	#

	def add_attachment(self, part):
	#
		"""
Adds an e-Mail attachment to the message.

:param params: Query parameters as dict
:param separator: Query parameter separator

:return: (mixed) Response data; Exception on error
:since:  v0.1.00
		"""

		if (
			(not isinstance(part, Part)) or
			(
				part.get_part_type() != Part.TYPE_ATTACHMENT and
				part.get_part_type() != Part.TYPE_BINARY_ATTACHMENT and
				part.get_part_type() != Part.TYPE_BINARY_INLINE and
				part.get_part_type() != Part.TYPE_INLINE
			)
		):
		#
			raise TypeError("Only parts of type attachment can be added as attachment elements")
		#

		if (part not in self.attachment_list): self.attachment_list.append(part)
	#

	def _add_attachments_to_multipart(self, element):
	#
		"""
Appends previously added attachments to the given element.

:return: (mixed) Matching body multipart element; None if unneeded
:since:  v0.1.00
		"""

		for attachment_part in self.attachment_list: element.attach(attachment_part)
	#

	def add_body(self, part):
	#
		"""
Adds an e-Mail attachment related to the message body. Please note that RFC
defines an increasing priority for each body part added. That means the last
body should be the preferred representation.

:param params: Query parameters as dict
:param separator: Query parameter separator

:return: (mixed) Response data; Exception on error
:since:  v0.1.00
		"""

		if ((not isinstance(part, Part)) or part.get_part_type() != Part.TYPE_MESSAGE_BODY):
		#
			raise TypeError("Only parts of type message body can be added as body elements")
		#

		if (part not in self.body_list): self.body_list.append(part)
	#

	def add_body_related_attachment(self, part):
	#
		"""
Adds an e-Mail attachment related to the message body.

:param params: Query parameters as dict
:param separator: Query parameter separator

:return: (mixed) Response data; Exception on error
:since:  v0.1.00
		"""

		if (
			(not isinstance(part, Part)) or
			(
				part.get_part_type() != Part.TYPE_ATTACHMENT and
				part.get_part_type() != Part.TYPE_BINARY_ATTACHMENT and
				part.get_part_type() != Part.TYPE_BINARY_INLINE and
				part.get_part_type() != Part.TYPE_INLINE
			)
		):
		#
			raise TypeError("Only parts of type attachment can be added as body related elements")
		#

		if (part not in self.body_related_list): self.body_related_list.append(part)
	#

	def _add_body_to_multipart(self, element):
	#
		"""
Appends the body to the given element.

:return: (mixed) Matching body multipart element; None if unneeded
:since:  v0.1.00
		"""

		element.attach(self._get_body())
	#

	def as_string(self):
	#
		"""
Python.org: Return the entire formatted message as a string.

:return: (str)
:since:  v0.1.00
		"""

		self._populate_message()
		return self.message.as_string()
	#

	def _get_body(self):
	#
		"""
Returns the populated body element.

:return: (mixed) Matching body multipart element; None if unneeded
:since:  v0.1.00
		"""

		if (len(self.body_list) < 1): raise ValueError("No body has been defined")

		# First handle alternative representations of the body
		if (len(self.body_list) > 1):
		#
			body_root = Part(Part.TYPE_MULTIPART, "multipart/alternative")
			for body_part in self.body_list: body_root.attach(body_part)
		#
		else: body_root = self.body_list[0]

		# If related attachments are defined we will add them now
		if (len(self.body_related_list) > 0):
		#
			_return = Part(Part.TYPE_MULTIPART, "multipart/related")
			_return.attach(body_root)
			for related_part in self.body_related_list: _return.attach(related_part)
		#
		else: _return = body_root

		return _return
	#

	def _populate_message(self):
	#
		"""
Python.org: Return the entire formatted message as a string.

:return: (str)
:since:  v0.1.00
		"""

		self.message = (Part(Part.TYPE_MULTIPART, "multipart/mixed") if (len(self.attachment_list) > 0) else None)

		if (self.message == None): self.message = self._get_body()
		else: self._add_body_to_multipart(self.message)

		self._add_attachments_to_multipart(self.message)
	#
#

##j## EOF