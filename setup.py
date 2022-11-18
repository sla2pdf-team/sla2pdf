# SPDX-FileCopyrightText: 2022 geisserml <geisserml@gmail.com>
# SPDX-License-Identifier: MPL-2.0

import setuptools
from os.path import join, dirname

def get_version():
    ver_namespace = {}
    VersionFile = join(dirname(__file__), "src", "sla2pdf", "_version.py")
    with open(VersionFile, "r") as fh:
        exec(fh.read(), ver_namespace)
    return ver_namespace["V_SLA2PDF"]

setuptools.setup(
    version = get_version(),
)
