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
Converter = ModuleDir / "_converter.py"
Scribus = shutil.which("scribus")


def run_scribus(args, hide_gui=True):
    
    if Scribus is None:
        raise RuntimeError("Scribus could not be found.")
    
    cmd = [Scribus, "--no-gui", "--no-splash"]
    if hide_gui:
        cmd += ["-platform", "offscreen"]
    cmd += ["--python-script", Converter, ModuleDir.parent]
    cmd += args
    
    cmd = [str(c) for c in cmd]
    logger.info(cmd)
    
    subprocess.run(cmd, check=True, cwd=os.getcwd())


def _handle_paths(inputs, outputs):
    
    in_paths  = [Path(p).expanduser().resolve() for p in inputs]
    missing_ins = [p for p in in_paths if not p.is_file()]
    if len(missing_ins) > 0:
        raise FileNotFoundError("The following inputs could not be found: %s" % (missing_ins, ))
    
    output_dir = None
    if isinstance(outputs, (str, Path)):
        output_dir = Path(outputs)
    elif len(outputs) == 1 and Path(outputs[0]).is_dir():
        output_dir = Path(outputs[0]).expanduser().resolve()
    
    if output_dir is None:
        out_paths = [Path(p).expanduser().resolve() for p in outputs]
    else:
        if not output_dir.is_dir():
            raise NotADirectoryError(output_dir)
        out_paths = [(output_dir / p.name).with_suffix(".pdf") for p in in_paths]
    
    if len(in_paths) != len(out_paths):
        raise ValueError("Length of inputs and outputs does not match (%s != %s)" % (len(in_paths), len(out_paths)))
    
    if not all(p.suffix.lower() == ".pdf" for p in out_paths):
        raise ValueError("Not all output paths terminated with '.pdf' suffix")
    
    return in_paths, out_paths


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
        outputs,
        params = {},
        hide_gui = True,
    ):
    """
    Parameters:
        inputs (list[str|pathlib.Path]):
            List of input file paths (Scribus SLA documents).
        outputs (str | pathlib.Path | list[str|pathlib.Path]):
            Output directory or list of explicit output paths for the PDF files to generate.
        params (dict):
            Dictionary of saving parameters (see the Scribus Scripter PDFfile API).
        hide_gui (bool):
            If True, the Scribus GUI will be hidden using ``QT_QPA_PLATFORM=offscreen``.
            Otherwise, it will be shown.
    """
    
    inputs, outputs = _handle_paths(inputs, outputs)
    
    conv_params = DefaultParams.copy()
    conv_params.update(params)
    
    args = inputs + ["-o"] + outputs + ["-p", conv_params]
    run_scribus(args, hide_gui=hide_gui)
    
    missing_outs = [p for p in outputs if not p.is_file()]
    if len(missing_outs) > 0:
        raise RuntimeError("The following outputs were not generated: %s" % missing_outs)
