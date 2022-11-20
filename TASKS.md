<!-- SPDX-FileCopyrightText: 2022 geisserml <geisserml@gmail.com> -->
<!-- SPDX-License-Identifier: CC-BY-4.0 -->

# Tasks

* Support output formats other than PDF (in spite of the project's name).
* Support image export (complicated because 1 input will result in multiple outputs).
  Besides, we're not sure if Scribus's API supports exporting pages other than the first.
* Think about some kind of abstraction around Scribus's API, at places where it makes sense.
* runner/converter: handle parameters on a per-dcument basis, at least in the Python API
* Improve default parameters, consider using lossless conversion by default
* Improve the readme
* Add tests and sphinx documentation
