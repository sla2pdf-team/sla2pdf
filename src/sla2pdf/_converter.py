# SPDX-FileCopyrightText: 2022 geisserml <geisserml@gmail.com>
# SPDX-License-Identifier: MPL-2.0
# -- This code needs to remain compatible with Py2 --

import sys
import ast
import argparse

try:
    import scribus
except ImportError:
    raise RuntimeError("This script must be called from within Scribus.")


def parse_args(argv=sys.argv[1:]):
    
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "inputs",
        nargs = "+",
    )
    parser.add_argument(
        "--outputs", "-o",
        required = True,
        nargs = "+",
    )
    parser.add_argument(
        "--params", "-p",
        required = True,
        type = ast.literal_eval,
    )
    
    return parser.parse_args(argv)


def sla_to_pdf(args):
    
    for in_path, out_path in zip(args.inputs, args.outputs):
        
        scribus.openDoc(in_path)
        pdf = scribus.PDFfile()
        
        for key, value in args.params.items():
            if value is not None:
                setattr(pdf, key, value)
        
        pdf.file = out_path
        pdf.save()
        scribus.closeDoc()


if __name__ == "__main__":
    sla_to_pdf( parse_args() )
