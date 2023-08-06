# Copyright (C) 2015 Sebastian Pipping <sebastian@pipping.org>
# Licensed under AGPL v3 or later

PACKAGE_NAME = 'image-bootstrap'

GITHUB_HOME_URL = 'https://github.com/hartwork/image-bootstrap'

DESCRIPTION = 'Command line tool for creating bootable virtual machine images'

_VERSION = (2, 0, 5)
VERSION_STR = '.'.join((str(e) for e in _VERSION))

_RELEASE_DATE = (2021, 1, 8)
RELEASE_DATE_STR = '-'.join(('%02d' % e for e in _RELEASE_DATE))
