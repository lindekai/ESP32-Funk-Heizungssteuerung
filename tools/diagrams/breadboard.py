#!/usr/bin/env python3
"""Erzeugt docs/assets/breadboard-{light,dark}.svg.

Aufbau: zwei halbe Breadboards übereinander, das ESP32-DevKit liegt quer
über der Fuge (oben Pinreihe J1 in Reihe j, unten J2 in Reihe a). Pinlage
nach ESP32-DevKitC V4 (38 Pins), Antenne links, USB rechts.
"""

import pathlib

from theme import THEMES, write

P = 18  # Lochraster in px
COLS = 30
BOARD_W = COLS * P + 40

# Lokale y-Positionen innerhalb eines Breadboards
RAIL_TOP = (20, 20 + P)
ROWS_A_E = [70 + i * P for i in range(5)]
ROWS_F_J = [ROWS_A_E[-1] + 2 * P + 6 + i * P for i in range(5)]
RAIL_BOT = (ROWS_F_J[-1] + 34, ROWS_F_J[-1] + 34 + P)
BOARD_H = RAIL_BOT[1] + 20

X0 = 50
UPPER_Y = 170
# Abstand der beiden DevKit-Pinreihen: 10 Raster
LOWER_Y = UPPER_Y + ROWS_F_J[-1] + 10 * P - ROWS_A_E[0]

ESP_COL0 = 3
TOP_PINS = ["GND", "23", "22", "TX", "RX", "21", "GND", "19", "18", "5",
            "17", "16", "4", "0", "2", "15", "D1", "D0", "CLK"]
BOT_PINS = ["3V3", "EN", "VP", "VN", "34", "35", "32", "33", "25", "26",
            "27", "14", "12", "GND", "13", "D2", "D3", "CMD", "5V"]

WIRE = {
    "3V3": "#E0402B", "GND": "#2B2F36", "SCK": "#E8B10C", "MISO": "#2F6FDE",
    "MOSI": "#18A6C4", "CSN": "#E07B39", "GDO0": "#9B5DE5", "GDO2": "#B9A2F0",
    "SDA": "#1F9D74", "SCL": "#86C440",
}


def col_x(c):
    return X0 + 20 + P / 2 + c * P


def hole(board_y, row_y, c):
    return col_x(c), board_y + row_y


def breadboard(o, by, c):
    o.append(f'<rect x="{X0}" y="{by}" width="{BOARD_W}" height="{BOARD_H}" rx="10" '
             f'fill="{c["bb"]}" stroke="{c["bbEdge"]}" stroke-width="2"/>')
    # Fuge in der Mitte
    gy = by + ROWS_A_E[-1] + P + 3
    o.append(f'<rect x="{X0 + 12}" y="{gy}" width="{BOARD_W - 24}" height="{P - 6}" rx="3" fill="{c["bbGroove"]}"/>')
    # Schienen-Markierung
    for (y1, y2) in (RAIL_TOP, RAIL_BOT):
        o.append(f'<path d="M{X0 + 14} {by + y1 - 9} H{X0 + BOARD_W - 14}" stroke="#E0402B" stroke-width="2" opacity="0.7"/>')
        o.append(f'<path d="M{X0 + 14} {by + y2 + 9} H{X0 + BOARD_W - 14}" stroke="#2F6FDE" stroke-width="2" opacity="0.7"/>')
        o.append(f'<text x="{X0 + 8}" y="{by + y1 + 4}" class="r" fill="#E0402B">+</text>')
        o.append(f'<text x="{X0 + 8}" y="{by + y2 + 4}" class="r" fill="#2F6FDE">−</text>')
    holes = []
    for ry in (*RAIL_TOP, *RAIL_BOT):
        for cc in range(COLS):
            if cc % 6 != 5:  # Schienen haben Fünfergruppen
                holes.append((col_x(cc), by + ry))
    for ry in (*ROWS_A_E, *ROWS_F_J):
        for cc in range(COLS):
            holes.append((col_x(cc), by + ry))
    o.append(f'<g fill="{c["bbHole"]}">' + "".join(
        f'<rect x="{x - 3.5:.1f}" y="{y - 3.5:.1f}" width="7" height="7" rx="1.5"/>' for x, y in holes) + "</g>")
    labels = "abcde"
    for i, ry in enumerate(ROWS_A_E):
        o.append(f'<text x="{X0 + 10}" y="{by + ry + 4}" class="r" fill="{c["bbText"]}">{labels[i]}</text>')
    for i, ry in enumerate(ROWS_F_J):
        o.append(f'<text x="{X0 + 10}" y="{by + ry + 4}" class="r" fill="{c["bbText"]}">{"fghij"[i]}</text>')


