# PYTHON_ARGCOMPLETE_OK
# SPDX-FileCopyrightText: 2022 geisserml <geisserml@gmail.com>
# SPDX-License-Identifier: MPL-2.0

import logging
import argparse
from sla2pdf.runner import convert
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
        "inputs",
        nargs = "+",
    )
    parser.add_argument(
        "--outputs", "-o",
        nargs = "+",
        help = "An output directory, or a sequence of explicit output paths. Defaults to the current directory.",
    )
    parser.add_argument(
        "--show-gui",
        action = "store_true",
        help = "Show the Scribus GUI",
    )
    parser.add_argument(
        "--params", "-p",
        nargs = "+",
        default = [],
        help = "A sequence of Scribus key=value PDF saving paramters (see the Scribus Scripter docs). Values can be interpreted as integers, booleans or strings.",
    )
    
    if argcomplete is not None:
        argcomplete.autocomplete(parser)
    
    return parser.parse_args()


def _parse_value(value):
    value = value.strip()
    if value.isnumeric():
        return int(value)
    elif value.lower() in ("true", "false"):
        return bool(value.lower().capitalize())
    elif value[0] == "[" and value[-1] == "]":
        return [_parse_value(v) for v in value[1:-1].split(",")]


def main():
    
    logger.addHandler( logging.StreamHandler() )
    logger.setLevel(logging.DEBUG)
    
    args = parse_args()
    
    # TODO consider just parsing with ast.literal_eval() instead?
    params = {}
    for param in args.params:
        key, value = param.split("=", maxsplit=1)
        key = key.strip()
        params[key] = _parse_value(value)
        
    convert(
        args.inputs, args.outputs,
        hide_gui = not args.show_gui,
        params = params,
    )


if __name__ == "__main__":
    main()
