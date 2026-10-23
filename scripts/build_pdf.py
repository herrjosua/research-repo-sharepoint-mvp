"""Word -> PDF with LibreOffice (headless). Requests a tagged PDF so structure is kept."""
from __future__ import annotations

import shutil
import subprocess
from pathlib import Path

TAGGED = 'pdf:writer_pdf_Export:{"UseTaggedPDF":{"type":"boolean","value":"true"}}'


def build_pdf(docx: Path, out: Path, profile_dir: Path) -> Path:
    soffice = shutil.which("soffice") or shutil.which("libreoffice")
    if not soffice:
        raise RuntimeError("LibreOffice (soffice) is required for the PDF step")
    out.parent.mkdir(parents=True, exist_ok=True)
    profile_dir.mkdir(parents=True, exist_ok=True)
    cmd = [soffice, f"-env:UserInstallation=file://{profile_dir}", "--headless",
           "--convert-to", TAGGED, "--outdir", str(out.parent), str(docx)]
    res = subprocess.run(cmd, capture_output=True, text=True, timeout=180)
    produced = out.parent / (docx.stem + ".pdf")
    if res.returncode != 0 or not produced.exists():
        # Older LibreOffice versions reject the filter options; retry with defaults.
        cmd[cmd.index(TAGGED)] = "pdf"
        res = subprocess.run(cmd, capture_output=True, text=True, timeout=180)
        if res.returncode != 0 or not produced.exists():
            raise RuntimeError(f"PDF conversion failed: {res.stderr or res.stdout}")
    if produced != out:
        produced.replace(out)
    return out
