# SPDX-FileCopyrightText: 2022 geisserml <geisserml@gmail.com>
# SPDX-License-Identifier: MPL-2.0
# -- This code needs to remain compatible with Py2 --

from enum import Enum


class ImageQuality (Enum):
    MAXIMUM = 0
    HIGH    = 1
    MEDIUM  = 2
    LOW     = 3
    MINIMUM = 4


class ImageCompression (Enum):
    AUTO = 0
    JPEG = 1
    ZIP  = 2
    NONE = 3
