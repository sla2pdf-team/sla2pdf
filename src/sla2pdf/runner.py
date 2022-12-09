# SPDX-FileCopyrightText: 2022 geisserml <geisserml@gmail.com>
# SPDX-License-Identifier: MPL-2.0

__all__ = ["batch_convert"]

import shutil
import logging
import subprocess
from pathlib import Path
from tempfile import NamedTemporaryFile

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
    cmd += ["--python-script", Converter, ModuleDir.parent] + args
    
    cmd = [str(c) for c in cmd]
    logger.info(cmd)
    
    subprocess.run(cmd, check=True, cwd=str(Path.cwd()))


def _handle_paths(inputs, outputs, converter, ext):
    
    inputs  = [Path(p).expanduser().resolve() for p in inputs]
    missing = [p for p in inputs if not p.is_file()]
    if len(missing) > 0:
        raise FileNotFoundError("The following inputs could not be found: %s" % (missing, ))
    
    if not isinstance(outputs, (tuple, list)):
        outputs = [outputs]
    outputs = [Path(p).expanduser().resolve() for p in outputs]
    
    if converter == "img":
        assert all(p.is_dir() for p in outputs)
        while len(outputs) < len(inputs):
            outputs.append(outputs[-1])
    else:
        if len(outputs) == 1 and outputs[0].is_dir():
            outputs = [(outputs[0] / p.name).with_suffix("."+ext) for p in inputs]
        assert all(p.suffix.endswith("."+ext) for p in outputs)
    
    assert len(inputs) == len(outputs)
    
    return inputs, outputs


#: Default PDF saving parameters.
DefaultParamsPdf = dict(
    compress = True,
    compressmtd = 0,  # automatic
    quality = 1,      # high
    resolution = 300,
    downsample = 300,
)


#: Default image saving parameters.
DefaultParamsImg = dict(
    dpi = 300,
    quality = 100,
    scale = 100,
    transparentBkgnd = False,
    type = "PNG",
)


ConverterToDefaultParams = {
    "pdf": DefaultParamsPdf,
    "img": DefaultParamsImg,
}


def _get_tasks(
        inputs,
        outputs,
        converter = "pdf",
        params = {},
    ):
    
    converter = converter.lower()
    conv_params = ConverterToDefaultParams[converter].copy()
    conv_params.update(params)
    
    if converter == "img":
        ext = conv_params["type"].lower()
    else:
        ext = converter
    
    inputs, outputs = _handle_paths(inputs, outputs, converter, ext)
    args = inputs + ["-o"] + outputs + ["-p", conv_params, "-c", converter]
    args = [str(arg) for arg in args]
    
    info = (converter, outputs)
    
    return args, info


def batch_convert(batches, hide_gui=True):
    
    infos = []
    tmp_handle = NamedTemporaryFile(prefix="sla2pdf_", suffix=".txt")
    
    for batch in batches:
        task, info = _get_tasks(**batch)
        logger.info(task)
        tmp_handle.write(str(task).encode() + b"\n")
        infos.append(info)
    
    tmp_handle.seek(0)
    run_scribus([tmp_handle.name], hide_gui=hide_gui)
    tmp_handle.close()
    
    for converter, outputs in infos:
        if converter == "img":
            assert all(p.is_dir() for p in outputs)
        elif converter == "pdf":
            assert all(p.is_file() for p in outputs)