def esp32(o, c):
    top_y = UPPER_Y + ROWS_F_J[-1]
    bot_y = LOWER_Y + ROWS_A_E[0]
    x1 = col_x(ESP_COL0) - P * 1.6
    x2 = col_x(ESP_COL0 + 18) + P * 1.9
    o.append(f'<rect x="{x1:.1f}" y="{top_y - 8}" width="{x2 - x1:.1f}" height="{bot_y - top_y + 16}" rx="8" '
             f'fill="#1D2329" stroke="#0B0E11" stroke-width="2"/>')
    # Antenne + Modul
    o.append(f'<rect x="{x1 - 34:.1f}" y="{top_y + 22}" width="44" height="{bot_y - top_y - 44}" rx="4" fill="#C9CED4" stroke="#8A939C"/>')
    o.append(f'<path d="M{x1 - 26:.1f} {top_y + 36} h20 v14 h-20 v14 h20 v14 h-20 v14 h20" fill="none" stroke="#B88A1E" stroke-width="3"/>')
    o.append(f'<rect x="{x1 + 18:.1f}" y="{top_y + 22}" width="150" height="{bot_y - top_y - 44}" rx="4" fill="#B7BDC4" stroke="#8A939C"/>')
    o.append(f'<text x="{x1 + 93:.1f}" y="{(top_y + bot_y) / 2 + 5}" text-anchor="middle" class="chip">ESP32-WROOM-32</text>')
    # USB
    o.append(f'<rect x="{x2 - 18:.1f}" y="{(top_y + bot_y) / 2 - 16}" width="34" height="32" rx="3" fill="#A6ADB5" stroke="#6D757E"/>')
    o.append(f'<text x="{x2 - 70:.1f}" y="{(top_y + bot_y) / 2 + 4}" text-anchor="middle" class="pin" fill="#C7CED6">USB</text>')
    # Pins + Beschriftung
    for i, name in enumerate(TOP_PINS):
        x = col_x(ESP_COL0 + i)
        o.append(f'<rect x="{x - 4}" y="{top_y - 4}" width="8" height="8" rx="1" fill="#D9B44A"/>')
        o.append(f'<text x="{x}" y="{top_y + 18}" text-anchor="middle" class="pin" fill="#E9EDF1">{name}</text>')
    for i, name in enumerate(BOT_PINS):
        x = col_x(ESP_COL0 + i)
        o.append(f'<rect x="{x - 4}" y="{bot_y - 4}" width="8" height="8" rx="1" fill="#D9B44A"/>')
        o.append(f'<text x="{x}" y="{bot_y - 10}" text-anchor="middle" class="pin" fill="#E9EDF1">{name}</text>')


