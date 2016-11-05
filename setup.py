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
setup.py
"""

def get_version():
    """
Returns the version currently in development.

:return: (str) Version string
:since:  v0.1.02
    """

    return "v0.1.02"
#

from dNG.distutils.command.build_py import BuildPy
from dNG.distutils.temporary_directory import TemporaryDirectory

from distutils.core import setup
from os import path

with TemporaryDirectory(dir = ".") as build_directory:
    parameters = { "pyRfcEMailVersion": get_version() }

    BuildPy.set_build_target_path(build_directory)
    BuildPy.set_build_target_parameters(parameters)

    _build_path = path.join(build_directory, "src")

    setup(name = "RFC e-mail for Python",
          version = get_version(),
          description = "An abstracted programming interface to generate e-mails",
          long_description = """RFC e-mail extends the Python integrated "email" package with an easy to use abstraction layer to construct e-mails with alternative bodies and attachments.""",
          author = "direct Netware Group et al.",
          author_email = "web@direct-netware.de",
          license = "MPL2",
          url = "https://www.direct-netware.de/redirect?py;rfc_email",

          platforms = [ "any" ],

          package_dir = { "": _build_path },
          packages = [ "dNG" ],

          data_files = [ ( "docs", [ "LICENSE", "README" ]) ],

          # Override build_py to first run builder.py over all PAS modules
          cmdclass = { "build_py": BuildPy }
         )
#
