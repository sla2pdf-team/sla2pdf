<!-- SPDX-FileCopyrightText: 2022 geisserml <geisserml@gmail.com> -->
<!-- SPDX-License-Identifier: CC-BY-4.0 -->

# sla2pdf

Convert Scribus SLA documents to PDF, using the command line or Python API.
Runs Scribus in a subprocess with a custom Python script.

## Installation

sla2pdf can be installed via `pip`, like any other Python project:

Normal installation (copies a snapshot of the code to a python package directory)
```bash
pip install .
```

Development installation (points to the source tree, so changes take effect without needing to re-install)
```bash
pip install -e .
```

In principle, it is also possible to install sla2pdf without setup tooling (Linux instructions):
* Append the absolute path to `sla2pdf/src` to the environment variable `PYTHONPATH`
  by adding `export PYTHONPATH=${PYTHONPATH}:${HOME}/.../sla2pdf/src` to `~/.bashrc`
* Save the code below as `sla2pdf` in `~/.local/bin/`:
  ```python
  #! /usr/bin/env python3
  import sla2pdf.__main__
  
  if __name__ == "__main__":
      sla2pdf.__main__.main()
  ```

If you have multiple versions of Python 3 installed, note that any of them can be used to install sla2pdf.
It does not necessarily need to be the one Scribus is linked against, as the module of
sla2pdf that is run within Scribus will automatically configure its search path appropriately.

## Usage

### Command-line
<!-- TODO -->

### Python API

```python
from sla2pdf.runner import convert

convert(
    ["path/to/input.sla", ...],   # sequence of input documents
    ["path/to/output.pdf", ...],  # sequence of output paths
)
```


## Behaviour

sla2pdf uses lossy image compression by default, to prevent the resulting files from getting too large.
Quality settings can be controlled precisely using command-line options.


## Development

Relevant Scribus links:

* https://scribus.net/websvn/filedetails.php?repname=Scribus&path=%2Ftrunk%2FScribus%2Fdoc%2Fen%2Fscripterapi-doc.html
* https://scribus.net/websvn/filedetails.php?repname=Scribus&path=%2Ftrunk%2FScribus%2Fdoc%2Fen%2Fscripterapi-PDFfile.html
* https://scribus.net/websvn/listing.php?repname=Scribus&path=%2Ftrunk%2FScribus%2Fdoc%2Fen%2F&#af20fbfeebfcfd73863fd3438754d4fed
* https://wiki.scribus.net/canvas/Command_line_scripts
* https://github.com/scribusproject/scribus/tree/master/scribus/plugins/scripter
* https://bugs.scribus.net/view.php?id=16355


### Python 2 Compatibility Notice

Several files show the following notice:
```python
# -- This code needs to remain compatible with Py2 --
```
That is because the file in question is run inside Scribus (either directly, or indirectly through imports).
Some mainstream Scribus distributions are still built with Python 2, so we intend to keep compatibility for the time being.
