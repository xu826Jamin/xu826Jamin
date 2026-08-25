# Hi, I'm Jamin Xu 👋

**Computer Engineering @ McMaster (Level 3, Co-op) — I ship products, then measure whether they worked.**

Most of my week is production TypeScript: a live consumer product with a cofounder, a
client storefront, and tooling I actually use. Before that I came up through low-level
systems — C/C++, Verilog, Docker, ROS 2 — and that's still where my instincts come from.

---

## 🚀 What I'm building

Several of these are private (client work or pre-launch). Happy to walk through any of
them in detail, including the parts that didn't work.

**AI Cultural Translator** · Next.js · TypeScript · *private repo, live deployment*
An AI that translates *everyday life* for newcomers to Canada — not language. Photograph a
letter, form, or sign; get a China-first explanation of what it is, what to do next, and a
drafted reply. Built with a cofounder. ~1,400 commits since July 2026. MVP deployed on
Vercel; the photo→answer flow is complete and currently gated behind a feature flag until
the public endpoint is rate-limited. Validated with real users and documented honestly.

**DTC E-Commerce Storefront** · Next.js · TypeScript · *client work, private*
Production storefront for a direct-to-consumer apparel brand. Full build: catalog,
cart/checkout flow, responsive image pipeline, deployment.

**Decision Engine** · *private*
A reasoning tool that produces a structured, self-attacked decision record instead of a
confident answer. Scored against a 10-problem evaluation corpus with pre-committed kill
criteria — two of its three phases had a kill gate, and I fired one of them and deleted
the feature it covered. Calibration over persuasiveness.

**Sensei Pipeline** · Python · *private*
Content pipeline built around a single JSONL manifest as the source of truth, with
generated human-readable views. Ideation → script → ingest → render → publish → learn.

---

## 🛠 Tech

- **Languages:** TypeScript, Python, C, C++, Verilog, ARM Assembly
- **Web:** Next.js, React, Node, Vercel
- **Systems:** Linux/Unix, Docker, Podman, WSL2, ROS 2 Humble
- **Hardware:** FPGA (Intel/Altera MAX10), DE10-Lite, Quartus Prime
- **Tools:** Git, Bash, Makefiles

---

## 🔩 Systems & embedded work

**[RoboticsAcademy](https://github.com/xu826Jamin/RoboticsAcademy) — GSoC 2025 Contribution (JdeRobot)**
Profiled and optimized the RADI Docker image against a 47.2 GB baseline. Removed dev/CI
tooling from `Dockerfile.dependencies_humble`; CPU/GPU split analysis identified ~8 GB of
savings for non-DL users. Demo: Follow Line exercise, `docker history` analysis, Podman on WSL2.

**[Robot-Navigation](https://github.com/xu826Jamin/Robot-Navigation)**
BFS pathfinding engine in C++ with full manual memory management. Debugged pointer
corruption across hundreds of iterations — the project that taught me to verify before I ship.

**[GDB-UI](https://github.com/xu826Jamin/GDB-UI)** · **[metaflow](https://github.com/xu826Jamin/metaflow)** · **[Wavr](https://github.com/xu826Jamin/Wavr)**
Developer tooling and experiments.

---

## 📫 Let's connect

- **LinkedIn:** [jaminxu](https://www.linkedin.com/in/jaminxu)
- **Email:** [xujamin90@gmail.com](mailto:xujamin90@gmail.com)
