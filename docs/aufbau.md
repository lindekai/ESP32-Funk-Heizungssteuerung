# Hardware-Aufbau

Schritt für Schritt vom Tütchen voller Module zum laufenden Sniffer – auf **einem** Breadboard.

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="assets/breadboard-dark.svg">
  <img alt="Breadboard-Aufbau mit ESP32, CC1101, OLED und Temperatursensor" src="assets/breadboard-light.svg">
</picture>

## Stückliste

| Anzahl | Bauteil | Hinweis |
| --- | --- | --- |
| 1 | ESP32-DevKit (WROOM-32, 38 Pins) | Pinlage in der Grafik: DevKitC V4. Klone weichen ab, **Aufdruck auf der Platine gilt** |
| 1 | CC1101-Modul **868 MHz** mit Antenne | Pinfolge am Modul unterscheidet sich je nach Hersteller, Beschriftung prüfen |
| 1 | OLED 0,96″, SSD1306, I²C | Adresse 0x3C (auf der Platine oft „0x78“ = 8-Bit-Schreibweise) |
| 1 | Temperatursensor SHT31 oder BME280 | für Phase 4, kann jetzt schon mit auf den Bus |
| 1 | Breadboard, 830 Punkte | |
| ~20 | Dupont-Kabel (Stecker–Buchse und Stecker–Stecker) | |
| 1 | USB-Netzteil + Micro-USB-Kabel (Daten!) | reine Ladekabel können nicht flashen |

## Warum alle Pins auf einer Seite?

Das 38-Pin-DevKit ist so breit, dass auf einem Breadboard nur vor **einer** Stiftleiste eine Lochreihe frei bleibt. Vor der anderen ist kein Loch mehr erreichbar. Deshalb liegen alle Signale auf der Stiftleiste mit **3V3**. SPI und I²C lassen sich beim ESP32 frei auf GPIOs legen. Die Zuordnung ist so gewählt, dass die Reihenfolge am DevKit der Pinfolge am CC1101 entspricht und die Kabel parallel laufen. Boot-Strapping-Pins (0, 2, 5, 12, 15) bleiben frei.

## Schaltplan

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="assets/schaltplan-dark.svg">
  <img alt="Schaltplan" src="assets/schaltplan-light.svg">
</picture>

| Signal | ESP32 | CC1101 | OLED | Sensor |
| --- | --- | --- | --- | --- |
| 3,3 V | 3V3 | VCC | VCC | VCC / VIN |
| Masse | GND | GND | GND | GND |
| Empfangsdaten | G13 | GDO0 | | |
| Chip-Select | G14 | CSN | | |
| SPI-Takt | G27 | SCK | | |
| SPI MOSI | G26 | MOSI (SI) | | |
| SPI MISO | G25 | MISO (SO) | | |
| optional | G35 | GDO2 | | |
| I²C-Takt | G32 | | SCL | SCL |
| I²C-Daten | G33 | | SDA | SDA |

Alle Pins stehen in [`config.h`](../firmware/vrt240f_sniffer/config.h). Wer anders verdrahtet, ändert sie nur dort.

## Aufbau

1. **ESP32 einsetzen:** quer über die Mittelrinne, die **3V3-Stiftleiste in Reihe b**, die andere in Reihe j. Davor bleibt Reihe *a* frei. Das ist die Anschlussreihe, ein Loch pro Pin.
2. **Versorgung:** Von Reihe *a* am 3V3-Pin zur +Schiene und vom GND-Pin (zwischen 13 und 12) zur −Schiene.
3. **CC1101:** Mit Stecker–Buchse-Kabeln von Reihe *a* zum Modul, Reihenfolge laut Tabelle. VCC und GND kommen von den Schienen. **VCC an 3,3 V, niemals an 5 V.** Antenne aufschrauben, ohne sie ist die Reichweite minimal.
4. **I²C-Verteiler:** G32 (SCL) und G33 (SDA) haben nur je ein freies Loch. Von dort je ein Kabel zu einer freien Spalte rechts neben dem ESP32 führen. Jede Spalte (a–e) ist dann ein kleiner Verteiler, aus dem OLED und Sensor abgreifen.
5. **OLED und Sensor:** VCC/GND von den Schienen, SCL/SDA aus den Verteilerspalten. Die meisten Breakout-Boards haben die Pull-up-Widerstände schon drauf.
6. **Sichtprüfung:** Vor dem Einstecken des USB-Kabels jede Leitung einmal mit der Tabelle abgleichen. Vor allem VCC/GND prüfen und dass nichts am 5V-Pin hängt.

## Inbetriebnahme

Sketch [`vrt240f_sniffer.ino`](../firmware/vrt240f_sniffer/vrt240f_sniffer.ino) in der Arduino IDE öffnen, Board **ESP32 Dev Module** wählen, hochladen, seriellen Monitor mit **115200 Baud** öffnen. Details im [README](../README.md#schnellstart).

| Beobachtung | Bedeutung |
| --- | --- |
| Upload: „Failed to connect“ | beim „Connecting…“ die BOOT-Taste gedrückt halten, Datenkabel statt Ladekabel nutzen |
| `FEHLER: CC1101 antwortet nicht` | SPI-Verdrahtung (G14/G27/G26/G25) oder Versorgung prüfen |
| OLED bleibt dunkel | SDA/SCL vertauscht oder falsche Adresse, mit einem I²C-Scanner prüfen |
| RSSI-Balken springt ständig voll | Bandbreite zu groß oder Störquelle in der Nähe, `bw 135` probieren |
| `Pufferüberläufe` steigen | sehr viel Rauschen an GDO0, Bandbreite verkleinern |
| Keine Rahmen beim Drehen am Thermostat | Frequenz variieren (`f 868.25` … `f 868.40`), Thermostat näher heranlegen |

## Gehäuse

Kommt mit Phase 6 nach [`enclosure/`](../enclosure/): Sensorkammer unten, thermisch vom ESP32 getrennt, Aussparungen für OLED und USB.
