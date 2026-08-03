# News-Übersicht für GitHub Pages

Automatisch generierte Übersicht aller Daily News Summaries.

## Ordnerstruktur im Repo

```
dein-repo/
├── index.md                        ← wird automatisch generiert (Startseite)
├── generate_index.py               ← der Generator
├── news/
│   ├── 2026-07-28.md               ← eine Datei pro Tag
│   ├── 2026-07-27.md
│   └── ...
└── .github/
    └── workflows/
        └── build-index.yml         ← GitHub Action
```

## So funktioniert es

1. Du legst jeden Tag eine neue Summary unter `news/JJJJ-MM-TT.md` ab (z.B. `news/2026-07-28.md`).
2. Beim Push nach `main` läuft die GitHub Action, führt `generate_index.py` aus und committet die aktualisierte `index.md` automatisch zurück.
3. GitHub Pages zeigt `index.md` als Startseite mit der kompletten, nach Monaten gruppierten Übersicht.

Du musst die Übersicht **nie von Hand pflegen** – nur die täglichen Dateien hinzufügen.

## Titel & Anriss

- Als **Titel** eines Eintrags wird die erste `# Überschrift` der jeweiligen Datei genommen (sonst der Dateiname).
- Als **Anriss** wird der erste Textabsatz gekürzt angezeigt.

Empfohlener Aufbau einer Daily-Datei:

```markdown
# 28.07.2026 – Kurztitel des Tages

Ein bis zwei Sätze Zusammenfassung als Anriss.

## Thema 1
...
```

## Konfiguration

Über Umgebungsvariablen (im Workflow gesetzt, lokal optional):

| Variable     | Default          | Bedeutung                          |
|--------------|------------------|------------------------------------|
| `NEWS_DIR`   | `news`           | Ordner mit den täglichen Summaries |
| `OUTPUT`     | `index.md`       | Zieldatei der Übersicht            |
| `SITE_TITLE` | `News-Übersicht` | Überschrift der Übersicht          |

## Einmaliges Setup

1. Lege die Dateien so ab wie in der Ordnerstruktur oben (Workflow nach `.github/workflows/build-index.yml`).
2. GitHub → **Settings → Pages**: Source auf „Deploy from a branch", Branch `main`, Ordner `/ (root)`.
3. GitHub → **Settings → Actions → General → Workflow permissions**: „Read and write permissions" aktivieren (damit die Action den Commit zurückpushen darf).
4. Ersten Push machen – fertig.

## Lokal testen

```bash
python generate_index.py      # erzeugt/aktualisiert index.md aus news/
```
