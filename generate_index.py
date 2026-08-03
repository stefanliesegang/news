#!/usr/bin/env python3
"""
Generiert eine Übersichts-Markdown-Datei (index.md) aus täglichen News-Summaries.

Erwartete Struktur: eine Datei pro Tag, benannt nach Datum, z.B.
    news/2026-07-28.md
    news/2026-07-27.md

Das Skript scannt den News-Ordner, liest aus jeder Datei das Datum (aus dem
Dateinamen) und den Titel (erste H1-Überschrift, sonst Dateiname), gruppiert
alles nach Jahr/Monat und schreibt eine sortierte Übersicht.

Konfiguration über Umgebungsvariablen (mit Defaults):
    NEWS_DIR     Ordner mit den täglichen Summaries   (default: "news")
    OUTPUT       Zieldatei der Übersicht              (default: "index.md")
    SITE_TITLE   Überschrift der Übersicht            (default: "News-Übersicht")
"""

import os
import re
import datetime
from pathlib import Path

NEWS_DIR = Path(os.environ.get("NEWS_DIR", "news"))
OUTPUT = Path(os.environ.get("OUTPUT", "index.md"))
SITE_TITLE = os.environ.get("SITE_TITLE", "News-Übersicht")

# Datum darf IRGENDWO im Dateinamen stehen, z.B.:
#   2026-07-31_KI-News.md   ·   KI-News_2026-08-02.md   ·   2026-07-02-KI-Tagesuebersicht.md
DATE_RE = re.compile(r"(\d{4})-(\d{2})-(\d{2})")

MONTHS_DE = {
    1: "Januar", 2: "Februar", 3: "März", 4: "April", 5: "Mai", 6: "Juni",
    7: "Juli", 8: "August", 9: "September", 10: "Oktober", 11: "November", 12: "Dezember",
}


def extract_title(path: Path) -> str:
    """Erste H1-Überschrift (# ...) als Titel, sonst Dateiname ohne Endung."""
    try:
        for line in path.read_text(encoding="utf-8").splitlines():
            stripped = line.strip()
            if stripped.startswith("# "):
                return stripped[2:].strip()
    except (OSError, UnicodeDecodeError):
        pass
    return path.stem


def extract_excerpt(path: Path, max_len: int = 140) -> str:
    """Erster echter Textabsatz als kurzer Anriss (ohne Überschriften/Listen)."""
    try:
        for line in path.read_text(encoding="utf-8").splitlines():
            s = line.strip()
            if not s or s.startswith("#") or s.startswith(("-", "*", ">", "|", "`")):
                continue
            s = re.sub(r"[*_`]", "", s)  # simple Markdown-Zeichen entfernen
            return (s[:max_len] + "…") if len(s) > max_len else s
    except (OSError, UnicodeDecodeError):
        pass
    return ""


def collect_entries():
    entries = []
    if not NEWS_DIR.is_dir():
        return entries
    for path in NEWS_DIR.glob("*.md"):
        if path.name.lower() == "index.md":
            continue
        m = DATE_RE.search(path.name)
        if not m:
            continue
        try:
            date = datetime.date(int(m.group(1)), int(m.group(2)), int(m.group(3)))
        except ValueError:
            continue
        entries.append({
            "date": date,
            "title": extract_title(path),
            "excerpt": extract_excerpt(path),
            "link": f"{NEWS_DIR.as_posix()}/{path.name}",
        })
    entries.sort(key=lambda e: e["date"], reverse=True)
    return entries


def build_markdown(entries) -> str:
    now = datetime.datetime.now().strftime("%d.%m.%Y %H:%M")
    lines = []
    lines.append("---")
    lines.append(f"title: {SITE_TITLE}")
    lines.append("---")
    lines.append("")
    lines.append(f"# {SITE_TITLE}")
    lines.append("")

    if not entries:
        lines.append(f"_Noch keine Einträge im Ordner `{NEWS_DIR.as_posix()}/` gefunden._")
        lines.append("")
        lines.append(f"<sub>Automatisch generiert am {now}.</sub>")
        return "\n".join(lines) + "\n"

    newest = entries[0]["date"].strftime("%d.%m.%Y")
    lines.append(f"**{len(entries)}** Einträge · aktuellster: **{newest}**")
    lines.append("")

    # Gruppieren nach Jahr > Monat (Reihenfolge bleibt absteigend durch Sortierung)
    current_year = None
    current_month = None
    for e in entries:
        y, mo = e["date"].year, e["date"].month
        if y != current_year:
            if lines and lines[-1] != "":
                lines.append("")
            lines.append(f"## {y}")
            lines.append("")
            current_year = y
            current_month = None
        if mo != current_month:
            if lines and lines[-1] != "":
                lines.append("")
            lines.append(f"### {MONTHS_DE[mo]} {y}")
            lines.append("")
            current_month = mo
        day = e["date"].strftime("%d.%m.%Y")
        line = f"- **[{day}]({e['link']})** — {e['title']}"
        if e["excerpt"]:
            line += f"  \n  <sub>{e['excerpt']}</sub>"
        lines.append(line)
    lines.append("")
    lines.append(f"<sub>Automatisch generiert am {now} · {len(entries)} Einträge.</sub>")
    return "\n".join(lines) + "\n"


def main():
    entries = collect_entries()
    OUTPUT.write_text(build_markdown(entries), encoding="utf-8")
    print(f"index.md geschrieben: {len(entries)} Einträge aus '{NEWS_DIR}/'.")


if __name__ == "__main__":
    main()
