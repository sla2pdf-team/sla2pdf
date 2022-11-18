# SPDX-FileCopyrightText: 2022 geisserml <geisserml@gmail.com>
# SPDX-License-Identifier: MPL-2.0
# -- This code needs to remain compatible with Py2 --

from sla2pdf.constants import *


def _get_type(enum):
    return lambda val: enum[val.upper()]

def _get_choices(enum):
    return [member.name.lower() for member in list(enum)]


def extend_parser(parser):
    parser.add_argument(
        "inputs",
        nargs = "+",
    )
    parser.add_argument(
        "--show-gui",
        action = "store_true",
        help = "Show the Scribus GUI",
    )
    parser.add_argument(
        "--compression",
        type = _get_type(ImageCompression),
        default = ImageCompression.JPEG,
        help = "Image compression method %s" % _get_choices(ImageCompression),
    )
    parser.add_argument(
        "--quality",
        type = _get_type(ImageQuality),
        default = ImageQuality.HIGH,
        help = "Image quality %s" % _get_choices(ImageQuality),
    )
    parser.add_argument(
        "--downsample",
        default = 400,
        type = int,
        help = "Limit image resolution to the given DPI value",
    )
