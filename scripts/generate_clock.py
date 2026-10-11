#!/usr/bin/env python3
"""Generate an analog clock SVG with hands set to the current time in IST.

GitHub strips <script> from README SVGs, so the time is baked into hand
transforms. CSS animation keeps the hands moving after the image loads.
"""

from __future__ import annotations

import sys
from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo

TIMEZONE = ZoneInfo("Asia/Kolkata")


def hand_angles(now: datetime) -> tuple[float, float, float]:
    hour12 = now.hour % 12
    minute = now.minute
    second = now.second + now.microsecond / 1_000_000
    hour_deg = hour12 * 30 + minute / 2 + second / 120
    minute_deg = minute * 6 + second / 10
    second_deg = second * 6
    return hour_deg, minute_deg, second_deg


def render_svg(now: datetime) -> str:
    hour_deg, minute_deg, second_deg = hand_angles(now)
    stamp = now.strftime("%Y-%m-%d %H:%M:%S %Z")
    digital = now.strftime("%H:%M")
    return f'''<?xml version="1.0" encoding="utf-8"?>
<svg viewBox="-1136 -1136 2272 2272" width="600" height="600"
  xmlns="http://www.w3.org/2000/svg"
  xmlns:xlink="http://www.w3.org/1999/xlink">
  <title>Clock · {stamp}</title>
  <desc>Current time in Asia/Kolkata (IST): {digital}</desc>
  <style type="text/css">
  #face-outline {{
    fill: #fff;
    stroke: #d3d3d3;
    stroke-width: 64;
  }}
  #face-use,
  #hand-h-use,
  #hand-m-use {{
    fill: #000;
    stroke: none;
  }}
  #hand-s-use {{
    fill: #bd2420;
    stroke: none;
  }}
  #center-dot {{
    fill: #fff;
    stroke: none;
  }}
  #digital-time {{
    fill: #333;
    font-family: ui-monospace, SFMono-Regular, Menlo, Consolas, monospace;
    font-size: 150px;
    font-weight: 600;
  }}
  #digital-zone {{
    fill: #888;
    font-family: ui-monospace, SFMono-Regular, Menlo, Consolas, monospace;
    font-size: 72px;
  }}
  @keyframes rotation {{
    from {{ transform: rotate(0deg); }}
    to {{ transform: rotate(360deg); }}
  }}
  #hand-h-use {{
    transform-origin: 0 0;
    animation: rotation 43200s linear infinite;
  }}
  #hand-m-use {{
    transform-origin: 0 0;
    animation: rotation 3600s linear infinite;
  }}
  #hand-s-use {{
    transform-origin: 0 0;
    animation: rotation 60s linear infinite;
  }}
  </style>
  <defs>
    <path id="mark-5min" d="M -40,-1000 l 80,0 0,245 -80,0 z" />
    <path id="mark-min" d="M -15,-1000 l 30,0 0,80  -30,0 z" />
    <path id="hand-h" d="M -50,-650 l 100,0 10,890 -120,0 z" transform="rotate({hour_deg:.4f})" />
    <path id="hand-m" d="M -40,-950 l 80,0 10,1200 -100,0 z" transform="rotate({minute_deg:.4f})" />
    <g id="hand-s" transform="rotate({second_deg:.4f})">
      <path d="M -20,-550 l 30,0 7,890 -30,0 z" />
      <path d="M 0,-750 a 105,105 0 0 1 0,210 a 105,105 0 0 1 0,-210 z" />
    </g>
    <g id="face-30d">
      <use xlink:href="#mark-5min" />
      <use xlink:href="#mark-min" transform="rotate(06)" />
      <use xlink:href="#mark-min" transform="rotate(12)" />
      <use xlink:href="#mark-min" transform="rotate(18)" />
      <use xlink:href="#mark-min" transform="rotate(24)" />
    </g>
    <g id="face-90d">
      <use xlink:href="#face-30d" />
      <use xlink:href="#face-30d" transform="rotate(30)" />
      <use xlink:href="#face-30d" transform="rotate(60)" />
    </g>
    <g id="face">
      <use xlink:href="#face-90d" />
      <use xlink:href="#face-90d" transform="rotate(90)" />
      <use xlink:href="#face-90d" transform="rotate(180)" />
      <use xlink:href="#face-90d" transform="rotate(270)" />
    </g>
  </defs>
  <circle id="face-outline" r="1104" />
  <use xlink:href="#face" id="face-use" />
  <text id="digital-time" x="0" y="430" text-anchor="middle">{digital}</text>
  <text id="digital-zone" x="0" y="530" text-anchor="middle">IST</text>
  <use xlink:href="#hand-h" id="hand-h-use" />
  <use xlink:href="#hand-m" id="hand-m-use" />
  <use xlink:href="#hand-s" id="hand-s-use" />
  <circle id="center-dot" r="5" />
</svg>
'''


def main() -> None:
    destination = Path(sys.argv[1]) if len(sys.argv) > 1 else Path("assets/clock.svg")
    destination.parent.mkdir(parents=True, exist_ok=True)
    now = datetime.now(TIMEZONE)
    destination.write_text(render_svg(now), encoding="utf-8")
    print(f"Wrote {destination} for {now.strftime('%H:%M:%S %Z')}")


if __name__ == "__main__":
    main()
