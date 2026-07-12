#!/usr/bin/env python3
"""Regenerate the Featured Projects section of README.md from projects.json.

Usage: python3 scripts/render_readme.py

Reads ../projects.json (relative to this script) and rewrites everything
between the <!-- PROJECTS:START --> and <!-- PROJECTS:END --> markers in
README.md. Nothing outside those markers is touched.
"""
import json
import pathlib

ROOT = pathlib.Path(__file__).resolve().parent.parent
README = ROOT / "README.md"
MANIFEST = ROOT / "projects.json"
GITHUB_USER = "bhavanibedreshankar"

START_MARKER = "<!-- PROJECTS:START -->"
END_MARKER = "<!-- PROJECTS:END -->"


def featured_card(p: dict) -> str:
    return f"""    <td width="50%" valign="top">
      <a href="https://github.com/{GITHUB_USER}/{p['repo']}"><b>{p['emoji']} {p['repo']}</b></a>
      <br/>
      {p['description']}
      <br/><br/>
      <i>{p['stack']}</i>
    </td>"""


def render_featured(projects: list) -> str:
    rows = []
    for i in range(0, len(projects), 2):
        pair = projects[i:i + 2]
        cells = [featured_card(p) for p in pair]
        if len(cells) == 1:
            cells.append('    <td width="50%" valign="top">&nbsp;</td>')
        rows.append("  <tr>\n" + "\n".join(cells) + "\n  </tr>")
    return "<table>\n" + "\n".join(rows) + "\n</table>"


def render_fun(projects: list) -> str:
    blocks = []
    for p in projects:
        blocks.append(
            f"""<details>
<summary><b>{p['emoji']} {p['repo']}</b> — a for-fun side project</summary>
<br/>

{p['description']} → <a href="https://github.com/{GITHUB_USER}/{p['repo']}">repo</a>

</details>"""
        )
    return "\n\n".join(blocks)


def main() -> None:
    manifest = json.loads(MANIFEST.read_text())
    readme = README.read_text()

    if START_MARKER not in readme or END_MARKER not in readme:
        raise SystemExit(
            f"README.md is missing {START_MARKER} / {END_MARKER} markers — "
            "add them around the Featured Projects section first."
        )

    before, rest = readme.split(START_MARKER, 1)
    _, after = rest.split(END_MARKER, 1)

    section = "### Featured Projects\n\n"
    section += render_featured(manifest.get("featured", []))
    fun = manifest.get("fun", [])
    if fun:
        section += "\n\n" + render_fun(fun)

    new_readme = before + START_MARKER + "\n" + section + "\n" + END_MARKER + after
    README.write_text(new_readme)
    print(f"Regenerated Featured Projects section: "
          f"{len(manifest.get('featured', []))} featured, {len(fun)} fun.")


if __name__ == "__main__":
    main()
