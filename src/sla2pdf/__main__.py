# PYTHON_ARGCOMPLETE_OK
# SPDX-FileCopyrightText: 2022 geisserml <geisserml@gmail.com>
# SPDX-License-Identifier: MPL-2.0

import os
import logging
import argparse
from os.path import (
    join,
    isdir,
    abspath,
    splitext,
    basename,
    expanduser,
)
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
        "--output-dir", "-o",
        default = os.getcwd(),
        help = "Output directory",
    )
    extend_parser(parser)
    
    if argcomplete is not None:
        argcomplete.autocomplete(parser)
    
    return parser.parse_args()


def main():
    
    logger.addHandler( logging.StreamHandler() )
    logger.setLevel(logging.DEBUG)
    
    args = parse_args()
    
    input_paths = args.inputs
    output_dir = abspath(expanduser(args.output_dir))
    if not isdir(output_dir):
        raise ValueError("Directory does not exist: '%s'" % output_dir)
    
    output_paths = []
    for inpath in input_paths:
        out_name = splitext(basename(inpath))[0] + ".pdf"
        output_paths.append( join(output_dir, out_name) )
    
    convert(
        input_paths, output_paths,
        show_gui = args.show_gui,
        quality = args.quality,
        compression = args.compression,
        downsample = args.downsample,
    )


if __name__ == "__main__":
    main()
