#!/usr/bin/env python3
"""Erzeugt docs/assets/breadboard-{light,dark}.svg.

Aufbau auf EINEM Breadboard: Das ESP32-DevKit (38 Pins, 1" breit) steckt
mit der 3V3-Stiftleiste in Reihe b und mit der anderen in Reihe j. Vor der
3V3-Leiste bleibt Reihe a frei – darüber laufen alle Verbindungen. Pinlage
nach ESP32-DevKitC V4, um 90° gedreht (USB links, Antenne rechts).
"""

from theme import THEMES, write

P = 18  # Lochraster in px
COLS = 46
BOARD_W = COLS * P + 40

# Lokale y-Positionen innerhalb des Breadboards
RAIL_TOP = (20, 20 + P)          # +, −
ROWS_A_E = [70 + i * P for i in range(5)]
ROWS_F_J = [ROWS_A_E[-1] + 3 * P + i * P for i in range(5)]
RAIL_BOT = (ROWS_F_J[-1] + 34, ROWS_F_J[-1] + 34 + P)
BOARD_H = RAIL_BOT[1] + 20

X0 = 40
BOARD_Y = 250

ESP_COL0 = 3
# Stiftleiste J2 (oben, Reihe b) und J3 (unten, Reihe j), jeweils von links
TOP_PINS = ["5V", "CMD", "D3", "D2", "13", "GND", "12", "14", "27", "26",
            "25", "33", "32", "35", "34", "VN", "VP", "EN", "3V3"]
BOT_PINS = ["CLK", "D0", "D1", "15", "2", "0", "4", "16", "17", "5", "18",
            "19", "GND", "21", "RX", "TX", "22", "23", "GND"]
USED = {"13", "GND", "14", "27", "26", "25", "33", "32", "35", "3V3"}  # hervorgehoben

SCL_BUS, SDA_BUS = 38, 40  # freie Spalten als I²C-Verteiler

WIRE = {
    "3V3": "#E0402B", "SCK": "#E8B10C", "MISO": "#2F6FDE", "MOSI": "#18A6C4",
    "CSN": "#E07B39", "GDO0": "#9B5DE5", "GDO2": "#B9A2F0", "SDA": "#1F9D74",
    "SCL": "#86C440",
}


def col_x(c):
    return X0 + 20 + P / 2 + c * P


def hole(row_y, c):
    return col_x(c), BOARD_Y + row_y


def row(letter):
    return (ROWS_A_E + ROWS_F_J)["abcdefghij".index(letter)]


def breadboard(o, c):
    by = BOARD_Y
    o.append(f'<rect x="{X0}" y="{by}" width="{BOARD_W}" height="{BOARD_H}" rx="10" '
             f'fill="{c["bb"]}" stroke="{c["bbEdge"]}" stroke-width="2"/>')
    gy = by + ROWS_A_E[-1] + P
    o.append(f'<rect x="{X0 + 12}" y="{gy}" width="{BOARD_W - 24}" height="{P}" rx="3" fill="{c["bbGroove"]}"/>')
    for (y1, y2) in (RAIL_TOP, RAIL_BOT):
        o.append(f'<path d="M{X0 + 14} {by + y1 - 9} H{X0 + BOARD_W - 14}" stroke="#E0402B" stroke-width="2" opacity="0.7"/>')
        o.append(f'<path d="M{X0 + 14} {by + y2 + 9} H{X0 + BOARD_W - 14}" stroke="#2F6FDE" stroke-width="2" opacity="0.7"/>')
        o.append(f'<text x="{X0 + 8}" y="{by + y1 + 4}" class="r" fill="#E0402B">+</text>')
        o.append(f'<text x="{X0 + 8}" y="{by + y2 + 4}" class="r" fill="#2F6FDE">−</text>')
    holes = []
    for ry in (*RAIL_TOP, *RAIL_BOT):
        holes += [(col_x(cc), by + ry) for cc in range(COLS) if cc % 6 != 5]
    for ry in (*ROWS_A_E, *ROWS_F_J):
        holes += [(col_x(cc), by + ry) for cc in range(COLS)]
    o.append(f'<g fill="{c["bbHole"]}">' + "".join(
        f'<rect x="{x - 3.5:.1f}" y="{y - 3.5:.1f}" width="7" height="7" rx="1.5"/>' for x, y in holes) + "</g>")
    for i, ry in enumerate(ROWS_A_E + ROWS_F_J):
        o.append(f'<text x="{X0 + 10}" y="{by + ry + 4}" class="r" fill="{c["bbText"]}">{"abcdefghij"[i]}</text>')
    # freie Reihe a hervorheben
    ya = by + row("a")
    o.append(f'<rect x="{col_x(ESP_COL0) - P / 2}" y="{ya - P / 2}" width="{19 * P}" height="{P}" rx="4" '
             f'fill="none" stroke="{c["heat"]}" stroke-width="1.5" stroke-dasharray="4 3"/>')


