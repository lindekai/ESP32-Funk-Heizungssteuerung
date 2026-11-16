#!/usr/bin/env python3
"""Erzeugt docs/assets/schaltplan-{light,dark}.svg (logischer Verdrahtungsplan)."""

from theme import THEMES, write

W, H = 1000, 560

SIGNAL = {"VCC": "vcc", "3V3": "vcc", "GND": "gnd", "SCL": "i2c", "SDA": "i2c",
          "SCK": "spi", "MISO": "spi", "MOSI": "spi", "CSN": "spi",
          "GDO0": "gdo", "GDO2": "gdo"}


def render(c):
    o = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" '
         f'role="img" aria-label="Schaltplan ESP32, CC1101, OLED, Temperatursensor">',
         f'''<style>
  text {{ font-family: ui-sans-serif,-apple-system,'Segoe UI',Helvetica,Arial,sans-serif; fill:{c["text"]}; }}
  .t {{ font-size:17px; font-weight:700; }}
  .p {{ font-size:13px; font-family: ui-monospace,Menlo,monospace; }}
  .m {{ font-size:12px; fill:{c["muted"]}; }}
  .box {{ fill:{c["card"]}; stroke:{c["line"]}; stroke-width:2; }}
  .w {{ fill:none; stroke-width:3; stroke-linecap:round; stroke-linejoin:round; }}
</style>''',
         f'<rect width="{W}" height="{H}" rx="18" fill="{c["bg"]}"/>']
    a = o.append

    def color(sig):
        return c[SIGNAL[sig]]

    a(f'<rect x="380" y="60" width="240" height="440" rx="14" fill="{c["board"]}" stroke="{c["line"]}" stroke-width="2"/>')
    a('<text x="500" y="92" text-anchor="middle" class="t" style="fill:#fff">ESP32-DevKit</text>')
    a('<text x="500" y="112" text-anchor="middle" class="m" style="fill:#d7efe6">WROOM-32 · 38 Pins</text>')

    # CC1101 rechts
    cc = [("VCC", "3V3"), ("GND", "GND"), ("GDO0", "G13"), ("CSN", "G14"), ("SCK", "G27"),
          ("MOSI", "G26"), ("MISO", "G25"), ("GDO2", "G35")]
    a('<rect class="box" x="760" y="110" width="190" height="350" rx="10"/>')
    a('<text x="855" y="140" text-anchor="middle" class="t">CC1101</text>'
      '<text x="855" y="158" text-anchor="middle" class="m">868 MHz · nur 3,3 V!</text>')
    for i, (mod, esp) in enumerate(cc):
        y = 190 + i * 34
        col = color(mod)
        dash = ' stroke-dasharray="6 6"' if mod == "GDO2" else ""
        a(f'<path class="w" stroke="{col}" d="M620 {y} H760"{dash}/>')
        a(f'<circle cx="620" cy="{y}" r="4" fill="{col}"/><circle cx="760" cy="{y}" r="4" fill="{col}"/>')
        a(f'<text x="608" y="{y + 4}" text-anchor="end" class="p" style="fill:#fff">{esp}</text>')
        a(f'<text x="772" y="{y + 4}" class="p">{mod}</text>')
    a('<text x="855" y="454" text-anchor="middle" class="m">GDO2 optional</text>')

    # I²C-Module links über gemeinsame Busleitungen
    esp_y = {"VCC": 230, "GND": 270, "SCL": 310, "SDA": 350}
    for lab, sig in (("3V3", "VCC"), ("GND", "GND"), ("G32", "SCL"), ("G33", "SDA")):
        a(f'<text x="392" y="{esp_y[sig] + 4}" class="p" style="fill:#fff">{lab}</text>')
    bus_x = {"VCC": 280, "GND": 300, "SCL": 320, "SDA": 340}
    spans = {k: [v, v] for k, v in esp_y.items()}
    for name, sub, top in (("OLED 0,96″", "SSD1306 · I²C 0x3C", 70),
                           ("Temperatursensor", "SHT31 / BME280 · I²C", 320)):
        a(f'<rect class="box" x="50" y="{top}" width="190" height="170" rx="10"/>')
        a(f'<text x="64" y="{top + 28}" class="t">{name}</text><text x="64" y="{top + 46}" class="m">{sub}</text>')
        for i, sig in enumerate(("VCC", "GND", "SCL", "SDA")):
            y = top + 76 + i * 24
            x, col = bus_x[sig], color(sig)
            a(f'<text x="226" y="{y + 4}" text-anchor="end" class="p">{sig}</text>')
            a(f'<path class="w" stroke="{col}" d="M240 {y} H{x}"/><circle cx="{x}" cy="{y}" r="4" fill="{col}"/>')
            spans[sig] = [min(spans[sig][0], y), max(spans[sig][1], y)]
    for sig, x in bus_x.items():
        col = color(sig)
        lo, hi = spans[sig]
        y = esp_y[sig]
        a(f'<path class="w" stroke="{col}" d="M{x} {lo} V{hi}"/>')
        a(f'<path class="w" stroke="{col}" d="M{x} {y} H380"/>'
          f'<circle cx="{x}" cy="{y}" r="4" fill="{col}"/><circle cx="380" cy="{y}" r="4" fill="{col}"/>')

    x = 50
    for key, label in (("vcc", "3,3 V"), ("gnd", "GND"), ("i2c", "I²C"), ("spi", "SPI"), ("gdo", "GDO (Daten)")):
        a(f'<path class="w" stroke="{c[key]}" d="M{x} 530 h26"/><text x="{x + 34}" y="534" class="m">{label}</text>')
        x += 130
    a('<text x="950" y="534" text-anchor="end" class="m">logischer Plan · alle Pins auf der 3V3-Stiftleiste</text>')
    a("</svg>")
    return "\n".join(o)


if __name__ == "__main__":
    for name, c in THEMES.items():
        write(f"schaltplan-{name}.svg", render(c))
