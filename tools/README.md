# Werkzeuge

| Datei | Zweck |
| --- | --- |
| [`capture.py`](capture.py) | Serial-Ausgabe des Sniffers mit Zeitstempel nach `captures/` schreiben (`pip install pyserial`) |
| [`diagrams/`](diagrams/) | Generatoren für alle Grafiken in `docs/assets/` (nur Python-Standardbibliothek) |

Grafiken neu erzeugen:

```bash
for f in hero breadboard schaltplan architektur oled; do python3 tools/diagrams/$f.py; done
```
