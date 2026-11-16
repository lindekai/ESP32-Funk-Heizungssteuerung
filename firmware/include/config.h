// Pinbelegung und Startwerte – siehe docs/projektbriefing.md
#pragma once

#include <stdint.h>

// CC1101 (VSPI)
constexpr uint8_t PIN_CC1101_SCK = 18;
constexpr uint8_t PIN_CC1101_MISO = 19;
constexpr uint8_t PIN_CC1101_MOSI = 23;
constexpr uint8_t PIN_CC1101_CSN = 5;
constexpr uint8_t PIN_CC1101_GDO0 = 26;  // asynchrone Empfangsdaten
constexpr uint8_t PIN_CC1101_GDO2 = 17;  // derzeit ungenutzt

// I²C für OLED und Temperatursensor
constexpr uint8_t PIN_I2C_SDA = 21;
constexpr uint8_t PIN_I2C_SCL = 22;

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
