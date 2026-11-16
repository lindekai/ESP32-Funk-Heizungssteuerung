# Mitmachen

Danke für dein Interesse! Besonders hilfreich sind:

- **Mitschnitte** anderer Vaillant-Funkthermostate (VRT 240f, 340f, calorMATIC …) – am einfachsten über die Issue-Vorlage „Funk-Mitschnitt teilen“
- **Protokoll-Erkenntnisse** – Ergänzungen in [`docs/protokoll.md`](docs/protokoll.md)
- **Grafiken** – werden aus `tools/diagrams/` erzeugt, bitte dort ändern statt im SVG
- **Fehlerberichte** mit Hardware, Verdrahtung und Serial-Ausgabe

## Entwicklung

```bash
cd firmware
pio test -e native   # Decoder-Tests müssen grün sein
pio run              # Firmware muss bauen
```

- Code im Stil der umgebenden Dateien, Kommentare auf Deutsch
- Plattformunabhängige Logik (Dekodierung, Regelung) gehört in `firmware/lib/` und bekommt native Tests
- Ein Pull Request pro Thema, kurze Beschreibung, was und warum

## Sicherheit

Keine Beiträge, die Sicherheitsfunktionen der Therme umgehen oder dauerhaft im 868-MHz-Band senden. Siehe Haftungsausschluss im [README](README.md).