def esp32(o, c):
    top_y = BOARD_Y + row("b")
    bot_y = BOARD_Y + row("j")
    x1 = col_x(ESP_COL0) - P * 1.9
    x2 = col_x(ESP_COL0 + 18) + P * 1.6
    o.append(f'<rect x="{x1:.1f}" y="{top_y - 8}" width="{x2 - x1:.1f}" height="{bot_y - top_y + 16}" rx="8" '
             f'fill="#1D2329" stroke="#0B0E11" stroke-width="2"/>')
    mid = (top_y + bot_y) / 2
    # USB links, Modul + Antenne rechts
    o.append(f'<rect x="{x1 - 16:.1f}" y="{mid - 16}" width="34" height="32" rx="3" fill="#A6ADB5" stroke="#6D757E"/>')
    o.append(f'<text x="{x1 + 52:.1f}" y="{mid + 4}" text-anchor="middle" class="pin" fill="#C7CED6">USB</text>')
    o.append(f'<rect x="{x2 - 168:.1f}" y="{top_y + 22}" width="150" height="{bot_y - top_y - 44}" rx="4" fill="#B7BDC4" stroke="#8A939C"/>')
    o.append(f'<text x="{x2 - 93:.1f}" y="{mid + 5}" text-anchor="middle" class="chip">ESP32-WROOM-32</text>')
    o.append(f'<rect x="{x2 - 10:.1f}" y="{top_y + 22}" width="44" height="{bot_y - top_y - 44}" rx="4" fill="#C9CED4" stroke="#8A939C"/>')
    o.append(f'<path d="M{x2 + 26:.1f} {top_y + 36} h-20 v14 h20 v14 h-20 v14 h20 v14 h-20" fill="none" stroke="#B88A1E" stroke-width="3"/>')
    for pins, y, dy in ((TOP_PINS, top_y, 18), (BOT_PINS, bot_y, -10)):
        for i, name in enumerate(pins):
            x = col_x(ESP_COL0 + i)
            used = pins is TOP_PINS and name in USED
            o.append(f'<rect x="{x - 4}" y="{y - 4}" width="8" height="8" rx="1" fill="#D9B44A"/>')
            o.append(f'<text x="{x}" y="{y + dy}" text-anchor="middle" class="pin" '
                     f'fill="{"#FFD866" if used else "#9AA4AE"}">{name}</text>')


def module(o, c, x, y, w, h, title, sub, pins, kind, pitch=30):
    """Modul mit Stiftleiste an der Unterkante; liefert Pin-Positionen."""
    o.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="8" fill="{c["pcb_" + kind]}" stroke="#0B0E11" stroke-width="1.5"/>')
    if kind == "oled":
        o.append(f'<rect x="{x + 14}" y="{y + 12}" width="{w - 28}" height="{h - 52}" rx="3" fill="#05080B"/>')
        o.append(f'<text x="{x + 24}" y="{y + 32}" class="scr">VRT 240f Sniffer</text>')
        o.append(f'<text x="{x + 24}" y="{y + 48}" class="scr">868.300 MHz</text>')
    elif kind == "cc":
        o.append(f'<rect x="{x + w / 2 - 22}" y="{y + 14}" width="44" height="40" rx="3" fill="#15191E"/>')
        o.append(f'<text x="{x + w / 2}" y="{y + 38}" text-anchor="middle" class="pin" fill="#C7CED6">CC1101</text>')
        o.append(f'<rect x="{x + w - 4}" y="{y + 18}" width="16" height="12" fill="#C9A227"/>')
        o.append(f'<rect x="{x + w + 12}" y="{y + 16}" width="70" height="16" rx="8" fill="#20252B"/>')
    else:
        o.append(f'<rect x="{x + w / 2 - 11}" y="{y + 16}" width="22" height="22" rx="2" fill="#15191E"/>')
    o.append(f'<text x="{x}" y="{y - 24}" class="mt">{title}</text>')
    o.append(f'<text x="{x}" y="{y - 8}" class="ms">{sub}</text>')
    pos = {}
    x0 = x + (w - (len(pins) - 1) * pitch) / 2
    for i, p in enumerate(pins):
        px = x0 + i * pitch
        py = y + h
        o.append(f'<text x="{px}" y="{py - 10}" text-anchor="middle" class="pin" fill="#E9EDF1">{p}</text>')
        o.append(f'<rect x="{px - 4}" y="{py - 4}" width="8" height="8" rx="1" fill="#D9B44A"/>')
        pos[p] = (px, py)
    return pos


