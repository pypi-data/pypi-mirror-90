# Copyright 2005-2015 Canonical Ltd.  This software is licensed under
# the GNU Affero General Public License version 3 (see the file LICENSE).

from __future__ import absolute_import

from txpkgupload.plugin import PkgUploadServiceMaker

# Construct objects which *provide* the relevant interfaces. The name of
# these variables is irrelevant, as long as there are *some* names bound to
# providers of IPlugin and IServiceMaker.

service_pkgupload = PkgUploadServiceMaker(
    "pkgupload", "A package upload frontend server.")
