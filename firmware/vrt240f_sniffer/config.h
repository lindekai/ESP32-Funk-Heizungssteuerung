// Pinbelegung und Startwerte – siehe docs/aufbau.md
//
// Alle Signale liegen auf EINER Stiftleiste des DevKits (die Seite mit 3V3).
// So passt das Board auf ein einzelnes Breadboard, obwohl dort auf der
// anderen Seite kein Loch mehr frei bleibt. SPI und I²C sind beim ESP32 frei
// auf GPIOs legbar; Boot-Strapping-Pins (0, 2, 5, 12, 15) bleiben unbenutzt.
#pragma once

#include <stdint.h>

// CC1101 (SPI) – Reihenfolge am DevKit entspricht dem 8-Pin-Header des
// Moduls (GDO0, CSN, SCK, MOSI, MISO, GDO2), so laufen die Kabel parallel.
constexpr uint8_t PIN_CC1101_GDO0 = 13;  // asynchrone Empfangsdaten
constexpr uint8_t PIN_CC1101_CSN = 14;
constexpr uint8_t PIN_CC1101_SCK = 27;
constexpr uint8_t PIN_CC1101_MOSI = 26;
constexpr uint8_t PIN_CC1101_MISO = 25;
constexpr uint8_t PIN_CC1101_GDO2 = 35;  // optional, derzeit ungenutzt (nur Eingang)

// I²C für OLED und Temperatursensor
constexpr uint8_t PIN_I2C_SDA = 33;
constexpr uint8_t PIN_I2C_SCL = 32;

// Funk-Startwerte: 13,568 MHz × 64 ≈ 868,35 MHz; der 340f wurde bei
// ~868,28 MHz beobachtet. Per Serial-Befehl "f" änderbar.
constexpr float DEFAULT_FREQ_MHZ = 868.30f;
constexpr float DEFAULT_RX_BW_KHZ = 270.0f;

// Pulsfilter: der 340f nutzt ~825 µs / ~1650 µs. Kürzere Pulse gelten als
// Rauschen, längere als Pause – beides beendet einen Rahmen.
constexpr uint32_t MIN_PULSE_US = 300;
constexpr uint32_t MAX_PULSE_US = 4000;
constexpr uint32_t FRAME_GAP_US = 8000;   // Stille nach dem letzten Puls
constexpr uint16_t MIN_FRAME_PULSES = 40;  // kürzere Folgen verwerfen
constexpr uint16_t MAX_FRAME_PULSES = 1024;

constexpr uint32_t SERIAL_BAUD = 115200;
