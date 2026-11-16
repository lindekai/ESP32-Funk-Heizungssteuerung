# ESP32 Funk-Heizungssteuerung (Vaillant VRT 240f)

Projektbriefing als Startpunkt für Claude Code und das GitHub-Repo.

## Ziel

Ein eigenes, smartes Funkgerät auf Basis eines ESP32, das mit dem vorhandenen Funkempfänger einer Vaillant-Heiztherme (Baujahr ca. 1994, nachgerüstet mit Funkset VRT 240f) kommuniziert. Langfristig soll es das alte Thermostat ersetzen oder ergänzen und in Apple Home steuerbar sein.

## Bestehendes System

- Raumthermostat (Sender): Vaillant VRT 240f, 2x AAA, Typenschild-Nr. 306773, CE 0536
- Funkempfänger an der Therme: 230 V, im Prinzip ein Schaltrelais (Wärmeanforderung an/aus), Status-LEDs
- Quarz im Thermostat: 13,568 MHz, daraus folgt 13,568 × 64 ≈ 868,35 MHz. Das Funkband ist also sehr wahrscheinlich 868 MHz.
- Referenz: Der Nachfolger Vaillant calorMATIC/VRT 340f (868 MHz) wurde bereits decodiert: http://wiki.kainhofer.com/hardware/vaillantvrt340f

## Hardware

- Mikrocontroller: ESP32-DevKit (ESP32-WROOM-32, 38 Pins, Stiftleisten bereits verlötet, Micro-USB)
- Display: 0,96" OLED, 128x64, SSD1306, I²C, Adresse 0x3C (auf der Platine als 0x78 beschriftet), Stiftleiste vorhanden
- Funkmodul: CC1101, 868-MHz-Variante, 2,54-mm-Raster (muss noch gekauft werden)
- Temperatursensor: I²C, z. B. SHT31 oder BME280 (noch festzulegen)
- Stromversorgung: USB-Netzteil (Dauerbetrieb). LiPo-Puffer nur als spätere Ausbaustufe.
- Aufbau: Breadboard und Dupont-Kabel für den Test, Stecker bleiben auch im Gehäuse

## Pinbelegung (Vorschlag)

| Bauteil | Bauteil-Pin | ESP32-DevKit-Pin |
| --- | --- | --- |
| CC1101 | VCC | 3V3 |
| CC1101 | GND | GND |
| CC1101 | GDO0 | G13 |
| CC1101 | CSN | G14 |
| CC1101 | SCK | G27 |
| CC1101 | MOSI (SI) | G26 |
| CC1101 | MISO (SO) | G25 |
| CC1101 | GDO2 (optional) | G35 |
| OLED 0,96" | VCC | 3V3 |
| OLED 0,96" | GND | GND |
| OLED 0,96" | SCL | G32 |
| OLED 0,96" | SDA | G33 |
| Temperatursensor | VCC | 3V3 |
| Temperatursensor | GND | GND |
| Temperatursensor | SCL | G32 |
| Temperatursensor | SDA | G33 |

Breadboard: Ein Breadboard reicht. Das DevKit ist so breit, dass nur auf einer Seite eine Lochreihe frei bleibt – deshalb liegen alle benötigten Signale auf der 3V3-Stiftleiste (SPI und I²C sind beim ESP32 frei auf GPIOs legbar). 3V3 und GND auf die Versorgungsschienen legen, alle drei Module von dort versorgen. Den CC1101 niemals an 5 V anschließen.

&#91;embedded content: Schalt- und Breadboard-Plan · ESP32, CC1101, OLED, Sensor\]

Auf dem Breadboard: ESP32 mittig über zwei Boards, 3V3 und GND auf die Schienen, CC1101 rechts daneben, OLED und Sensor teilen sich die beiden I²C-Leitungen.

## Software-Architektur

- Framework: Arduino IDE
- CC1101: SmartRC-CC1101-Driver-Lib oder RadioLib
- Display: U8g2 (128x64-SSD1306)
- Smart-Home-Anbindung ohne MQTT, eine der beiden Varianten (Entscheidung offen):
  - A: HomeSpan, der ESP32 erscheint direkt als HomeKit-Thermostat in Apple Home
  - B: HTTP-Schnittstelle am ESP32 und Homebridge-Plugin (z. B. homebridge-web-thermostat) auf dem Raspberry Pi
- Vorhandenes Setup: Homebridge auf Raspberry Pi, Apple TV als Home-Zentrale, Steuerung über Apple Home

## Phasen

1. Sniffer: CC1101 auf 868,35 MHz, Pakete des VRT 240f beim Tastendruck mitschneiden, im Serial Monitor und auf dem OLED anzeigen
2. Protokollanalyse: Modulation, Datenrate, Paketaufbau und Adresse bestimmen, mit dem 340f-Decoding vergleichen
3. Senden: Befehle "Heizung an" und "Heizung aus" replizieren und am Empfänger testen
4. Regelung: Temperatursensor, Sollwert, Hysterese
5. Smart Home: HomeSpan oder Homebridge-Anbindung
6. Gehäuse: 3D-Druck, eigene belüftete Sensorkammer unten, thermisch getrennt vom ESP32, Aussparungen für OLED und USB, Platz für Dupont-Stecker

## Einkaufsliste

- 1x CC1101-Modul 868 MHz mit Antenne, 2,54-mm-Raster
- 1x Temperatursensor I²C (SHT31 oder BME280)
- USB-Netzteil und Kabel

## Offene Punkte

- HomeSpan oder Homebridge-HTTP
- Sensortyp
- Modulation und Paketformat des VRT 240f

## GitHub-Repo

Das Repo wird öffentlich und soll sich optisch von üblichen Bastel-Repos abheben.

- Hero-Banner oben im README (SVG, hell und dunkel per `<picture>`), mit Projektname, Kurzclaim und stilisierter Zeichnung von Thermostat, ESP32 und Funkwellen
- Badges: Plattform ESP32, Arduino IDE, Lizenz, HomeKit
- Kurzer Pitch in zwei Sätzen, danach Foto oder Rendering des fertigen Geräts im Gehäuse
- Feature-Liste, Hardware-Tabelle mit Bezugsquellen, Verdrahtungsplan als SVG
- Schnellstart: Flashen, WLAN einrichten, in Apple Home koppeln
- Abschnitt zur Protokollanalyse des VRT 240f mit Dank an das 340f-Decoding
- Ordner: `firmware/`, `enclosure/` (STL und Quelldateien), `docs/` (Schaltplan, Bilder), `tools/`
- Lizenz (z. B. MIT), CONTRIBUTING, Haftungshinweis zum Eingriff in die Heizung
