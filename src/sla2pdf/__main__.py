# SPDX-FileCopyrightText: 2022 geisserml <geisserml@gmail.com>
# SPDX-License-Identifier: MPL-2.0

import sys
import ast
import logging
import argparse
from pathlib import Path
from sla2pdf.runner import batch_convert
from sla2pdf._version import V_SLA2PDF

logger = logging.getLogger('sla2pdf')


def split_list(list, value):
    
    new = []
    sub = []
    
    for item in list:
        if item == value and len(sub) > 0:
            new.append(sub)
            sub = []
        else:
            sub.append(item)
    
    if len(sub) > 0:
        new.append(sub)
    
    return new


def parse_params(params_list):
    
    params_dict = {}
    
    for param in params_list:
        
        key, value = param.split("=", maxsplit=1)
        key, value = key.strip(), value.strip()
        
        if value.isnumeric():
            value = int(value)
        elif value.replace(".", "", 1).isdigit():
            value = float(value)
        elif value.lower() in ("true", "false", "none"):
            value = ast.literal_eval(value.lower().capitalize())
        elif value[0] in ("(", "[", "{"):
            value = ast.literal_eval(value)
        
        params_dict[key] = value
    
    return params_dict


def parse_args(part):
    
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
        default = Path.cwd(),
        help = "An output directory, or a sequence of explicit output paths. Defaults to the current directory.",
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
    
    return parser.parse_args(part)


def main():
    
    logger.addHandler( logging.StreamHandler() )
    logger.setLevel(logging.DEBUG)
    
    batches = []
    for part in split_list(sys.argv[1:], "-"):
        args = parse_args(part)
        params = parse_params(args.params)
        batch = dict(
            inputs = args.inputs,
            outputs = args.outputs,
            converter = args.converter,
            params = params,
        )
        batches.append(batch)
    
    # TODO think about how to pass common arguments
    batch_convert(batches)


if __name__ == "__main__":
    main()