def wire(o, a, b, color, dashed=False, lift=0, straight=False):
    """Dupont-Kabel als Kurve; lift > 0 wölbt es nach oben, straight zieht
    es schräg vom Loch weg und erst kurz vor dem Ziel senkrecht."""
    (x1, y1), (x2, y2) = a, b
    if straight:
        d = (f"M{x1:.1f} {y1:.1f} C{x1 + (x2 - x1) * 0.35:.1f} {y1 + (y2 - y1) * 0.35:.1f} "
             f"{x2:.1f} {y2 + 40:.1f} {x2:.1f} {y2:.1f}")
    else:
        dy = (y2 - y1) * 0.5
        d = (f"M{x1:.1f} {y1:.1f} C{x1:.1f} {y1 + dy - lift:.1f} "
             f"{x2:.1f} {y2 - dy - lift:.1f} {x2:.1f} {y2:.1f}")
    dash = ' stroke-dasharray="8 7"' if dashed else ""
    o.append(f'<path d="{d}" fill="none" stroke="#000" stroke-opacity="0.25" stroke-width="7" stroke-linecap="round"{dash}/>')
    o.append(f'<path d="{d}" fill="none" stroke="{color}" stroke-width="5" stroke-linecap="round"{dash}/>')
    for x, y in (a, b):
        o.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="4.5" fill="{color}" stroke="#000" stroke-opacity="0.35"/>')


def render(c):
    W, H = 1100, BOARD_Y + BOARD_H + 80
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
         f'<text x="{X0 + 230}" y="44" class="l">Ein Breadboard · alle Signale auf der 3V3-Seite · Reihe a ist die Anschlussreihe</text>']

    breadboard(o, c)
    esp32(o, c)

    cc = module(o, c, 120, 112, 270, 76, "CC1101 868 MHz", "Pinfolge laut Aufdruck prüfen!",
                ["GND", "VCC", "GDO0", "CSN", "SCK", "MOSI", "MISO", "GDO2"], "cc")
    oled = module(o, c, 560, 100, 150, 88, "OLED 0,96″", "SSD1306 · I²C 0x3C",
                  ["GND", "VCC", "SCL", "SDA"], "oled")
    sens = module(o, c, 860, 112, 150, 76, "Temperatursensor", "SHT31 / BME280",
                  ["VCC", "GND", "SCL", "SDA"], "sens")

    pin = lambda name: hole(row("a"), ESP_COL0 + TOP_PINS.index(name))
    plus = lambda col: hole(RAIL_TOP[0], col)
    minus = lambda col: hole(RAIL_TOP[1], col)
    gnd = c["wireGnd"]

    # Versorgung: 3V3 und GND aus Reihe a auf die oberen Schienen
    wire(o, pin("3V3"), plus(ESP_COL0 + 18), WIRE["3V3"])
    wire(o, pin("GND"), minus(ESP_COL0 + 5), gnd)

    # I²C-Verteiler: SDA (33) und SCL (32) flach über Reihe a auf zwei freie
    # Spalten zwischen OLED und Sensor; OLED zweigt in Reihe b nach links ab,
    # der Sensor in Reihe e nach rechts
    wire(o, pin("33"), hole(row("a"), SDA_BUS), WIRE["SDA"], lift=30)
    wire(o, pin("32"), hole(row("a"), SCL_BUS), WIRE["SCL"], lift=16)

    # CC1101: Pinfolge am DevKit = Pinfolge am Modul
    wire(o, minus(2), cc["GND"], gnd)
    wire(o, plus(4), cc["VCC"], WIRE["3V3"])
    wire(o, pin("13"), cc["GDO0"], WIRE["GDO0"])
    wire(o, pin("14"), cc["CSN"], WIRE["CSN"])
    wire(o, pin("27"), cc["SCK"], WIRE["SCK"])
    wire(o, pin("26"), cc["MOSI"], WIRE["MOSI"])
    wire(o, pin("25"), cc["MISO"], WIRE["MISO"])
    wire(o, pin("35"), cc["GDO2"], WIRE["GDO2"], dashed=True)

    wire(o, minus(28), oled["GND"], gnd)
    wire(o, plus(29), oled["VCC"], WIRE["3V3"])
    wire(o, hole(row("b"), SCL_BUS), oled["SCL"], WIRE["SCL"], straight=True)
    wire(o, hole(row("b"), SDA_BUS), oled["SDA"], WIRE["SDA"], straight=True)
    wire(o, plus(44), sens["VCC"], WIRE["3V3"])
    wire(o, minus(45), sens["GND"], gnd)
    wire(o, hole(row("e"), SCL_BUS), sens["SCL"], WIRE["SCL"], straight=True)
    wire(o, hole(row("e"), SDA_BUS), sens["SDA"], WIRE["SDA"], straight=True)

    ly = H - 34
    x = X0
    for name in ["3V3", "GND", "SDA", "SCL", "SCK", "MISO", "MOSI", "CSN", "GDO0", "GDO2"]:
        color = gnd if name == "GND" else WIRE[name]
        o.append(f'<path d="M{x} {ly} h22" stroke="{color}" stroke-width="5" stroke-linecap="round"/>')
        o.append(f'<text x="{x + 30}" y="{ly + 4}" class="l">{name}</text>')
        x += 78
    o.append(f'<text x="{W - 40}" y="{ly + 4}" text-anchor="end" class="l">Pinlage: ESP32-DevKitC (38 Pins)</text>')
    o.append("</svg>")
    return "\n".join(o)


if __name__ == "__main__":
    for name, c in THEMES.items():
        write(f"breadboard-{name}.svg", render(c))
