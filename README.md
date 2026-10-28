# Herbstwoche Mallorca – Tagesplan

Gemeinsamer Urlaubsplaner für eine Herbstwoche bei Alcúdia (26.–31. Oktober 2026), gebaut als Claude-Artifact:
https://claude.ai/artifact/AnNbhTL4P9nJf5R4sHSASN

## Was die Seite kann

- Kanban der Urlaubstage mit Drag-and-drop (Maus, Touch, Tastatur), eigene und bearbeitbare Kacheln, Spa-Kacheln à 90 min
- Motto-Kacheln, genau eins pro Tag
- Tage entfernen und wiederherstellen, Kacheln löschen
- Handy: wischbares Tages-Karussell, Tagesleiste und Mini-Wochenüberblick (hochkant 3, quer 5 Tage)
- Wettervorhersage pro Tag, alle 3 Stunden von einem Agenten aktualisiert
- Wetter-Studio „Mallorca-Wetter“: animierte Karte mit 48 h Live-Daten (Wind, Böen, Wolken, Regen, Temperatur, Wellen, Meerestemperatur) von Open-Meteo und Regenradar von RainViewer; Tagesübersicht, Sonnenbogen und Mondphase
- „Ideen für Mallorca“ mit Fotos von Wikimedia Commons, Karte mit Pins und ein Suchfeld, das einen Recherche-Agenten startet

## GitHub Pages

Die Seite läuft als GitHub Pages unter https://dingenz358.github.io/mallorca/ .

- **Ansehen:** Ohne Anmeldung sehen alle den Plan schreibgeschützt. Die Seite lädt Änderungen alle 90 Sekunden nach.
- **Bearbeiten (nur Lukas):** Unten auf der Seite auf „Bearbeiten (Token)“ tippen und ein GitHub-Token einfügen. Das Token bleibt nur in diesem Browser. Jede Änderung wird als Commit in `data/board.json` gespeichert und ist für alle nach 1–2 Minuten sichtbar.
  Token anlegen: GitHub → Settings → Developer settings → Personal access tokens → Fine-grained tokens → „Generate new token“. Repository access: „Only select repositories“ → `Dingenz358/mallorca`. Permissions → Repository permissions → Contents: „Read and write“.
- **Wetter:** Der Workflow `.github/workflows/pages.yml` holt alle 3 Stunden die Tagesvorhersage (`scripts/fetch_weather.py`) und die Live-Kartendaten (`scripts/fetch_live.py`) und veröffentlicht die Seite neu. Über „Actions → Wetter & Seite → Run workflow“ geht das auch sofort.
- **Recherche-Suchfeld:** Funktioniert nur in der Claude-Version (Artifact), weil dort der Agent gestartet wird.

## Inhalt

| Pfad | Inhalt |
| --- | --- |
| `index.html` | Die Seite (HTML, CSS, JS). Lädt beim Start die Dateien aus `data/` |
| `data/board.json` | Der Plan: Tage, Kacheln, Mottos, ausgeblendete Ideen |
| `data/weather.json`, `data/live.json` | Tagesvorhersage und 48-h-Live-Daten mit Radar, alle 3 h aktualisiert |
| `data/ideas.json` | Die Ideen für Mallorca |
| `data/islands.json` | Küstenlinie Mallorca/Menorca (geo-maps earth-lands 100 m, © OpenStreetMap-Mitwirkende, ODbL) |
| `scripts/fetch_weather.py`, `scripts/fetch_live.py` | Wetterabruf bei Open-Meteo und RainViewer |
| `scripts/commons.py`, `scripts/fetch_photos.py` | Suche und Download der Ideen-Fotos von Wikimedia Commons |
| `photos/` | Ideen-Fotos (Urheber und Lizenz je Foto in `photos/meta.json`) und das Titelbild `hero.jpg` |
| `agents/` | Auftragstexte der beiden Claude-Agenten (Wetter für das Artifact, Recherche aus dem Suchfeld) |

## Quellen

Wetterdaten: Open-Meteo (CC BY 4.0), Radar: RainViewer. Fotos: Wikimedia Commons, Lizenzen siehe `photos/meta.json`.
