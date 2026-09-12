# Attribution and changes

This is an independent community extension, not an official SunFounder product.
It is not affiliated with, sponsored by, or endorsed by SunFounder.
SunFounder and Pironman names identify the upstream software and compatible hardware.
No SunFounder logo is included in this repository.

## Upstream work

SunFounder and upstream contributors retain rights to their original work.
The unchanged file `tests/upstream_oled.py` comes from:
https://github.com/sunfounder/pm_auto/blob/1b8b4d05b50358eb09831066304d51ddec268d19/pm_auto/oled.py
Upstream GPL version 2 license:
https://github.com/sunfounder/pm_auto/blob/1b8b4d05b50358eb09831066304d51ddec268d19/LICENSE

The Dockerfile references, but this repository does not redistribute, the official
SunFounder ARM64 container. Its bundled components retain their respective licenses.
Upstream projects:
- https://github.com/sunfounder/pironman5/tree/1.2.6
- https://github.com/sunfounder/pm_dashboard/tree/1.2.6
- https://github.com/sunfounder/home-assistant-addon

## Community changes — 2026-09-11

Added a text-overlay subclass, HTTP routes, a version-checked launcher, Home Assistant
packaging, tests and a Node-RED example. The original OLED test fixture is unchanged.
Version 0.1.1 restores the Supervisor API access required by the upstream software.

The extension source is distributed under GPL-2.0-only; see LICENSE.
Provided without warranty, to the extent permitted by applicable law.

## Community changes — 2026-09-12

Version 0.2.0 adds selectable font sizes, original code-drawn pictograms,
frame-based icon animations, real Pillow rendering tests and examples.
The original upstream test fixture remains unchanged.
