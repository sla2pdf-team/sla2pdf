# PYTHON_ARGCOMPLETE_OK
# SPDX-FileCopyrightText: 2022 geisserml <geisserml@gmail.com>
# SPDX-License-Identifier: MPL-2.0

import ast
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
        help = "A sequence of Scribus key=value PDF saving paramters (see the Scribus Scripter docs).",
    )
    
    if argcomplete is not None:
        argcomplete.autocomplete(parser)
    
    return parser.parse_args()


def _parse_params(params_list):
    
    params_dict = {}
    
    for param in params_list:
        
        key, value = param.split("=", maxsplit=1)
        key, value = key.strip(), value.strip()
        value_lc = value.lower()
        
        if value.isnumeric():
            value = int(value)
        elif value_lc == "true":
            value = True
        elif value_lc == "false":
            value = False
        elif value_lc == "none":
            value = None
        elif not value.isalnum():
            value = ast.literal_eval(value)
        
        params_dict[key] = value
    
    return params_dict


def main():
    
    logger.addHandler( logging.StreamHandler() )
    logger.setLevel(logging.DEBUG)
    
    args = parse_args()
    convert(
        args.inputs, args.outputs,
        hide_gui = not args.show_gui,
        params = _parse_params(args.params),
    )


if __name__ == "__main__":
    main()
