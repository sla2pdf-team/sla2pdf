<!-- SPDX-FileCopyrightText: 2022 geisserml <geisserml@gmail.com> -->
<!-- SPDX-License-Identifier: CC-BY-4.0 -->

# Tasks

* move auto-naming implementation from CLI to Python API (accept both directory or explicit paths)
* add ability to set any attribute on the Scribus PDFFile object using a key-value sequence and `setattr()`
* avoid parsing arguments twice and pass options to scribus in a single key-value string
* runner/converter: handle parameters on a per-document basis
* make downsampling optional, also think about making conversion lossless by default
* add tests and documentation
* switch to pathlib (in the python 3 part)
* cli: use argparse choices parameter