def module(o, c, x, y, w, h, title, sub, pins, kind):
    o.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="8" fill="{c["pcb_" + kind]}" stroke="#0B0E11" stroke-width="1.5"/>')
    if kind == "oled":
        o.append(f'<rect x="{x + 34}" y="{y + 14}" width="{w - 48}" height="{h - 40}" rx="3" fill="#05080B"/>')
        o.append(f'<text x="{x + 42}" y="{y + 34}" class="scr">VRT 240f Sniffer</text>')
        o.append(f'<text x="{x + 42}" y="{y + 50}" class="scr">868.300 MHz</text>')
        o.append(f'<rect x="{x + 42}" y="{y + 58}" width="{(w - 66) * 0.6:.0f}" height="6" fill="#7FD8FF"/>')
    elif kind == "cc":
        o.append(f'<rect x="{x + 46}" y="{y + 40}" width="44" height="44" rx="3" fill="#15191E"/>')
        o.append(f'<text x="{x + 68}" y="{y + 66}" text-anchor="middle" class="pin" fill="#C7CED6">CC1101</text>')
        o.append(f'<rect x="{x + w - 4}" y="{y + 22}" width="16" height="12" fill="#C9A227"/>')
        o.append(f'<rect x="{x + w + 12}" y="{y + 20}" width="70" height="16" rx="8" fill="#20252B"/>')
    else:
        o.append(f'<rect x="{x + 48}" y="{y + 26}" width="22" height="22" rx="2" fill="#15191E"/>')
    o.append(f'<text x="{x + w / 2 + 14}" y="{y + h + 20}" text-anchor="middle" class="mt">{title}</text>')
    o.append(f'<text x="{x + w / 2 + 14}" y="{y + h + 36}" text-anchor="middle" class="ms">{sub}</text>')
    pos = {}
    for i, p in enumerate(pins):
        py = y + 18 + i * P
        o.append(f'<rect x="{x - 4}" y="{py - 4}" width="8" height="8" rx="1" fill="#D9B44A"/>')
        o.append(f'<text x="{x + 10}" y="{py + 4}" class="pin" fill="#E9EDF1">{p}</text>')
        pos[p] = (x - 4, py)
    return pos


def wire(o, a, b, color, dashed=False, bend=0.5, lane=None):
    (x1, y1), (x2, y2) = a, b
    if lane is None:
        dx = (x2 - x1) * bend
        c1, c2 = x1 + dx, x2 - dx
    else:  # bleibt lange auf Höhe y1 und biegt erst bei x=lane ab
        c1 = c2 = lane
    d = f"M{x1:.1f} {y1:.1f} C{c1:.1f} {y1:.1f} {c2:.1f} {y2:.1f} {x2:.1f} {y2:.1f}"
    dash = ' stroke-dasharray="8 7"' if dashed else ""
    o.append(f'<path d="{d}" fill="none" stroke="#000" stroke-opacity="0.25" stroke-width="7" stroke-linecap="round"{dash}/>')
    o.append(f'<path d="{d}" fill="none" stroke="{color}" stroke-width="5" stroke-linecap="round"{dash}/>')
    for x, y in (a, b):
        o.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="4.5" fill="{color}" stroke="#000" stroke-opacity="0.35"/>')


def jumper(o, a, b, color):
    (x1, y1), (x2, y2) = a, b
    o.append(f'<path d="M{x1:.1f} {y1:.1f} L{x2:.1f} {y2:.1f}" stroke="{color}" stroke-width="5" stroke-linecap="round"/>')
    for x, y in (a, b):
        o.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="4.5" fill="{color}" stroke="#000" stroke-opacity="0.35"/>')


