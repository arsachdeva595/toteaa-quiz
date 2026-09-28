#!/usr/bin/env python3
"""Inline data/*.json into quiz/template.html.

Writes:
  quiz/index.html        standalone page (open in a browser or host anywhere)
  <out-fragment>         optional: the page without the <html>/<head> wrapper
"""
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


def load(name):
    data = json.loads((ROOT / "data" / name).read_text(encoding="utf-8"))
    # keep the payload small and safe inside a <script> tag
    return json.dumps(data, ensure_ascii=False, separators=(",", ":")).replace("</", "<\\/")


def main():
    page = (ROOT / "quiz" / "template.html").read_text(encoding="utf-8")
    page = (page.replace("/*__TAXONOMY__*/", load("taxonomy.json"))
                .replace("/*__QUIZ__*/", load("quiz-v1.json"))
                .replace("/*__OUTFITS__*/", load("outfits.sample.json")))

    standalone = ('<!doctype html>\n<html lang="en">\n<head>\n<meta charset="utf-8">\n'
                  '<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">\n'
                  '</head>\n<body>\n' + page + '\n</body>\n</html>\n')
    (ROOT / "quiz" / "index.html").write_text(standalone, encoding="utf-8")
    print("wrote quiz/index.html")

    if len(sys.argv) > 1:
        Path(sys.argv[1]).write_text(page, encoding="utf-8")
        print("wrote", sys.argv[1])


if __name__ == "__main__":
    main()
