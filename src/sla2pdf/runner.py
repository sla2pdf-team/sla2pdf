# SPDX-FileCopyrightText: 2022 geisserml <geisserml@gmail.com>
# SPDX-License-Identifier: MPL-2.0

import os
import shutil
import logging
import subprocess
from pathlib import Path
from sla2pdf.constants import (
    ImageQuality,
    ImageCompression,
)

logger = logging.getLogger(__name__)


Converter = Path(__file__).resolve().parent / "_converter.py"
Scribus = shutil.which("scribus")


def _run_command(command):
    command = [str(c) for c in command]
    logger.info(command)
    subprocess.run(command, check=True, cwd=os.getcwd())


def convert(
        inputs,
        outputs = None,
        show_gui = False,
        quality = ImageQuality.HIGH,
        compression = ImageCompression.JPEG,
        downsample = 400,
    ):
    
    if Scribus is None:
        raise RuntimeError("Scribus could not be found.")
    
    input_paths  = [Path(p).expanduser().resolve() for p in inputs]
    missing_inputs = [p for p in input_paths if not p.is_file()]
    if len(missing_inputs) > 0:
        raise FileNotFoundError("The following inputs could not be found: %s" % (missing_inputs, ))
    
    output_dir = None
    if not outputs:
        output_dir = Path.cwd()
    elif len(outputs) == 1 and Path(outputs[0]).is_dir():
        output_dir = Path(outputs[0]).expanduser().resolve()
    
    if output_dir is None:
        output_paths = [Path(p).expanduser().resolve() for p in outputs]
    else:
        output_paths = [(output_dir / p.name).with_suffix(".pdf") for p in input_paths]
    
    if len(input_paths) != len(output_paths):
        raise ValueError("Length of inputs and outputs does not match (%s != %s)" % (len(input_paths), len(output_paths)))
    
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
    
    missing_outputs = [p for p in output_paths if not p.is_file()]
    if len(missing_outputs) > 0:
        raise RuntimeError("The following outputs were not generated: %s" % missing_outputs)