def render(c):
    W, H = 1180, LOWER_Y + BOARD_H + 110
    o = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" '
         f'role="img" aria-label="Breadboard-Aufbau ESP32, CC1101, OLED, Temperatursensor">',
         f'''<style>
  text {{ font-family: ui-sans-serif,-apple-system,'Segoe UI',Helvetica,Arial,sans-serif; }}
  .r {{ font-size:11px; font-family: ui-monospace,Menlo,monospace; }}
  .pin {{ font-size:10px; font-family: ui-monospace,Menlo,monospace; font-weight:600; }}
  .chip {{ font-size:13px; font-weight:700; fill:#2A3038; }}
  .scr {{ font-size:11px; font-family: ui-monospace,Menlo,monospace; fill:#7FD8FF; }}
  .mt {{ font-size:15px; font-weight:700; fill:{c["text"]}; }}
  .ms {{ font-size:12px; fill:{c["muted"]}; }}
  .h {{ font-size:22px; font-weight:800; fill:{c["text"]}; }}
  .l {{ font-size:13px; fill:{c["muted"]}; }}
</style>''',
         f'<rect width="{W}" height="{H}" rx="18" fill="{c["bg"]}"/>',
         f'<text x="{X0}" y="44" class="h">Breadboard-Aufbau</text>',
         f'<text x="{X0 + 230}" y="44" class="l">Zwei halbe Breadboards, ESP32 quer über der Fuge · alle Module an 3,3 V</text>']

    breadboard(o, UPPER_Y, c)
    breadboard(o, LOWER_Y, c)
    esp32(o, c)

    # Module rechts: Sensor und OLED oben (I²C), CC1101 darunter
    mx = 760
    sens = module(o, c, mx, 70, 150, 84, "Temperatursensor", "SHT31 / BME280", ["VCC", "GND", "SCL", "SDA"], "sens")
    oled = module(o, c, mx, 196, 190, 96, "OLED 0,96″", "SSD1306 · I²C 0x3C", ["GND", "VCC", "SCL", "SDA"], "oled")
    cc = module(o, c, mx, 338, 150, 160, "CC1101 868 MHz", "Pinfolge laut Aufdruck!",
                ["VCC", "GND", "MOSI", "SCK", "MISO", "GDO2", "GDO0", "CSN"], "cc")

    top = lambda name, row: hole(UPPER_Y, ROWS_F_J[row], ESP_COL0 + TOP_PINS.index(name))
    bot = lambda name, row: hole(LOWER_Y, ROWS_A_E[row], ESP_COL0 + BOT_PINS.index(name))
    up_plus = lambda cc_: hole(UPPER_Y, RAIL_TOP[0], cc_)
    up_minus = lambda cc_: hole(UPPER_Y, RAIL_TOP[1], cc_)
    lo_plus = lambda cc_: hole(LOWER_Y, RAIL_BOT[0], cc_)
    lo_minus = lambda cc_: hole(LOWER_Y, RAIL_BOT[1], cc_)
    gnd = c["wireGnd"]

    # Versorgung: 3V3 -> untere +Schiene, GND -> obere −Schiene,
    # beide Schienenpaare am rechten Rand verbunden
    jumper(o, bot("3V3", 4), lo_plus(ESP_COL0), WIRE["3V3"])
    jumper(o, top("GND", 0), up_minus(ESP_COL0), gnd)
    jumper(o, lo_plus(29), up_plus(29), WIRE["3V3"])
    jumper(o, up_minus(28), lo_minus(28), gnd)

    # Alle Module von der oberen Schiene versorgt
    wire(o, up_plus(20), sens["VCC"], WIRE["3V3"])
    wire(o, up_minus(21), sens["GND"], gnd)
    wire(o, up_plus(22), oled["VCC"], WIRE["3V3"])
    wire(o, up_minus(23), oled["GND"], gnd)
    wire(o, up_plus(25), cc["VCC"], WIRE["3V3"])
    wire(o, up_minus(26), cc["GND"], gnd)

    # I²C: OLED aus Reihe f, Sensor aus Reihe g
    wire(o, top("22", 0), oled["SCL"], WIRE["SCL"])
    wire(o, top("21", 0), oled["SDA"], WIRE["SDA"])
    wire(o, top("22", 1), sens["SCL"], WIRE["SCL"])
    wire(o, top("21", 1), sens["SDA"], WIRE["SDA"])

    # CC1101 (SPI + GDO)
    wire(o, top("23", 2), cc["MOSI"], WIRE["MOSI"])
    wire(o, top("18", 3), cc["SCK"], WIRE["SCK"])
    wire(o, top("19", 1), cc["MISO"], WIRE["MISO"])
    wire(o, top("17", 2), cc["GDO2"], WIRE["GDO2"], dashed=True)
    wire(o, bot("26", 4), cc["GDO0"], WIRE["GDO0"])
    wire(o, top("5", 3), cc["CSN"], WIRE["CSN"])

    # Legende
    ly = H - 34
    x = X0
    for name in ["3V3", "GND", "SDA", "SCL", "SCK", "MISO", "MOSI", "CSN", "GDO0", "GDO2"]:
        color = c["wireGnd"] if name == "GND" else WIRE[name]
        o.append(f'<path d="M{x} {ly} h22" stroke="{color}" stroke-width="5" stroke-linecap="round"/>')
        o.append(f'<text x="{x + 30}" y="{ly + 4}" class="l">{name}</text>')
        x += 88
    o.append(f'<text x="{W - 40}" y="{ly + 4}" text-anchor="end" class="l">Pinlage: ESP32-DevKitC (38 Pins)</text>')
    o.append("</svg>")
    return "\n".join(o)


if __name__ == "__main__":
    for name, c in THEMES.items():
        write(f"breadboard-{name}.svg", render(c))
