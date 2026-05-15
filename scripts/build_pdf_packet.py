#!/usr/bin/env python3
"""Build simple PDF documents from markdown using headless Chrome."""

from __future__ import annotations

import html
import re
import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PDF_DIR = ROOT / "pdfs"

DOCS = [
    ROOT / "protocols" / "LAB_PACKET_INDEX_V1.md",
    ROOT / "protocols" / "OSF_PREREG_PROMPT_STRUCTURE_HALLUCINATION_V1.md",
    ROOT / "protocols" / "ASPREDICTED_SUMMARY_V1.md",
    ROOT / "protocols" / "PREREG_CHECKLIST_ANSWERS_V1.md",
    ROOT / "protocols" / "MODEL_PLAN_V1.md",
    ROOT / "protocols" / "DATA_DICTIONARY_V1.md",
    ROOT / "scoring" / "SCORING_RUBRIC_V1.md",
    ROOT / "protocols" / "RUN_PROTOCOL_V1.md",
    ROOT / "protocols" / "ANALYSIS_PLAN_V1.md",
    ROOT / "protocols" / "ETHICS_AND_RISK_NOTE_V1.md",
    ROOT / "proofs" / "PRE_RUN_AUDIT_REQUEST_V1.md",
    ROOT / "proofs" / "PRE_RUN_AUDIT_FIXES_V2.md",
]


def inline_markup(text: str) -> str:
    text = html.escape(text)
    text = re.sub(r"`([^`]+)`", r"<code>\1</code>", text)
    text = re.sub(r"\*\*([^*]+)\*\*", r"<strong>\1</strong>", text)
    return text


def md_to_html(markdown_text: str, title: str) -> str:
    body = []
    in_code = False
    in_ul = False
    for raw in markdown_text.splitlines():
        line = raw.rstrip()
        if line.startswith("```"):
            if in_ul:
                body.append("</ul>")
                in_ul = False
            if not in_code:
                body.append("<pre><code>")
                in_code = True
            else:
                body.append("</code></pre>")
                in_code = False
            continue
        if in_code:
            body.append(html.escape(line) + "\n")
            continue
        if not line:
            if in_ul:
                body.append("</ul>")
                in_ul = False
            continue
        if line.startswith("# "):
            if in_ul:
                body.append("</ul>")
                in_ul = False
            body.append(f"<h1>{inline_markup(line[2:])}</h1>")
        elif line.startswith("## "):
            if in_ul:
                body.append("</ul>")
                in_ul = False
            body.append(f"<h2>{inline_markup(line[3:])}</h2>")
        elif line.startswith("### "):
            if in_ul:
                body.append("</ul>")
                in_ul = False
            body.append(f"<h3>{inline_markup(line[4:])}</h3>")
        elif line.startswith("- "):
            if not in_ul:
                body.append("<ul>")
                in_ul = True
            body.append(f"<li>{inline_markup(line[2:])}</li>")
        else:
            if in_ul:
                body.append("</ul>")
                in_ul = False
            body.append(f"<p>{inline_markup(line)}</p>")
    if in_ul:
        body.append("</ul>")
    if in_code:
        body.append("</code></pre>")

    return f"""<!doctype html>
<html>
<head>
<meta charset="utf-8">
<title>{html.escape(title)}</title>
<style>
body {{ font-family: Arial, sans-serif; margin: 42px; line-height: 1.42; color: #111; }}
h1 {{ font-size: 24px; border-bottom: 1px solid #ddd; padding-bottom: 8px; }}
h2 {{ font-size: 18px; margin-top: 26px; }}
h3 {{ font-size: 15px; margin-top: 20px; }}
p, li {{ font-size: 12px; }}
code {{ font-family: monospace; background: #f3f3f3; padding: 1px 3px; }}
pre {{ background: #f6f6f6; padding: 12px; white-space: pre-wrap; font-size: 11px; }}
table {{ border-collapse: collapse; width: 100%; }}
td, th {{ border: 1px solid #ddd; padding: 4px; font-size: 11px; }}
</style>
</head>
<body>
{chr(10).join(body)}
</body>
</html>
"""


def build_one(path: Path) -> Path:
    PDF_DIR.mkdir(exist_ok=True)
    html_path = PDF_DIR / f"{path.stem}.html"
    pdf_path = PDF_DIR / f"{path.stem}.pdf"
    html_path.write_text(md_to_html(path.read_text(encoding="utf-8"), path.stem), encoding="utf-8")
    subprocess.run(
        [
            "google-chrome",
            "--headless",
            "--disable-gpu",
            "--no-sandbox",
            f"--print-to-pdf={pdf_path}",
            str(html_path),
        ],
        check=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
    )
    return pdf_path


def main() -> int:
    outputs = []
    for doc in DOCS:
        outputs.append(build_one(doc))
    for out in outputs:
        print(out)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
