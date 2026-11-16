// Plattformunabhängiger Decoder für mitgeschnittene OOK-Pulsfolgen.
//
// Annahmen aus dem VRT-340f-Decoding (wiki.kainhofer.com):
//   - OOK, Grundpuls ~825 µs (= halbe Bitzeit), lange Pulse = 2 Grundpulse
//   - Leitungscode: Differential Manchester / Bi-Phase Mark (BMC)
//   - Rahmen: HDLC-Flag 0x7E, danach Bit-Stuffing (0 nach fünf 1en)
//
// Ob der VRT 240f genauso funkt, ist offen – daher ist jede Stufe einzeln
// aufrufbar und die Rohdaten bleiben immer verfügbar.
#pragma once

#include <stddef.h>
#include <stdint.h>

namespace vaillant {

struct Pulse {
  uint32_t us;  // Dauer des Pegels in Mikrosekunden
  uint8_t level;  // 1 = Träger an, 0 = Träger aus
};

// Schätzt die Grundpulsdauer: Mittelwert aller Pulse, die kürzer als das
// 1,5-fache des kürzesten Pulses sind. Liefert 0 bei leerer Eingabe.
uint32_t estimateUnit(const Pulse* pulses, size_t n);

// Zerlegt Pulse in Halbbit-Pegel (Puls mit k Grundpulsen -> k Einträge).
// k wird auf 1..2 begrenzt, Abweichungen werden in *errors gezählt.
size_t pulsesToHalfBits(const Pulse* pulses, size_t n, uint32_t unitUs,
                        uint8_t* halfBits, size_t maxHalfBits, size_t* errors);

// BMC-Dekodierung ab Halbbit-Offset (0 oder 1): gleiche Halbbits -> 0,
// unterschiedliche -> 1.
size_t bmcDecode(const uint8_t* halfBits, size_t n, size_t offset,
                 uint8_t* bits, size_t maxBits);

// Sucht das Flag 0x7E, entfernt Bit-Stuffing und packt MSB-first in Bytes.
// Das Flag selbst ist das erste Ausgabebyte. Liefert 0, wenn kein Flag
// gefunden wurde. Folgen fünf 1en eine weitere 1 (Endflag/0xFF), wird ab
// dort ohne Unstuffing weiterkopiert.
size_t hdlcExtract(const uint8_t* bits, size_t n, uint8_t* out,
                   size_t maxBytes);

struct DecodeResult {
  uint32_t unitUs;
  size_t halfBitErrors;
  size_t phase;      // gewählter BMC-Offset
  size_t numBytes;   // 0 = kein Rahmen erkannt
};

// Komplette Kette: Pulse -> Halbbits -> BMC (beide Phasen) -> HDLC.
// unitUs = 0 schätzt den Grundpuls automatisch.
DecodeResult decodeFrame(const Pulse* pulses, size_t n, uint32_t unitUs,
                         uint8_t* out, size_t maxBytes);

}  // namespace vaillant
