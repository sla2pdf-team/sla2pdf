# SPDX-FileCopyrightText: 2022 geisserml <geisserml@gmail.com>
# SPDX-License-Identifier: MPL-2.0
# -- This code needs to remain compatible with Py2 --

try:
    import scribus
except ImportError:
    raise RuntimeError("This script must be called from within Scribus.")

import sys
import ast
import argparse
from os.path import join, basename, splitext

# The path of the directory containing the sla2pdf module is always passed as first positional argument and excluded from following parsing
# This would allow us to use local imports even in this part which runs inside Scribus
# Note that we cannot use __file__ because some Scribus builds do not define it
ModuleParDir = sys.argv[1]
sys.path.insert(0, ModuleParDir)


def parse_args(argv=sys.argv[2:]):
    
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
        "--converter", "-c",
        choices = ("pdf", "img"),
        required = True,
    )
    parser.add_argument(
        "--params", "-p",
        required = True,
        type = ast.literal_eval,
    )
    
    return parser.parse_args(argv)


def _set_params(exporter, params):
    [setattr(exporter, k, v) for k, v in params.items() if v is not None]


def main():
    
    args = parse_args()
    
    for in_path, out in zip(args.inputs, args.outputs):
        
        scribus.openDoc(in_path)
        
        if args.converter == "img":
            
            exporter = scribus.ImageExport()
            
            n_pages = scribus.pageCount()
            n_digits = len(str(n_pages))
            prefix = splitext(basename(in_path))[0]
            suffix = args.params["type"].lower()
            
            for n in range(1, n_pages+1):
                scribus.gotoPage(n)
                exporter = scribus.ImageExport()
                _set_params(exporter, args.params)
                exporter.saveAs( join(out, "%s_%0*d.%s" % (prefix, n_digits, n, suffix)) )
        
        elif args.converter == "pdf":
            
            exporter = scribus.PDFfile()
            
            _set_params(exporter, args.params)
            exporter.file = out
            exporter.save()
        
        else:
            raise Exception()  # supposed to be unreachable
        
        scribus.closeDoc()


if __name__ == "__main__":
    main()
