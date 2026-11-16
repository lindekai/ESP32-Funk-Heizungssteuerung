<picture>
  <source media="(prefers-color-scheme: dark)" srcset="docs/assets/hero-dark.svg">
  <img alt="ESP32 Funk-Heizungssteuerung – Die alte Therme spricht wieder, jetzt auch mit Apple Home." src="docs/assets/hero-light.svg">
</picture>

<p align="center">
  <a href="https://github.com/lindekai/ESP32-Funk-Heizungssteuerung/actions/workflows/ci.yml"><img alt="CI" src="https://img.shields.io/github/actions/workflow/status/lindekai/ESP32-Funk-Heizungssteuerung/ci.yml?branch=main&style=flat-square&label=CI"></a>
  <img alt="Plattform ESP32" src="https://img.shields.io/badge/Plattform-ESP32-1F5E4B?style=flat-square&logo=espressif&logoColor=white">
  <img alt="Framework PlatformIO / Arduino" src="https://img.shields.io/badge/Framework-PlatformIO%20%2F%20Arduino-F5822A?style=flat-square&logo=platformio&logoColor=white">
  <img alt="Funk 868 MHz" src="https://img.shields.io/badge/Funk-868%20MHz%20OOK-2F6FDE?style=flat-square">
  <img alt="HomeKit geplant" src="https://img.shields.io/badge/HomeKit-geplant-000000?style=flat-square&logo=apple&logoColor=white">
  <a href="LICENSE"><img alt="Lizenz MIT" src="https://img.shields.io/badge/Lizenz-MIT-5B6672?style=flat-square"></a>
</p>

<p align="center">
  <a href="docs/aufbau.md"><b>Aufbau</b></a> ·
  <a href="docs/firmware.md"><b>Firmware</b></a> ·
  <a href="docs/protokoll.md"><b>Protokoll</b></a> ·
  <a href="#roadmap"><b>Roadmap</b></a> ·
  <a href="CONTRIBUTING.md"><b>Mitmachen</b></a>
</p>

Eine Vaillant-Therme von 1994 mit nachgerüstetem Funkthermostat VRT 240f bekommt einen smarten Gesprächspartner. Ein ESP32 mit CC1101-Funkmodul lernt das 868-MHz-Protokoll des Thermostats, misst selbst die Raumtemperatur und schaltet die Heizung. Am Ende erscheint das Gerät als Thermostat in Apple Home – ohne Cloud, ohne MQTT.

> [!NOTE]
> **Status: Phase 1 – Sniffer.** Firmware und Decoder sind fertig und getestet. Der Mitschnitt am echten VRT 240f folgt, sobald das CC1101-Modul da ist.

<!-- Foto/Rendering des fertigen Geräts folgt mit Phase 6 (Gehäuse) -->

## Features

<table>
<tr>
<td width="55%" valign="top">

- 📡 **Sniffer:** CC1101 im asynchronen OOK-Modus, Pulsmessung per Interrupt, Ausgabe roh und dekodiert
- 🧩 **Decoder:** Differential Manchester (BMC) und HDLC-Rahmen mit Bit-Stuffing nach dem Vorbild des VRT-340f-Decodings, mit Unit-Tests auf dem Rechner
- 🎛️ **Live-Tuning:** Frequenz, Bandbreite und Grundpuls per Serial-Befehl, ohne neu zu flashen
- 🖥️ **OLED-Anzeige:** Live-RSSI und letzter Rahmen auf einen Blick
- 🛠️ *geplant:* Senden „Heizung an/aus“, Regelung mit Hysterese, HomeKit, 3D-gedrucktes Gehäuse

</td>
<td width="45%" valign="top">
<img alt="OLED-Anzeige des Sniffers" src="docs/assets/oled-sniffer.svg">
</td>
</tr>
</table>

## Hardware

| Bauteil | Details | Bezug |
| --- | --- | --- |
| ESP32-DevKit | ESP32-WROOM-32, 38 Pins, Micro-USB | z. B. AZ-Delivery, Berrybase, Amazon |
| CC1101-Modul | **868-MHz-Variante** mit Antenne, 2,54-mm-Raster | z. B. Amazon, eBay, AliExpress („CC1101 868MHz“) |
| OLED 0,96″ | 128×64, SSD1306, I²C (0x3C) | z. B. AZ-Delivery, Berrybase |
| Temperatursensor | SHT31 oder BME280, I²C (noch offen) | z. B. Adafruit, Berrybase |
| Netzteil | USB, 5 V / ≥ 1 A | – |
| Aufbau | 2 Breadboards, Dupont-Kabel | – |

> [!WARNING]
> Der CC1101 verträgt nur **3,3 V**. Niemals an 5 V anschließen.

## Aufbau

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="docs/assets/breadboard-dark.svg">
  <img alt="Breadboard-Aufbau mit ESP32, CC1101, OLED und Temperatursensor" src="docs/assets/breadboard-light.svg">
</picture>

<details>
<summary><b>Schaltplan und Pin-Tabelle</b></summary>
<br>

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="docs/assets/schaltplan-dark.svg">
  <img alt="Schaltplan" src="docs/assets/schaltplan-light.svg">
</picture>

