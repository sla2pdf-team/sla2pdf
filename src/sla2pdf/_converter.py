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

# The path of the directory containing the sla2pdf module is always passed as first positional argument and excluded from following parsing
# This would allow us to use local imports even in this part which runs inside Scribus
# Note that we cannot use __file__ because Scribus might not necessarily define it (esp. older versions)
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
        "--params", "-p",
        required = True,
        type = ast.literal_eval,
    )
    
    return parser.parse_args(argv)


def main():
    
    args = parse_args()
    
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
    main()
