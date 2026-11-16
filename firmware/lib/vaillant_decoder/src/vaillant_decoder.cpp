#include "vaillant_decoder.h"

namespace vaillant {

namespace {
constexpr size_t kMaxFrameBits = 1024;
}

uint32_t estimateUnit(const Pulse* pulses, size_t n) {
  if (n == 0) return 0;
  uint32_t shortest = UINT32_MAX;
  for (size_t i = 0; i < n; ++i) {
    if (pulses[i].us > 0 && pulses[i].us < shortest) shortest = pulses[i].us;
  }
  if (shortest == UINT32_MAX) return 0;

  const uint32_t limit = shortest + shortest / 2;
  uint64_t sum = 0;
  uint32_t count = 0;
  for (size_t i = 0; i < n; ++i) {
    if (pulses[i].us > 0 && pulses[i].us < limit) {
      sum += pulses[i].us;
      ++count;
    }
  }
  return static_cast<uint32_t>(sum / count);
}

size_t pulsesToHalfBits(const Pulse* pulses, size_t n, uint32_t unitUs,
                        uint8_t* halfBits, size_t maxHalfBits,
                        size_t* errors) {
  size_t out = 0;
  size_t errs = 0;
  if (unitUs == 0) return 0;
  for (size_t i = 0; i < n; ++i) {
    uint32_t k = (pulses[i].us + unitUs / 2) / unitUs;
    if (k < 1) {
      k = 1;
      ++errs;
    } else if (k > 2) {
      k = 2;
      ++errs;
    }
    for (uint32_t j = 0; j < k && out < maxHalfBits; ++j) {
      halfBits[out++] = pulses[i].level ? 1 : 0;
    }
  }
  if (errors) *errors = errs;
  return out;
}

size_t bmcDecode(const uint8_t* halfBits, size_t n, size_t offset,
                 uint8_t* bits, size_t maxBits) {
  size_t out = 0;
  for (size_t i = offset; i + 1 < n && out < maxBits; i += 2) {
    bits[out++] = (halfBits[i] != halfBits[i + 1]) ? 1 : 0;
  }
  return out;
}

size_t hdlcExtract(const uint8_t* bits, size_t n, uint8_t* out,
                   size_t maxBytes) {
  // Flag 01111110 suchen
  size_t start = n;
  for (size_t i = 0; i + 8 <= n; ++i) {
    if (bits[i] == 0 && bits[i + 1] && bits[i + 2] && bits[i + 3] &&
        bits[i + 4] && bits[i + 5] && bits[i + 6] && bits[i + 7] == 0) {
      start = i;
      break;
    }
  }
  if (start == n || maxBytes == 0) return 0;

  size_t numBytes = 0;
  uint8_t acc = 0;
  uint8_t accBits = 0;
  auto push = [&](uint8_t b) {
    acc = static_cast<uint8_t>((acc << 1) | b);
    if (++accBits == 8) {
      if (numBytes < maxBytes) out[numBytes++] = acc;
      acc = 0;
      accBits = 0;
    }
  };

  // Flag unverändert übernehmen
  for (size_t i = start; i < start + 8; ++i) push(bits[i]);

  uint8_t ones = 0;
  bool unstuff = true;
  for (size_t i = start + 8; i < n && numBytes < maxBytes; ++i) {
    const uint8_t b = bits[i];
    if (unstuff && ones == 5) {
      ones = 0;
      if (b == 0) continue;  // Stuff-Bit verwerfen
      unstuff = false;       // Endflag bzw. ungestuffter Schluss
    }
    push(b);
    ones = b ? static_cast<uint8_t>(ones + 1) : 0;
  }
  return numBytes;
}

DecodeResult decodeFrame(const Pulse* pulses, size_t n, uint32_t unitUs,
                         uint8_t* out, size_t maxBytes) {
  static uint8_t halfBits[kMaxFrameBits * 2];
  static uint8_t bits[kMaxFrameBits];
  static uint8_t candidate[kMaxFrameBits / 8];

  DecodeResult r{};
  r.unitUs = unitUs ? unitUs : estimateUnit(pulses, n);
  const size_t nHalf = pulsesToHalfBits(pulses, n, r.unitUs, halfBits,
                                        sizeof(halfBits), &r.halfBitErrors);

  // Die Bitgrenze ist unbekannt: beide Halbbit-Phasen probieren und den
  // längeren Rahmen behalten.
  for (size_t phase = 0; phase < 2; ++phase) {
    const size_t nBits = bmcDecode(halfBits, nHalf, phase, bits, sizeof(bits));
    const size_t nBytes =
        hdlcExtract(bits, nBits, candidate, sizeof(candidate));
    if (nBytes > r.numBytes) {
      r.numBytes = nBytes < maxBytes ? nBytes : maxBytes;
      r.phase = phase;
      for (size_t i = 0; i < r.numBytes; ++i) out[i] = candidate[i];
    }
  }
  return r;
}

}  // namespace vaillant
