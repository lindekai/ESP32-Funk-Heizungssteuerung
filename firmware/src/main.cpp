// Phase 1: Sniffer für den Vaillant VRT 240f
//
// Der CC1101 läuft im asynchronen OOK-Modus und gibt das demodulierte Signal
// an GDO0 aus. Ein Interrupt misst jede Pegeldauer; zusammenhängende Pulse
// werden zu Rahmen gruppiert, roh ausgegeben und testweise mit dem
// 340f-Schema (BMC + HDLC) dekodiert.

#include <Arduino.h>
#include <ELECHOUSE_CC1101_SRC_DRV.h>
#include <U8g2lib.h>
#include <Wire.h>
#include <soc/gpio_reg.h>

#include "config.h"
#include "vaillant_decoder.h"

using vaillant::Pulse;

// ---------------------------------------------------------------------------
// Pulserfassung (ISR -> Ringpuffer)

namespace {

constexpr size_t kRingSize = 4096;  // Zweierpotenz
Pulse ring[kRingSize];
volatile size_t ringHead = 0;
size_t ringTail = 0;
volatile uint32_t ringOverflows = 0;
volatile uint32_t lastEdgeUs = 0;

void IRAM_ATTR onGdo0Edge() {
  const uint32_t now = micros();
  const uint32_t duration = now - lastEdgeUs;
  lastEdgeUs = now;
  // Nach der Flanke liegt der neue Pegel an; gemessen wurde der vorherige.
  const uint8_t endedLevel =
      ((REG_READ(GPIO_IN_REG) >> PIN_CC1101_GDO0) & 1) ? 0 : 1;

  const size_t next = (ringHead + 1) & (kRingSize - 1);
  if (next == ringTail) {
    ++ringOverflows;
    return;
  }
  ring[ringHead] = {duration, endedLevel};
  ringHead = next;
}

bool popPulse(Pulse& p) {
  if (ringTail == ringHead) return false;
  p = ring[ringTail];
  ringTail = (ringTail + 1) & (kRingSize - 1);
  return true;
}

// ---------------------------------------------------------------------------
// Laufzeit-Einstellungen (per Serial änderbar)

struct Settings {
  float freqMhz = DEFAULT_FREQ_MHZ;
  float rxBwKhz = DEFAULT_RX_BW_KHZ;
  uint32_t unitUs = 0;  // 0 = automatisch schätzen
  bool printRaw = true;
} settings;

// ---------------------------------------------------------------------------
// Rahmenbildung

Pulse frame[MAX_FRAME_PULSES];
size_t frameLen = 0;
int frameRssi = 0;

struct LastFrame {
  uint32_t number = 0;
  size_t pulses = 0;
  uint32_t unitUs = 0;
  int rssi = 0;
  uint8_t bytes[32];
  size_t numBytes = 0;
} last;

U8G2_SSD1306_128X64_NONAME_F_HW_I2C display(U8G2_R0, U8X8_PIN_NONE,
                                            PIN_I2C_SCL, PIN_I2C_SDA);

void printFrame(const vaillant::DecodeResult& r) {
  Serial.printf("\n# Rahmen %lu | %u Pulse | Grundpuls %lu us | RSSI %d dBm"
                " | Halbbit-Fehler %u\n",
                static_cast<unsigned long>(last.number),
                static_cast<unsigned>(frameLen),
                static_cast<unsigned long>(r.unitUs), frameRssi,
                static_cast<unsigned>(r.halfBitErrors));

  if (settings.printRaw) {
    Serial.print("RAW:");
    for (size_t i = 0; i < frameLen; ++i) {
      Serial.printf(" %c%lu", frame[i].level ? '+' : '-',
                    static_cast<unsigned long>(frame[i].us));
    }
    Serial.println();
  }

  if (r.numBytes == 0) {
    Serial.println("HEX: (kein HDLC-Flag 0x7E gefunden)");
    return;
  }
  Serial.printf("HEX (Phase %u):", static_cast<unsigned>(r.phase));
  for (size_t i = 0; i < last.numBytes; ++i) Serial.printf(" %02X", last.bytes[i]);
  Serial.println();
}

void finishFrame() {
  if (frameLen >= MIN_FRAME_PULSES) {
    const auto r = vaillant::decodeFrame(frame, frameLen, settings.unitUs,
                                         last.bytes, sizeof(last.bytes));
    ++last.number;
    last.pulses = frameLen;
    last.unitUs = r.unitUs;
    last.rssi = frameRssi;
    last.numBytes = r.numBytes;
    printFrame(r);
  }
  frameLen = 0;
}

void handlePulse(const Pulse& p) {
  if (p.us < MIN_PULSE_US || p.us > MAX_PULSE_US) {
    finishFrame();
    return;
  }
  if (frameLen == MIN_FRAME_PULSES / 2) {
    frameRssi = ELECHOUSE_cc1101.getRssi();  // Signal ist gerade aktiv
  }
  if (frameLen < MAX_FRAME_PULSES) frame[frameLen++] = p;
}

// ---------------------------------------------------------------------------
// Funk und Anzeige

void configureRadio() {
  ELECHOUSE_cc1101.setCCMode(0);       // asynchroner Seriell-Modus an GDO0
  ELECHOUSE_cc1101.setModulation(2);   // ASK/OOK
  ELECHOUSE_cc1101.setMHZ(settings.freqMhz);
  ELECHOUSE_cc1101.setRxBW(settings.rxBwKhz);
  ELECHOUSE_cc1101.SetRx();
}

void drawDisplay(int rssiNow) {
  display.clearBuffer();
  display.setFont(u8g2_font_6x10_tf);
  display.drawStr(0, 9, "VRT 240f Sniffer");
  display.setCursor(0, 20);
  display.printf("%.3f MHz  OOK", settings.freqMhz);

  // RSSI-Balken von -110 bis -30 dBm
  display.setCursor(0, 31);
  display.printf("RSSI %4d", rssiNow);
  const int barWidth = constrain(map(rssiNow, -110, -30, 0, 64), 0, 64);
  display.drawFrame(62, 24, 66, 8);
  display.drawBox(63, 25, barWidth, 6);

  display.setCursor(0, 42);
  if (last.number == 0) {
    display.print("warte auf Rahmen...");
  } else {
    display.printf("#%lu %uP %luus %ddB", static_cast<unsigned long>(last.number),
                   static_cast<unsigned>(last.pulses),
                   static_cast<unsigned long>(last.unitUs), last.rssi);
    if (last.numBytes == 0) {
      display.drawStr(0, 53, "kein 0x7E-Flag");
    } else {
      for (size_t line = 0; line < 2; ++line) {
        display.setCursor(0, 53 + 11 * line);
        for (size_t i = line * 7; i < last.numBytes && i < line * 7 + 7; ++i) {
          display.printf("%02X ", last.bytes[i]);
        }
      }
    }
  }
  display.sendBuffer();
}

// ---------------------------------------------------------------------------
// Serial-Befehle

void printHelp() {
  Serial.println(
      "Befehle:\n"
      "  f <MHz>    Frequenz setzen, z. B. f 868.28\n"
      "  bw <kHz>   Empfangsbandbreite (58..812), z. B. bw 200\n"
      "  u <us>     Grundpuls fest vorgeben, 0 = automatisch\n"
      "  raw on|off Rohpulse ausgeben\n"
      "  status     aktuelle Einstellungen\n"
      "  help       diese Hilfe");
}

void printStatus() {
  Serial.printf("Frequenz %.3f MHz | BW %.0f kHz | Grundpuls %s | RAW %s |"
                " Rahmen %lu | Pufferüberläufe %lu\n",
                settings.freqMhz, settings.rxBwKhz,
                settings.unitUs ? String(settings.unitUs).c_str() : "auto",
                settings.printRaw ? "an" : "aus",
                static_cast<unsigned long>(last.number),
                static_cast<unsigned long>(ringOverflows));
}

void handleCommand(String line) {
  line.trim();
  const int space = line.indexOf(' ');
  const String cmd = space < 0 ? line : line.substring(0, space);
  const String arg = space < 0 ? "" : line.substring(space + 1);

  if (cmd == "f" && arg.length()) {
    settings.freqMhz = arg.toFloat();
    configureRadio();
  } else if (cmd == "bw" && arg.length()) {
    settings.rxBwKhz = arg.toFloat();
    configureRadio();
  } else if (cmd == "u" && arg.length()) {
    settings.unitUs = arg.toInt();
  } else if (cmd == "raw") {
    settings.printRaw = arg != "off";
  } else if (cmd == "help" || cmd == "?") {
    printHelp();
    return;
  } else if (cmd != "status") {
    Serial.printf("Unbekannter Befehl: %s\n", line.c_str());
    printHelp();
    return;
  }
  printStatus();
}

void pollSerial() {
  static String buffer;
  while (Serial.available()) {
    const char c = Serial.read();
    if (c == '\n' || c == '\r') {
      if (buffer.length()) handleCommand(buffer);
      buffer = "";
    } else {
      buffer += c;
    }
  }
}

}  // namespace

