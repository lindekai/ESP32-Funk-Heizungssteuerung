"""Gemeinsame Farben für alle Grafiken in docs/assets/."""

import pathlib

ASSETS = pathlib.Path(__file__).resolve().parents[2] / "docs" / "assets"

THEMES = {
    "light": {
        "bg": "#FBF7F1", "bg2": "#F1E9DD", "card": "#FFFFFF", "text": "#1C2630",
        "muted": "#5B6672", "line": "#1C2630", "grid": "#E6DCCD", "track": "#E6DCCD",
        "heat": "#E4572E", "radio": "#2F6FDE", "board": "#1F5E4B", "chip": "#2A2F36",
        "screen": "#10161C",
        "bb": "#F4F2EC", "bbEdge": "#D6D1C4", "bbHole": "#3A3F45", "bbGroove": "#E3DFD4",
        "bbText": "#8C8577", "wireGnd": "#2B2F36",
        "pcb_oled": "#1E3A5F", "pcb_sens": "#3B2F7A", "pcb_cc": "#1F5E4B",
        "vcc": "#E4572E", "gnd": "#4A5563", "spi": "#2F6FDE", "i2c": "#1F9D74", "gdo": "#9B5DE5",
    },
    "dark": {
        "bg": "#0E141B", "bg2": "#16202B", "card": "#1C2733", "text": "#EEF2F6",
        "muted": "#9AA7B4", "line": "#C9D3DD", "grid": "#1D2935", "track": "#2E3D4C",
        "heat": "#FF7A50", "radio": "#6EA2FF", "board": "#2E8A6E", "chip": "#0B0F14",
        "screen": "#05080B",
        "bb": "#E4E1DA", "bbEdge": "#9E988B", "bbHole": "#3A3F45", "bbGroove": "#CFCABF",
        "bbText": "#7A7365", "wireGnd": "#6B7480",
        "pcb_oled": "#1E3A5F", "pcb_sens": "#3B2F7A", "pcb_cc": "#1F5E4B",
        "vcc": "#FF7A50", "gnd": "#AAB6C2", "spi": "#6EA2FF", "i2c": "#3CC79A", "gdo": "#B98CFF",
    },
}


def write(name: str, svg: str) -> None:
    ASSETS.mkdir(parents=True, exist_ok=True)
    (ASSETS / name).write_text(svg, encoding="utf-8")
    print(f"geschrieben: docs/assets/{name}")
