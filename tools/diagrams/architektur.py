#!/usr/bin/env python3
"""Erzeugt docs/assets/architektur-{light,dark}.svg (Signalfluss des Sniffers)."""

from theme import THEMES, write

W, H = 1200, 330

STAGES = [
    ("VRT 240f", "Thermostat", "868 MHz OOK", "heat"),
    ("CC1101", "async. Modus", "Daten an GDO0", "radio"),
    ("ISR", "Flanke an GDO0", "Pulsdauer in µs", "radio"),
    ("Ringpuffer", "4096 Pulse", "ISR → loop()", "muted"),
    ("Rahmen", "Pulsfilter", "300 µs … 4 ms", "muted"),
    ("Decoder", "BMC → HDLC", "vaillant_decoder", "board"),
]


def render(c):
    o = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" '
         f'role="img" aria-label="Signalfluss des Sniffers">',
         f'''<defs><marker id="arr" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto">
  <path d="M0 0 L10 5 L0 10 z" fill="{c["muted"]}"/></marker></defs>
<style>
  text {{ font-family: ui-sans-serif,-apple-system,'Segoe UI',Helvetica,Arial,sans-serif; fill:{c["text"]}; }}
  .t {{ font-size:17px; font-weight:700; }}
  .s {{ font-size:13px; fill:{c["muted"]}; }}
  .mono {{ font-size:12px; font-family: ui-monospace,Menlo,monospace; fill:{c["muted"]}; }}
  .h {{ font-size:22px; font-weight:800; }}
</style>''',
         f'<rect width="{W}" height="{H}" rx="18" fill="{c["bg"]}"/>',
         '<text x="40" y="50" class="h">Signalfluss Phase 1</text>',
         f'<text x="270" y="50" class="s">vom Tastendruck am Thermostat bis zur Hex-Zeile im Serial Monitor</text>']
    bw, gap, y = 160, 32, 90
    for i, (title, l1, l2, accent) in enumerate(STAGES):
        x = 40 + i * (bw + gap)
        o.append(f'<rect x="{x}" y="{y}" width="{bw}" height="110" rx="14" fill="{c["card"]}" stroke="{c["grid"]}" stroke-width="2"/>')
        o.append(f'<rect x="{x}" y="{y}" width="{bw}" height="6" rx="3" fill="{c[accent]}"/>')
        o.append(f'<text x="{x + 16}" y="{y + 40}" class="t">{title}</text>')
        o.append(f'<text x="{x + 16}" y="{y + 66}" class="s">{l1}</text>')
        o.append(f'<text x="{x + 16}" y="{y + 88}" class="mono">{l2}</text>')
        if i < len(STAGES) - 1:
            ax = x + bw
            o.append(f'<path d="M{ax + 4} {y + 55} H{ax + gap - 4}" stroke="{c["muted"]}" stroke-width="2.5" marker-end="url(#arr)"/>')
    # Ausgaben
    dx = 40 + 5 * (bw + gap) + bw / 2
    for i, (label, sub) in enumerate((("Serial Monitor", "RAW + HEX"), ("OLED", "RSSI + letzter Rahmen"))):
        x = 40 + (3 + i) * (bw + gap) - 40 + i * 20
        o.append(f'<path d="M{dx} {y + 110} V{y + 150} H{x + bw / 2} V{y + 166}" fill="none" stroke="{c["muted"]}" stroke-width="2.5" marker-end="url(#arr)"/>')
        o.append(f'<rect x="{x}" y="{y + 170}" width="{bw}" height="56" rx="12" fill="{c["bg2"]}" stroke="{c["grid"]}" stroke-width="2"/>')
        o.append(f'<text x="{x + bw / 2}" y="{y + 194}" text-anchor="middle" class="t" style="font-size:15px">{label}</text>')
        o.append(f'<text x="{x + bw / 2}" y="{y + 214}" text-anchor="middle" class="s">{sub}</text>')
    o.append("</svg>")
    return "\n".join(o)


if __name__ == "__main__":
    for name, c in THEMES.items():
        write(f"architektur-{name}.svg", render(c))
