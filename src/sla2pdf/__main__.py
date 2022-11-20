# PYTHON_ARGCOMPLETE_OK
# SPDX-FileCopyrightText: 2022 geisserml <geisserml@gmail.com>
# SPDX-License-Identifier: MPL-2.0

import logging
import argparse
from sla2pdf.runner import convert
from sla2pdf._parser import extend_parser
from sla2pdf._version import V_SLA2PDF

try:
    import argcomplete
except ImportError:
    argcomplete = None

logger = logging.getLogger('sla2pdf')


def parse_args():
    
    parser = argparse.ArgumentParser(
        prog = "sla2pdf",
        description = "Export Scribus SLA documents to PDF from the command line",
    )
    
    parser.add_argument(
        "--version", "-v",
        action = "version",
        version = "sla2pdf %s" % V_SLA2PDF,
    )
    parser.add_argument(
        "--outputs", "-o",
        nargs = "+",
        help = "Either an output directory, or a sequence of explicit output paths. Defaults to the current directory.",
    )
    extend_parser(parser)
    
    if argcomplete is not None:
        argcomplete.autocomplete(parser)
    
    return parser.parse_args()


def main():
    
    logger.addHandler( logging.StreamHandler() )
    logger.setLevel(logging.DEBUG)
    
    args = parse_args()
    
    convert(
        args.inputs, args.outputs,
        show_gui = args.show_gui,
        quality = args.quality,
        compression = args.compression,
        downsample = args.downsample,
    )


if __name__ == "__main__":
    main()
