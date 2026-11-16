# Protokollanalyse VRT 240f

Arbeitsnotizen für Phase 2. Bekanntes vom Nachfolger VRT 340f steht oben, eigene Messungen am 240f kommen darunter.

## Referenz: VRT 340f

Quelle: [wiki.kainhofer.com/hardware/vaillantvrt340f](http://wiki.kainhofer.com/hardware/vaillantvrt340f)

| Merkmal | VRT 340f |
| --- | --- |
| Frequenz | ~868,28 MHz (gqrx-Peak 868,275 … 868,288 MHz) |
| Funkchip | Infineon TDA5250D2 (ASK/FSK) |
| Modulation | ASK/OOK |
| Grundpuls | ~825 µs, lange Pulse ~1650 µs |
| Symbolrate | ~606 Bd (Bitzeit ~1,65 ms) |
| Leitungscode | Differential Manchester / Bi-Phase Mark: Wechsel in Bitmitte = 1, kein Wechsel = 0 |
| Rahmen | Präambel 1100…, HDLC-Flag `0x7E`, Bit-Stuffing (0 nach fünf 1en), Prüfsumme, Abschluss `FF 00` (ungestufft) |
| Länge | ~215 ms, 130 Symbole, jeder Rahmen wird zweimal gesendet |

Beispielrahmen (nach Unstuffing):

```
00 00 7E B6 6F 00 04 00 00 11 2D 00 BF 82 FF 00
```

Adresse, Temperaturkodierung und Ein/Aus-Feld sind dort nicht dokumentiert.

## Messungen VRT 240f

Noch keine – CC1101 steht noch aus.

Vorgehen:

1. Sniffer flashen, `tools/capture.py` starten.
2. Am Thermostat Sollwert deutlich über die Raumtemperatur drehen (→ „Heizung an“), warten, dann deutlich darunter (→ „aus“). Jeweils mehrere Rahmen sammeln.
3. Kommt nichts an: Frequenz in 25-kHz-Schritten zwischen 868,0 und 868,6 MHz variieren (`f …`), RSSI-Balken auf dem OLED beobachten.
4. Rohpulse vergleichen: Grundpuls, Anzahl Pulse, Wiederholungen. Erkennt der Decoder `0x7E`, die Hex-Rahmen für „an“ und „aus“ nebeneinanderlegen.

| Datum | Frequenz | Grundpuls | Pulse | Aktion | Hex | Bemerkung |
| --- | --- | --- | --- | --- | --- | --- |
| | | | | | | |
