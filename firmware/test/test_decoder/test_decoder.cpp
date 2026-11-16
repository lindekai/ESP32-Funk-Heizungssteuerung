#include <unity.h>

#include <vector>

#include "vaillant_decoder.h"

using vaillant::Pulse;

namespace {

// Gegenstück zum Decoder: Bytes -> Bits (mit Stuffing nach dem Flag)
// -> BMC-Halbbits -> Pulse. jitterUs wird abwechselnd addiert/abgezogen.
std::vector<Pulse> encode(const std::vector<uint8_t>& payload, uint32_t unit,
                          int32_t jitterUs, size_t preambleBits = 16) {
  std::vector<uint8_t> bits(preambleBits, 0);
  auto appendByte = [&](uint8_t b) {
    for (int i = 7; i >= 0; --i) bits.push_back((b >> i) & 1);
  };
  appendByte(0x7E);
  int ones = 0;
  for (uint8_t byte : payload) {
    for (int i = 7; i >= 0; --i) {
      const uint8_t b = (byte >> i) & 1;
      bits.push_back(b);
      ones = b ? ones + 1 : 0;
      if (ones == 5) {
        bits.push_back(0);
        ones = 0;
      }
    }
  }

  std::vector<uint8_t> half;
  uint8_t level = 1;
  for (uint8_t b : bits) {
    level ^= 1;  // BMC: Wechsel an jeder Bitgrenze
    half.push_back(level);
    if (b) level ^= 1;  // zusätzlicher Wechsel in Bitmitte bei 1
    half.push_back(level);
  }

  std::vector<Pulse> pulses;
  int sign = 1;
  for (size_t i = 0; i < half.size();) {
    size_t run = 1;
    while (i + run < half.size() && half[i + run] == half[i]) ++run;
    pulses.push_back({static_cast<uint32_t>(run * unit + sign * jitterUs),
                      half[i]});
    sign = -sign;
    i += run;
  }
  return pulses;
}

void test_estimate_unit() {
  const Pulse p[] = {{800, 1}, {1650, 0}, {850, 1}, {1600, 0}, {830, 1}};
  TEST_ASSERT_UINT32_WITHIN(5, 826, vaillant::estimateUnit(p, 5));
  TEST_ASSERT_EQUAL_UINT32(0, vaillant::estimateUnit(p, 0));
}

void test_bmc_rule_matches_340f_description() {
  // "00" und "11" -> 0, "01" und "10" -> 1
  const uint8_t half[] = {0, 0, 1, 1, 0, 1, 1, 0};
  uint8_t bits[4];
  TEST_ASSERT_EQUAL(4, vaillant::bmcDecode(half, 8, 0, bits, 4));
  const uint8_t expected[] = {0, 0, 1, 1};
  TEST_ASSERT_EQUAL_UINT8_ARRAY(expected, bits, 4);
}

void test_hdlc_unstuffs_after_five_ones() {
  // Flag, dann 11111 0 111 -> 11111111 (Stuff-Bit entfernt)
  const uint8_t bits[] = {0, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 0, 1, 1, 1};
  uint8_t out[4];
  const size_t n = vaillant::hdlcExtract(bits, sizeof(bits), out, 4);
  TEST_ASSERT_EQUAL(2, n);
  TEST_ASSERT_EQUAL_HEX8(0x7E, out[0]);
  TEST_ASSERT_EQUAL_HEX8(0xFF, out[1]);
}

void test_hdlc_without_flag_returns_zero() {
  const uint8_t bits[] = {0, 0, 0, 0, 1, 0, 1, 0, 1, 0, 1, 0};
  uint8_t out[4];
  TEST_ASSERT_EQUAL(0, vaillant::hdlcExtract(bits, sizeof(bits), out, 4));
}

void test_roundtrip_with_jitter() {
  // Nutzdaten aus dem Beispielrahmen des VRT-340f-Decodings
  const std::vector<uint8_t> payload = {0xB6, 0x6F, 0x00, 0x04, 0x00,
                                        0x00, 0x11, 0x2D, 0x00, 0xBF, 0x82};
  const auto pulses = encode(payload, 825, 120);

  uint8_t out[32];
  const auto r = vaillant::decodeFrame(pulses.data(), pulses.size(), 0, out,
                                       sizeof(out));
  TEST_ASSERT_EQUAL(0, r.halfBitErrors);
  TEST_ASSERT_GREATER_OR_EQUAL(payload.size() + 1, r.numBytes);
  TEST_ASSERT_EQUAL_HEX8(0x7E, out[0]);
  TEST_ASSERT_EQUAL_HEX8_ARRAY(payload.data(), out + 1, payload.size());
}

void test_roundtrip_with_fixed_unit_and_odd_phase() {
  const std::vector<uint8_t> payload = {0x12, 0x34, 0xFB};
  auto pulses = encode(payload, 830, 0, 15);
  // Ersten Puls kürzen, damit die Bitgrenze auf einem ungeraden Halbbit liegt
  pulses.insert(pulses.begin(), Pulse{830, static_cast<uint8_t>(
                                               pulses.front().level ^ 1)});

  uint8_t out[16];
  const auto r = vaillant::decodeFrame(pulses.data(), pulses.size(), 830, out,
                                       sizeof(out));
  TEST_ASSERT_EQUAL_UINT32(830, r.unitUs);
  TEST_ASSERT_EQUAL(1, r.phase);
  TEST_ASSERT_EQUAL_HEX8_ARRAY(payload.data(), out + 1, payload.size());
}

}  // namespace

void setUp() {}
void tearDown() {}

int main() {
  UNITY_BEGIN();
  RUN_TEST(test_estimate_unit);
  RUN_TEST(test_bmc_rule_matches_340f_description);
  RUN_TEST(test_hdlc_unstuffs_after_five_ones);
  RUN_TEST(test_hdlc_without_flag_returns_zero);
  RUN_TEST(test_roundtrip_with_jitter);
  RUN_TEST(test_roundtrip_with_fixed_unit_and_odd_phase);
  return UNITY_END();
}