// ---------------------------------------------------------------------------

void setup() {
  Serial.begin(SERIAL_BAUD);
  delay(200);
  Serial.println("\nESP32 Funk-Heizungssteuerung – Phase 1: Sniffer");

  display.begin();
  display.setFont(u8g2_font_6x10_tf);

  ELECHOUSE_cc1101.setSpiPin(PIN_CC1101_SCK, PIN_CC1101_MISO, PIN_CC1101_MOSI,
                             PIN_CC1101_CSN);
  ELECHOUSE_cc1101.setGDO0(PIN_CC1101_GDO0);
  if (!ELECHOUSE_cc1101.getCC1101()) {
    Serial.println("FEHLER: CC1101 antwortet nicht – Verdrahtung prüfen.");
    display.clearBuffer();
    display.drawStr(0, 10, "CC1101 fehlt!");
    display.drawStr(0, 24, "Verdrahtung pruefen");
    display.sendBuffer();
    while (true) delay(1000);
  }
  ELECHOUSE_cc1101.Init();
  configureRadio();

  pinMode(PIN_CC1101_GDO0, INPUT);
  lastEdgeUs = micros();
  attachInterrupt(digitalPinToInterrupt(PIN_CC1101_GDO0), onGdo0Edge, CHANGE);

  printHelp();
  printStatus();
}

void loop() {
  Pulse p;
  while (popPulse(p)) handlePulse(p);

  // Rahmenende auch erkennen, wenn nach dem Signal keine Flanke mehr kommt
  // (lastEdgeUs vor micros() lesen, sonst kann die Differenz unterlaufen)
  const uint32_t edgeUs = lastEdgeUs;
  if (frameLen && micros() - edgeUs > FRAME_GAP_US) finishFrame();

  pollSerial();

  static uint32_t lastDraw = 0;
  if (millis() - lastDraw > 200) {
    lastDraw = millis();
    drawDisplay(ELECHOUSE_cc1101.getRssi());
  }
}
