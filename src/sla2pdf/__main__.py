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


def split_list(list, value, min_len=0):
    
    new = []
    sub = []
    
    for item in list:
        if item == value:
            new.append(sub)
            sub = []
        else:
            sub.append(item)
    
    new.append(sub)
    while len(new) < min_len:
        new.append([])
    
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


def _common_parser():
    parser = argparse.ArgumentParser(
        prog = "sla2pdf",
        description = "Export Scribus SLA documents to PDF from the command line",
    )
    parser.add_argument(
        "--version", "-v",
        action = "version",
        version = "sla2pdf %s" % V_SLA2PDF,
    )
    return parser


def parse_batch_args(argv):
    parser = _common_parser()
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
    
    return parser.parse_args(argv)


def parse_conv_args(argv):
    parser = _common_parser()
    parser.add_argument(
        "--show-gui",
        action = "store_true",
        help = "If given, show the Scribus GUI."
    )
    return parser.parse_args(argv)


def main():
    
    logger.addHandler( logging.StreamHandler() )
    logger.setLevel(logging.DEBUG)
    
    batch_argvs, conv_argv = split_list(sys.argv[1:], "--", 2)
    conv_args = parse_conv_args(conv_argv)
    
    batches = []
    for argv in split_list(batch_argvs, "-"):
        batch_args = parse_batch_args(argv)
        params = parse_params(batch_args.params)
        batch = dict(
            inputs = batch_args.inputs,
            outputs = batch_args.outputs,
            converter = batch_args.converter,
            params = params,
        )
        batches.append(batch)
    
    batch_convert(
        batches,
        hide_gui = not conv_args.show_gui,
    )


if __name__ == "__main__":
    main()
