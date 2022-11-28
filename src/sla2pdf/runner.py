# SPDX-FileCopyrightText: 2022 geisserml <geisserml@gmail.com>
# SPDX-License-Identifier: MPL-2.0

__all__ = ["convert"]

import os
import shutil
import logging
import subprocess
from pathlib import Path

logger = logging.getLogger(__name__)

ModuleDir = Path(__file__).resolve().parent
ModuleParDir = ModuleDir.parent
Converter = ModuleDir / "_converter.py"
Scribus = shutil.which("scribus")


def _run_command(command):
    command = [str(c) for c in command]
    logger.info(command)
    subprocess.run(command, check=True, cwd=os.getcwd())


#: Default PDF saving parameters.
DefaultParams = dict(
    compress = True,
    compressmtd = 0,  # automatic
    quality = 1,      # high
    resolution = 300,
    downsample = 300,
)


def convert(
        inputs,
        outputs = None,
        hide_gui = True,
        params = {},
    ):
    """
    Parameters:
        inputs (typing.Sequence[str|pathlib.Path]):
            List of input file paths (Scribus SLA documents).
        outputs (str | pathlib.Path | typing.Sequence[str|pathlib.Path]):
            Output directory or list of explicit output paths for the PDF files to generate.
        hide_gui (bool):
            If True, the Scribus GUI will be hidden using ``QT_QPA_PLATFORM=offscreen``.
            Otherwise, it will be shown.
        params (dict):
            Dictionary of saving parameters (see the Scribus Scripter PDFfile API).
    """
    
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
    
    conv_params = DefaultParams.copy()
    conv_params.update(params)
    
    command = [Scribus, "--no-gui", "--no-splash"]
    if hide_gui:
        command += ["-platform", "offscreen"]
    
    command += ["--python-script", Converter]
    command += [ModuleParDir]
    command += input_paths
    command += ["-o"] + output_paths
    command += ["-p", conv_params]
    
    _run_command(command)
    
    missing_outputs = [p for p in output_paths if not p.is_file()]
    if len(missing_outputs) > 0:
        raise RuntimeError("The following outputs were not generated: %s" % missing_outputs)