| Bauteil | Pin | ESP32 |
| --- | --- | --- |
| CC1101 | VCC / GND | 3V3 / GND |
| CC1101 | SCK / MISO / MOSI / CSN | G18 / G19 / G23 / G5 |
| CC1101 | GDO0 / GDO2 (optional) | G26 / G17 |
| OLED + Sensor | VCC / GND | 3V3 / GND |
| OLED + Sensor | SDA / SCL | G21 / G22 |

</details>

Schritt-für-Schritt-Anleitung, Stückliste und Fehlersuche: **[docs/aufbau.md](docs/aufbau.md)**

## Schnellstart

Voraussetzung: [PlatformIO](https://platformio.org/) (CLI oder VS-Code-Erweiterung).

```bash
git clone https://github.com/lindekai/ESP32-Funk-Heizungssteuerung.git
cd ESP32-Funk-Heizungssteuerung/firmware

pio run -t upload        # Sniffer flashen
pio device monitor       # Serial Monitor, 115200 Baud
pio test -e native       # Decoder-Tests auf dem Rechner
```

Dann am VRT 240f die Solltemperatur deutlich über bzw. unter die Raumtemperatur drehen, damit er sendet. Im Serial Monitor erscheint pro Funkrahmen:

```
# Rahmen 3 | 132 Pulse | Grundpuls 826 us | RSSI -61 dBm | Halbbit-Fehler 0
RAW: +1650 -825 +825 -1650 +1650 -1650 ...
HEX (Phase 0): 7E B6 6F 00 04 00 00 11 2D 00 BF 82 FF 00
```

Befehle wie `f 868.28` (Frequenz) oder `bw 200` (Bandbreite) stellen den Empfänger live um. Alle Befehle und die Funktionsweise: **[docs/firmware.md](docs/firmware.md)**. Mitschnitte schreibt [`tools/capture.py`](tools/capture.py) in eine Datei.

*WLAN-Einrichtung und Kopplung mit Apple Home folgen mit Phase 5.*

## So funktioniert's

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="docs/assets/architektur-dark.svg">
  <img alt="Signalfluss: Thermostat → CC1101 → ISR → Ringpuffer → Rahmen → Decoder → Serial/OLED" src="docs/assets/architektur-light.svg">
</picture>

## Roadmap

- [x] Projektgerüst, Schaltplan, Breadboard-Plan, CI
- [x] **Phase 1 – Sniffer:** Pulse mitschneiden, Serial + OLED
- [ ] **Phase 2 – Protokollanalyse:** Modulation, Datenrate, Rahmenaufbau, Adresse ([Notizen](docs/protokoll.md))
- [ ] **Phase 3 – Senden:** „Heizung an/aus“ replizieren und am Empfänger testen
- [ ] **Phase 4 – Regelung:** Temperatursensor, Sollwert, Hysterese
- [ ] **Phase 5 – Smart Home:** HomeSpan (direkt HomeKit) oder HTTP + Homebridge
- [ ] **Phase 6 – Gehäuse:** 3D-Druck, belüftete Sensorkammer, Aussparungen für OLED und USB

## Protokollanalyse

Das Funkprotokoll des VRT 240f ist nicht dokumentiert. Ausgangspunkt ist das Decoding des Nachfolgers **VRT 340f** auf [wiki.kainhofer.com](http://wiki.kainhofer.com/hardware/vaillantvrt340f). Dort: OOK auf ~868,3 MHz, Grundpuls ~825 µs, Differential-Manchester-Code und HDLC-Rahmen mit Bit-Stuffing. Ein großes Dankeschön dafür – ohne diese Vorarbeit wäre der Einstieg deutlich mühsamer.

Ob der 240f genauso funkt, klärt Phase 2. Der Quarz im Thermostat (13,568 MHz × 64 ≈ 868,35 MHz) spricht zumindest für dasselbe Band. Alle Erkenntnisse landen in [`docs/protokoll.md`](docs/protokoll.md). Eigene Mitschnitte gern über die [Issue-Vorlage](../../issues/new?template=mitschnitt.yml) teilen.

## Projektstruktur

```
firmware/    PlatformIO-Projekt: Sniffer, Decoder-Bibliothek, Tests
enclosure/   Gehäuse: STL und Quelldateien (Phase 6)
docs/        Aufbau, Firmware, Protokollnotizen, Projektbriefing, Grafiken
tools/       Serial-Mitschnitt, Generatoren für alle Grafiken
```

## Haftungsausschluss

> [!CAUTION]
> Dieses Projekt greift in die Steuerung einer Gasheizung ein. Nutzung auf eigene Gefahr. Arbeiten am 230-V-Funkempfänger oder an der Therme gehören in die Hände einer Fachkraft. Das Projekt steht in keiner Verbindung zur Vaillant GmbH. „Vaillant“ und „calorMATIC“ sind Marken ihrer jeweiligen Inhaber. Beim Senden im 868-MHz-SRD-Band gelten die gesetzlichen Grenzen für Sendeleistung und Duty-Cycle (in 868,0–868,6 MHz: max. 1 %).

## Mitmachen

Beiträge, Mitschnitte anderer Vaillant-Funkthermostate und Hinweise sind willkommen – siehe [CONTRIBUTING.md](CONTRIBUTING.md).

## Lizenz

[MIT](LICENSE) © lindekai
