# Hi, I'm Jamin Xu 👋

**Computer Engineering @ McMaster (Level 3, Co-op) — I ship products, then measure whether they worked.**

Most of my week is production TypeScript: a live consumer product built with a cofounder,
a client storefront, and tooling I actually use. I came up through low-level systems —
C/C++, Verilog, Docker, ROS 2 — and that's still where my instincts come from.

---

## 🌊 Wavr — live on the Chrome Web Store

**[Wavr](https://github.com/xu826Jamin/Wavr)** · JavaScript · Chrome Manifest V3 ·
**[Install →](https://chromewebstore.google.com/detail/Wavr/mekfjddabogijjildgiiikkibdmekhpo)**

Wave to scroll, click, and navigate Chrome with hand gestures. No mouse, no touch — just a
webcam. Gesture recognition runs entirely on-device via MediaPipe Tasks Vision, so no video
or data ever leaves your machine. Shipped and installable, not a demo.

---

## 🚀 What else I'm building

These are private — client work or pre-launch. Happy to walk through any of them in
detail, including the parts that didn't work.

**AI Cultural Translator** · Next.js · TypeScript · *private, deployed*
An AI that translates *everyday life* for newcomers to Canada — not language. Photograph a
letter, form, or sign; get a China-first explanation of what it is, what to do next, and a
drafted reply. Built with a cofounder; ~900 of my commits since July 2026. MVP deployed on
Vercel, with the photo→answer flow gated behind a feature flag until the public endpoint is
rate-limited. Validated with real users and documented honestly, including the bad results.

**DTC E-Commerce Storefront** · Next.js · TypeScript · *client work, private*
Production storefront for a direct-to-consumer apparel brand. Catalog, cart and checkout
flow, responsive image pipeline, deployment.

**Decision Engine** · *private*
A reasoning tool that produces a structured, self-attacked decision record instead of a
confident answer. Scored against a 10-problem evaluation corpus with pre-committed kill
criteria — I fired one of those gates and deleted the feature it covered. Calibration over
persuasiveness.

**Sensei Pipeline** · Python · *private*
Content pipeline built around a single JSONL manifest as the source of truth, with
generated human-readable views. Ideate → script → ingest → render → publish → learn.

---

## 🛠 Tech

- **Languages:** TypeScript, JavaScript, Python, C, C++, Verilog, ARM Assembly
- **Web:** Next.js, React, Node, Chrome Extensions (MV3), Vercel
- **Systems:** Linux/Unix, Docker, Podman, WSL2, ROS 2 Humble
- **Hardware:** FPGA (Intel/Altera MAX10), DE10-Lite, Quartus Prime
- **Tools:** Git, Bash, Makefiles

---

## 🔩 Systems & embedded

**[Robot-Navigation](https://github.com/xu826Jamin/Robot-Navigation)** · C++
BFS pathfinding engine with full manual memory management, navigating obstacle-filled
environments. Debugged pointer corruption across hundreds of iterations — the project that
taught me to verify before I ship.

**Docker image optimization — JdeRobot RoboticsAcademy**
Profiled the RADI image against a 47.2 GB baseline; removed dev/CI tooling from
`Dockerfile.dependencies_humble` and ran a CPU/GPU split analysis identifying ~8 GB of
savings for non-DL users. Worked through Follow Line, `docker history` analysis, and Podman
on WSL2.

Earlier coursework in C, C++, and Verilog is in my
[repositories](https://github.com/xu826Jamin?tab=repositories).

---

## 📫 Let's connect

- **LinkedIn:** [jaminxu](https://www.linkedin.com/in/jaminxu)
- **Email:** [xujamin90@gmail.com](mailto:xujamin90@gmail.com)
