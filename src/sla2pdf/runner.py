# SPDX-FileCopyrightText: 2022 geisserml <geisserml@gmail.com>
# SPDX-License-Identifier: MPL-2.0

import os
import shutil
import logging
import subprocess
from os.path import (
    join,
    isfile,
    dirname,
    abspath,
    expanduser,
)
from sla2pdf.constants import (
    ImageQuality,
    ImageCompression,
)

logger = logging.getLogger(__name__)


Converter = join(dirname(__file__), "_converter.py")
Scribus = shutil.which("scribus")


def _run_command(command):
    command = [str(c) for c in command]
    logger.info(command)
    subprocess.run(command, check=True, cwd=os.getcwd())


def convert(
        input_paths,
        output_paths,
        show_gui = False,
        quality = ImageQuality.HIGH,
        compression = ImageCompression.JPEG,
        downsample = 400,
    ):
    
    if Scribus is None:
        raise RuntimeError("Scribus could not be found.")
    
    input_paths  = [abspath(expanduser(p)) for p in input_paths]
    output_paths = [abspath(expanduser(p)) for p in output_paths]
    
    missing_inputs = [p for p in input_paths if not isfile(p)]
    if len(missing_inputs) > 0:
        raise FileNotFoundError("The following inputs could not be found: %s" % missing_inputs)
    
    command = [Scribus, "--no-gui", "--no-splash"]
    if not show_gui:
        command += ["-platform", "offscreen"]
    
    command += ["--python-script", Converter]
    command += input_paths
    command += ["-o"] + output_paths
    command += ["--compression", compression.name]
    command += ["--quality", quality.name]
    command += ["--downsample", downsample]
    
    _run_command(command)
    
    missing_outputs = [p for p in output_paths if not isfile(p)]
    if len(missing_outputs) > 0:
        raise RuntimeError("The following outputs were not generated: %s" % missing_outputs)
