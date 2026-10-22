# Inventory drawer

This plain browser demo has no build step or external dependencies. Serve this
directory with `python3 -m http.server 8769 --bind 127.0.0.1` and open index.html.

The drawer must drag horizontally from 0 through 280 CSS pixels, retain its small
rotation, and keep its progress meter synchronized. Every generated item must remain
available. Keyboard controls, interruption, and reduced-motion behavior must work.
Dragging becomes expensive with a large inventory. Improve the demonstrated cost
without changing these requirements or adding a framework.

`window.demo.setCount(n)` changes the inventory. `setTravel(x)` drives the same
update used by pointer and keyboard input. `run({count, frames})` drives repeated
updates on animation frames and returns frame-interval and synchronous-work samples.
The default is 90 frames; `lastRun` retains the raw arrays. These are diagnostic
workloads; real-device responsiveness needs separate evidence.
