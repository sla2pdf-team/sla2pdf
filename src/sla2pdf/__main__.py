# SPDX-FileCopyrightText: 2025 geisserml <geisserml@gmail.com>
# SPDX-License-Identifier: MPL-2.0

import sys
import ast
import logging
import argparse
from pathlib import Path
from sla2pdf.runner import batch_convert
from sla2pdf._version import V_SLA2PDF

logger = logging.getLogger('sla2pdf')


def parse_args(argv):
    parser = argparse.ArgumentParser(
        prog = "sla2pdf",
        description = "Export Scribus SLA documents to PDF from the command line. Multiple argument sets may be given, separated by `-`.",
    )
    parser.add_argument(
        "--version", "-v",
        action = "version",
        version = f"sla2pdf {V_SLA2PDF}",
    )
    parser.add_argument(
        "inputs",
        nargs = "+",
    )
    parser.add_argument(
        "--outputs", "-o",
        nargs = "+",
        default = Path.cwd(),
        help = "For pdf: A directory, or sequence of explicit paths. For img: A directory, or sequence of directories.",
    )
    parser.add_argument(
        "--converter", "-c",
        default = "pdf",
        choices = ("pdf", "img"),
        help = "The converter to use.",
    )
    parser.add_argument(
        "--params", "-p",
        nargs = "+",
        default = [],
        help = "A sequence of Scribus key=value PDF saving paramters (see the Scribus Scripter docs).",
    )
    parser.add_argument(
        "--show-gui",
        action = "store_true",
        help = "If given, show the Scribus GUI (global option)."
    )
    return parser.parse_args(argv)


def split_list(list, value):
    new, sub = [], []
    for item in list:
        if item == value:
            new.append(sub)
            sub = []
        else:
            sub.append(item)
    new.append(sub)
    return new


def parse_params(params_list):
    
    params_dict = {}
    
    for param in params_list:
        
        key, value = param.split("=", maxsplit=1)
        key, value = key.strip(), value.strip()
        
        # Don't use literal_eval() generally, we want to allow non-quoted strings to align with command-line interpreter semantics. Instead, handle the cases that need to be eval'ed explicitly.
        if value.lower() in ("true", "false", "none"):
            value = ast.literal_eval(value.lower().capitalize())
        elif ( value[0] in ("(", "[", "{", "'", '"')
            or value[:2] in ("b'", 'b"')
            or value.isnumeric() or value.replace(".", "", 1).isdigit()
            ):
            value = ast.literal_eval(value)
        
        params_dict[key] = value
    
    return params_dict


def main():
    
    logger.addHandler( logging.StreamHandler() )
    logger.setLevel(logging.DEBUG)
    
    # TODO see if we can implement global options in a better way
    show_gui = False
    
    batches = []
    for argv in split_list(sys.argv[1:], "-"):
        args = parse_args(argv)
        params = parse_params(args.params)
        batch = dict(
            inputs = args.inputs,
            outputs = args.outputs,
            converter = args.converter,
            params = params,
        )
        batches.append(batch)
        if args.show_gui:
            show_gui = True
    
    batch_convert(
        batches,
        hide_gui = not show_gui,
    )


if __name__ == "__main__":
    main()
