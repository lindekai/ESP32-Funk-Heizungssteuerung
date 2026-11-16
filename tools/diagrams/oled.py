#!/usr/bin/env python3
"""Erzeugt docs/assets/oled-sniffer.svg: Vorschau der OLED-Anzeige (128×64, 3-fach).

Layout entspricht drawDisplay() in firmware/vrt240f_sniffer/vrt240f_sniffer.ino.
"""

from theme import write

S = 3  # Skalierung
PAD = 22


def render():
    w, h = 128 * S + 2 * PAD, 64 * S + 2 * PAD
    px = lambda v: PAD + v * S
    lines = [
        (9, "VRT 240f Sniffer"),
        (20, "868.300 MHz  OOK"),
        (31, "RSSI  -62"),
        (42, "#3 132P 826us -61dB"),
        (53, "7E B6 6F 00 04 00 00"),
        (64, "11 2D 00 BF 82 FF 00"),
    ]
    o = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" '
         f'role="img" aria-label="OLED-Anzeige des Sniffers">',
         f'<rect width="{w}" height="{h}" rx="16" fill="#1E3A5F"/>',
         f'<rect x="{PAD - 6}" y="{PAD - 6}" width="{128 * S + 12}" height="{64 * S + 12}" rx="6" fill="#05080B"/>',
         '<style>text{font-family:ui-monospace,Menlo,Consolas,monospace;fill:#8FE3FF;font-size:'
         f'{8.4 * S:.1f}px;}}</style>']
    for baseline, text in lines:
        o.append(f'<text x="{px(0)}" y="{px(baseline) - S}" textLength="{len(text) * 6 * S}" '
                 f'lengthAdjust="spacingAndGlyphs">{text}</text>')
    # RSSI-Balken wie in der Firmware
    o.append(f'<rect x="{px(62)}" y="{px(24)}" width="{66 * S}" height="{8 * S}" fill="none" stroke="#8FE3FF" stroke-width="{S}"/>')
    o.append(f'<rect x="{px(63) + S / 2}" y="{px(25) + S / 2}" width="{38 * S}" height="{6 * S - S}" fill="#8FE3FF"/>')
    o.append("</svg>")
    return "\n".join(o)


if __name__ == "__main__":
    write("oled-sniffer.svg", render())
