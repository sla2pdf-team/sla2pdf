<!-- SPDX-FileCopyrightText: 2026 geisserml <geisserml@gmail.com> -->
<!-- SPDX-License-Identifier: CC-BY-4.0 -->

# sla2pdf

Convert Scribus SLA documents to PDF, using the command line or Python API.
Runs Scribus in a subprocess with a custom Python script.

## Installation

sla2pdf may be installed via `pip`, like any other Python project:

Normal installation (copies a snapshot of the code to a python package directory)
```bash
pip install .
```

Development installation (points to the source tree, so changes take effect without needing to re-install)
```bash
pip install -e .
```

If you have multiple Python interpreters installed, any of them can host sla2pdf.
It does not necessarily need to be the one Scribus is linked against.

sla2pdf's frontend requires Python 3.
The backend that runs inside Scribus is still supposed to be Python 2 compatible, so that sla2pdf may also work with older distributions. See [the note below](#python-2-compatibility-notice).


## Examples

### Command Line

* Export to PDF, placing outputs in the current directory
```bash
sla2pdf file1.sla file2.sla
```

* Export files with explicit output paths
```
sla2pdf file1.sla file2.sla -o out1.pdf out2.pdf
```

* Match SLA files by wildcard and export them to the directory `out/`
```bash
sla2pdf *.sla -o out/
```

* Export to PDF with parameters
  
  The parser accepts integers, floats, booleans (case-insensitive), lists, tuples, dictionaries and byte strings in Python syntax. Anything else is interpreted as string.
  String interpretation may also be enforced with quotes (use `\` escaping as necessary).

```bash
sla2pdf file1.sla --params compress=true compressmtd=1 quality=2 version=16
```

* Export to image
```bash
sla2pdf file1.sla file2.sla -c img -o out1/ out2/ --params type=JPG
```

* Run multiple tasks, separated by `-` (avoids re-starting scribus)
```bash
sla2pdf file1.sla - file2.sla --params quality=2 - file2.sla -c img out/
```


### Python API

Basic batch conversion usage:

```python
from sla2pdf.runner import batch_convert

pdf_params = dict(
    compressmtd = 1,  # JPEG
    quality = 2,      # Medium
    version = 16,     # PDF 1.6 standard
)
pdf_task = dict(
    inputs = ("file1.sla", "file2.sla"),  # input files
    outputs = ("out1.pdf", "out2.pdf"),   # output dests (file paths, or a dir)
    converter = "pdf",    # pdf mode
    params = pdf_params,  # custom pdf export parameters
)

img_params = dict(
    dpi = 300,                # resultion
    transparentBkgnd = True,  # transparent background
    type = "PNG",             # image format
)
img_task = dict(
    inputs = ("file3.sla", "file4.sla"),  # input files
    outputs = ("out3/", "out4/"),         # output dests (sequence of dirs)
    converter = "img",    # image mode
    params = img_params,  # custom image export parameters
),

batch_convert([pdf_task, img_task], hide_gui=True)  # run it
```


## Behaviour

sla2pdf uses lossy image compression by default. Quality settings can be controlled using the `--params` option.


## Development

Relevant Scribus links:

* https://scribus.net/websvn/filedetails.php?repname=Scribus&path=%2Ftrunk%2FScribus%2Fdoc%2Fen%2Fscripterapi-doc.html
* https://scribus.net/websvn/filedetails.php?repname=Scribus&path=%2Ftrunk%2FScribus%2Fdoc%2Fen%2Fscripterapi-page.html
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
Some people known to the author are still using Scribus builds that use Python 2 (e.g. from Ubuntu 20.04), so we intend to preserve compatibility for the time being.
