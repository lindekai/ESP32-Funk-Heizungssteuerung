#!/usr/bin/env python3
"""Erzeugt docs/assets/hero-{light,dark}.svg (Banner oben im README)."""

from theme import ASSETS

out = ASSETS
themes = {
 "light": dict(bg1="#FBF7F1", bg2="#F1E9DD", text="#1C2630", muted="#5B6672", card="#FFFFFF", stroke="#1C2630", board="#1F5E4B", chip="#2A2F36", heat="#E4572E", radio="#2F6FDE", grid="#E6DCCD", track="#E6DCCD", screen="#10161C"),
 "dark":  dict(bg1="#0E141B", bg2="#16202B", text="#EEF2F6", muted="#9AA7B4", card="#1C2733", stroke="#C9D3DD", board="#2E8A6E", chip="#0B0F14", heat="#FF7A50", radio="#6EA2FF", grid="#1D2935", track="#2E3D4C", screen="#05080B"),
}
for name, c in themes.items():
    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="1280" height="420" viewBox="0 0 1280 420" role="img" aria-label="ESP32 Funk-Heizungssteuerung">
  <defs>
    <linearGradient id="bg" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0" stop-color="{c['bg1']}"/><stop offset="1" stop-color="{c['bg2']}"/>
    </linearGradient>
    <pattern id="dots" width="24" height="24" patternUnits="userSpaceOnUse">
      <circle cx="2" cy="2" r="1.4" fill="{c['grid']}"/>
    </pattern>
  </defs>
  <rect width="1280" height="420" rx="24" fill="url(#bg)"/>
  <rect x="640" width="640" height="420" fill="url(#dots)" opacity="0.9"/>

  <g font-family="ui-sans-serif, -apple-system, 'Segoe UI', Helvetica, Arial, sans-serif">
    <text x="72" y="118" font-size="18" font-weight="600" letter-spacing="3" fill="{c['heat']}">VAILLANT VRT 240f · 868 MHz</text>
    <text x="72" y="182" font-size="54" font-weight="800" fill="{c['text']}">ESP32 Funk-</text>
    <text x="72" y="244" font-size="54" font-weight="800" fill="{c['text']}">Heizungssteuerung</text>
    <text x="72" y="296" font-size="22" fill="{c['muted']}">Die alte Therme spricht wieder – jetzt auch mit Apple Home.</text>
    <g font-size="15" font-weight="600">
      <rect x="72" y="326" width="96" height="30" rx="15" fill="none" stroke="{c['muted']}"/>
      <text x="120" y="346" text-anchor="middle" fill="{c['muted']}">ESP32</text>
      <rect x="180" y="326" width="96" height="30" rx="15" fill="none" stroke="{c['muted']}"/>
      <text x="228" y="346" text-anchor="middle" fill="{c['muted']}">CC1101</text>
      <rect x="288" y="326" width="104" height="30" rx="15" fill="none" stroke="{c['muted']}"/>
      <text x="340" y="346" text-anchor="middle" fill="{c['muted']}">HomeKit</text>
    </g>
  </g>

  <!-- Thermostat -->
  <g transform="translate(720 110)">
    <rect width="170" height="210" rx="26" fill="{c['card']}" stroke="{c['stroke']}" stroke-width="3"/>
    <circle cx="85" cy="92" r="52" fill="none" stroke="{c['track']}" stroke-width="10"/>
    <path d="M 48.2 128.8 A 52 52 0 1 1 132 66" fill="none" stroke="{c['heat']}" stroke-width="10" stroke-linecap="round"/>
    <text x="85" y="104" text-anchor="middle" font-family="ui-sans-serif, -apple-system, Helvetica, Arial, sans-serif" font-size="34" font-weight="700" fill="{c['text']}">21°</text>
    <rect x="35" y="168" width="100" height="10" rx="5" fill="{c['grid']}"/>
  </g>

  <!-- Funkwellen -->
  <g fill="none" stroke="{c['radio']}" stroke-width="5" stroke-linecap="round">
    <path d="M 920 180 A 40 40 0 0 1 920 250" opacity="1"/>
    <path d="M 945 160 A 66 66 0 0 1 945 270" opacity="0.7"/>
    <path d="M 970 140 A 92 92 0 0 1 970 290" opacity="0.4"/>
  </g>

  <!-- ESP32-Board -->
  <g transform="translate(1010 92)">
    <rect width="180" height="246" rx="12" fill="{c['board']}" stroke="{c['stroke']}" stroke-width="3"/>
    <g fill="{c['bg1']}" opacity="0.85">
      {''.join(f'<rect x="10" y="{40+i*18}" width="10" height="8" rx="2"/><rect x="160" y="{40+i*18}" width="10" height="8" rx="2"/>' for i in range(11))}
    </g>
    <rect x="40" y="22" width="100" height="112" rx="6" fill="{c['chip']}"/>
    <path d="M 56 36 h 68 M 56 48 h 50 M 56 60 h 68" stroke="{c['muted']}" stroke-width="3" stroke-linecap="round"/>
    <rect x="44" y="150" width="92" height="56" rx="4" fill="{c['screen']}" stroke="{c['stroke']}" stroke-width="2"/>
    <text x="90" y="186" text-anchor="middle" font-family="ui-monospace, Menlo, monospace" font-size="18" fill="{c['radio']}">7E B6 6F</text>
    <rect x="72" y="226" width="36" height="20" rx="3" fill="{c['chip']}"/>
  </g>
</svg>
'''
    open(f"{out}/hero-{name}.svg", "w").write(svg)
