#!/usr/bin/env python3
"""Schreibt die Serial-Ausgabe des Sniffers mit Zeitstempel in eine Datei.

Aufruf:
    pip install pyserial
    python3 tools/capture.py /dev/cu.usbserial-0001 [--note "Sollwert hoch"]

Eingaben im Terminal werden an den ESP32 weitergereicht (z. B. "f 868.28").
Mitschnitte landen in captures/ (per .gitignore ausgeschlossen).
"""

import argparse
import datetime as dt
import pathlib
import sys
import threading

import serial


def forward_stdin(port: serial.Serial) -> None:
    for line in sys.stdin:
        port.write(line.encode())


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("port", help="Serieller Port des ESP32")
    parser.add_argument("--baud", type=int, default=115200)
    parser.add_argument("--note", default="", help="Notiz für den Dateikopf")
    args = parser.parse_args()

    out_dir = pathlib.Path(__file__).resolve().parent.parent / "captures"
    out_dir.mkdir(exist_ok=True)
    path = out_dir / f"{dt.datetime.now():%Y-%m-%d_%H%M%S}.log"

    with serial.Serial(args.port, args.baud, timeout=1) as port, path.open("w") as log:
        if args.note:
            log.write(f"# Notiz: {args.note}\n")
        print(f"Schreibe nach {path} – Abbruch mit Strg+C")
        threading.Thread(target=forward_stdin, args=(port,), daemon=True).start()
        try:
            while True:
                raw = port.readline()
                if not raw:
                    continue
                line = raw.decode(errors="replace").rstrip()
                stamp = dt.datetime.now().strftime("%H:%M:%S.%f")[:-3]
                log.write(f"{stamp} {line}\n")
                log.flush()
                print(line)
        except KeyboardInterrupt:
            pass


if __name__ == "__main__":
    main()
