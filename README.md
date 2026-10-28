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

## Inhalt

| Pfad | Inhalt |
| --- | --- |
| `index.html` | Die komplette Seite (HTML, CSS, JS) inklusive der Datenblöcke `weather`, `ideas-data`, `live-data` und `board-state` |
| `scripts/fetch_live.py` | Holt das Wetter-Raster, Seegang und Radarbilder und schreibt das JSON für den Block `live-data` |
| `scripts/commons.py`, `scripts/fetch_photos.py` | Suche und Download der Ideen-Fotos von Wikimedia Commons |
| `data/islands.json` | Küstenlinie Mallorca/Menorca (geo-maps earth-lands 100 m, © OpenStreetMap-Mitwirkende, ODbL) |
| `photos/` | Ideen-Fotos (Urheber und Lizenz je Foto in `photos/meta.json`) und das Titelbild `hero.jpg` |
| `agents/` | Auftragstexte der beiden geplanten Agenten (Wetter alle 3 h, Recherche aus dem Suchfeld) |

## Hinweise

- Die Seite ist für claude.ai gebaut: Speichern für alle (`artifact.publish`), die Bilder (`/_blob/…`) und das Recherche-Suchfeld (Connector „Claude Code Remote“) funktionieren nur dort. Lokal geöffnet speichert sie Änderungen nur im Browser.
- `index.html` ist ein Stand vom 28.10.2026. Der aktuelle Plan, das Wetter und die Ideen liegen im Artifact.
- Wetterdaten: Open-Meteo (CC BY 4.0), RainViewer. Fotos: Wikimedia Commons, Lizenzen siehe `photos/meta.json`.
