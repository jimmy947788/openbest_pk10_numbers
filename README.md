<div align="center">

# 🎲 gpu-outcome-risk-engine

### ⚡ A Real-Time, Dual-GPU Lottery-Outcome Risk Engine

**In ~3 seconds, on 2× RTX 2080, enumerate 3.6 million draw permutations and compute the house's P&L for every single outcome.**

<br>

📖 **English** · [繁體中文](README_TW.md)

<br>

![C](https://img.shields.io/badge/C-99-00599C?style=for-the-badge&logo=c&logoColor=white)
![OpenCL](https://img.shields.io/badge/OpenCL-Dual_GPU-ED1C24?style=for-the-badge&logo=nvidia&logoColor=white)
![CUDA](https://img.shields.io/badge/NVIDIA-2×RTX2080-76B900?style=for-the-badge&logo=nvidia&logoColor=white)
![Python](https://img.shields.io/badge/Python-Flask-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Platform](https://img.shields.io/badge/Linux-5.9.16-FCC624?style=for-the-badge&logo=linux&logoColor=black)

![Version](https://img.shields.io/badge/version-2.30-blue?style=flat-square)
![GPU](https://img.shields.io/badge/GPU-parallel-green?style=flat-square)
![Latency](https://img.shields.io/badge/latency-~3s-orange?style=flat-square)
![Throughput](https://img.shields.io/badge/permutations-3.6M-red?style=flat-square)

<br>

*A hand-rolled, high-throughput GPU risk engine — no frameworks, no black boxes. Just C, OpenCL, and two graphics cards.*

<br>

![Architecture](assets/architecture.png)

</div>

---

## 🚀 The 30-Second Pitch

> Given **every wager** placed in a round, this engine enumerates **every possible draw outcome** in parallel,
> instantly computes "if this number comes up, how much does the house win or lose", and picks the best result
> against a configurable risk threshold.

```
   All wagers  ───▶  [ Dual-GPU parallel compute ]  ───▶  House P&L per draw  ───▶  Threshold filter
                       ↑ 3.85B-cell win/loss table       ↑ 3.6M candidates at once     ↑ sub-second reply
```

**This is not a toy.** It's a GPU microservice that ran in production — always-on, listening on a socket, serving upstream in real time.

---

## ✨ Features

<table>
<tr>
<td width="50%">

### ⚡ Massively Parallel
One GPU thread per candidate draw number —
**3.6M permutations computed simultaneously**.
2× RTX 2080 finishes a full sweep in **~3s**.

</td>
<td width="50%">

### 🧮 Answer-Table Precomputation
The win/loss of every wager against every
draw number is **precomputed into a
multi-billion-cell matrix**. Runtime does
only lookup + reduction — zero recomputation.

</td>
</tr>
<tr>
<td width="50%">

### 🔀 Champion-Split · Dual-GPU Divide & Conquer
Split the **3.6M permutation space** by the
**1st-place ball** — halves fed to two GPUs.
**Both compute at once, runtime halved.**

</td>
<td width="50%">

### 🎯 Four Games, One Engine
PK10 (racing), SSC (time lottery), 11-choose-5, K3 —
**one engine, one kernel**, switched by config.
Not a single line of code changes.

</td>
</tr>
<tr>
<td width="50%">

### 🌐 Always-On Microservice
A `while(true)` loop listens on TCP,
receives wagers in chunks, computes and replies.
**Upstream Flask calls, it answers instantly.**

</td>
<td width="50%">

### 🛠️ 100% Hand-Rolled
No CUDA libraries, no third-party compute frameworks.
Self-written OpenCL kernels, manual memory management,
custom socket protocol — **every line understood.**

</td>
</tr>
</table>

---

## 📊 Benchmark

> Measured on: 2× NVIDIA RTX 2080 · Ubuntu (Linux 5.9.16) · OpenCL · Game: **PK10 (racing — the heaviest workload)**

| Metric | Value |
|--------|-------|
| 🎰 Draw enumeration | **3,628,800 permutations (10!) / round** |
| 🧮 Win/loss matrix | **≈ 3.85 billion cells (3,628,800 × 1,060 uchar)** |
| ⚡ Full-sweep latency | **≈ 3 seconds** |
| 🔀 GPU parallelism | **Champion-split, 2 cards compute in parallel** |
| 🌐 Service model | **Persistent socket, sub-second reply** |

---

## 🧠 How It Works

### ① Answer Table — Precompute Every Outcome

A giant 2D matrix storing the win/loss of every wager against every draw number, computed ahead of time:

```
                    DWD1_1   TZF3_1-2-3   B1   ...   SUMB11
   1-2-3-4-5-...       W         L         W    ...    L
   2-1-3-4-5-...       L         L         L    ...    T
      ⋮
   10-9-8-7-6-...      W         W         L    ...    W
```

- **row = draw number** — every possible drawn permutation
- **column = game × bet type** — e.g. `DWD1_1` (1st place fixed = 1), `TZF3_1-2-3` (top-3 exact), `B1` (1st place big), `SUM7` (champion+runner-up sum = 7)… `createHeader()` expands every betting option of every game into one column
- **cell = the outcome of that wager under that draw number**

**Cell values: three states — Win / Tie / Loss.**

| | Player Wins | Tie | House Wins (Player Loses) |
|---|:---:|:---:|:---:|
| Design semantics (generator output) | `+1` | `0` | `-1` |
| Current storage format (compact, kernel-direct) | `W` (Win) | `T` (Tie) | `L` (Loss) |

> Most bet types are win/loss only (`+1 / -1`); **the tie (`0`) appears in the "sum = 11 rebate" bets** — `create_opencode_table_split.py`'s `SUMB11 / SUMS11 / SUMO11 / SUME11` return `0` when the champion+runner-up sum is exactly 11.
> The storage format evolved: early kernels compared raw numbers `+1 / 0 / -1` (ASCII `43 / 44 / 45`); later (commits `85a3d62` "add tie support" and `3fbcd52`) it switched to single-byte chars `W / T / L`, so the GPU compares characters directly and the giant table is compressed. Runtime is a pure lookup — **no per-round recomputation of outcomes.**

For PK10 (the heaviest game): draw numbers = all 10-ball permutations, **`3,628,800`** × **`1,060`** bet columns = a **≈ 3.85-billion-cell** uchar table. To finish that in seconds, the key is the dual-GPU split below 👇

### ①-B Champion-Split — Divide by 1st-Place Ball, Two Cards, Half the Time 🔀

> This is the single most important engineering insight in the project.

Rather than queueing 3.6M permutations onto one card, PK10 splits the permutation space **by the champion (1st-place) ball**:

```
   Full draw permutation space (10! = 3,628,800)
   ┌─────────────────────────────────┐
   │  1st-place ball  1 ── 10         │
   └─────────────────────────────────┘
            ✂️  split by champion (balls[0])
   ┌──────────────────┐   ┌──────────────────┐
   │ champion 1~5      │   │ champion 6~10     │
   │ = 1,814,400 perms │   │ = 1,814,400 perms │
   │   → GPU 0 / table1│   │   → GPU 1 / table2│
   └──────────────────┘   └──────────────────┘
          │                        │
          └──────── compute together ───────┘
                        ▼
                 merge & return
```

The split rule in `create_opencode_table_split.py` is literally `if balls[0] <= 5 → table1 else → table2` — 5 champion values × the remaining 9! permutations = exactly 1.81M each, a clean half.

**Two birds, one stone:**
1. **Time** — each GPU carries half the permutations, computing and returning at once → **runtime halved.**
2. **Space** — each half needs only half the VRAM. The same split mechanism lets even larger tables (e.g. SSC, still ~17.7GB *per half* after splitting) be **spread across cards**, running scales a single card can't hold.

The two files in `configs/*.json`'s `OPENCODE_ANSWER_TABLE_PATH` (`_table_1` / `_table_2`) and `USE_GPU_NUM=2` dispatch the two halves to two cards — **PK10's 3.6M draw numbers are exactly what motivates the split; SSC has only 100K draw numbers, so it rides along and returns even faster.**

### ② GPU Kernels — Two Cores, Full Throttle

| Kernel | Job |
|--------|-----|
| `sum_beton_total_amount` | Aggregate all wagers by bet type (stake / stake×odds) |
| `calc_numbers_risk` | **Main engine**: one thread per draw number → sweep all wagers, look up the table → `W` add payout, `L` subtract stake, `T` zero → yields the house P&L for that number |

### ③ Real-Time Filtering — Pick by Risk Threshold

```c
targetAmount = totalWagered × killRate     // risk threshold
direction = +1 → keep draws with P&L ≥ threshold
direction = -1 → keep draws with P&L ≤ threshold
none qualify   → fall back to the extreme-value result
finally pick N results at random and return
```

---

## 🗺️ System Architecture

```
 ┌──────────────┐   wager data (HTTP)  ┌────────────────────┐
 │  betting      │ ─────────────────▶ │  Flask web service  │
 │  frontend /   │                     │  tools/web_*.py     │
 │  upstream     │                     │ (format + allowlist)│
 └──────────────┘                     └─────────┬──────────┘
                          TCP socket · chunked · terminated by '!'
                          8700=11x5 · 8701=k3 · 8702=ssc
                                               │
                                               ▼
                              ┌────────────────────────────────┐
                              │   ⚡ optimize_opencode (C core) │
                              │                                  │
                              │   wagers → one-hot amount vector │
                              │   dual-GPU enumerate × table LUT │
                              │   → house P&L per draw number    │
                              │   → threshold filter → return    │
                              └────────────────┬─────────────────┘
                                               │
                                               ▼
                                  {draw number},{P&L amount} × N
```

---

## ⚙️ Tech Stack

| Layer | Technology |
|-------|------------|
| Compute core | **C99 + OpenCL** (dual NVIDIA GPU) |
| Memory strategy | Answer-table sharding · `CL_MEM_USE_HOST_PTR` · one-hot vectorization |
| Networking | Native **BSD sockets**, custom chunked protocol |
| Config | `json-c` reads per-game config |
| Upstream toolchain | **Python 3 · Flask · pandas · pyopencl** |
| Dependencies | `json-c` · `ocl-icd` · `opencl-headers` |
| Deployment | Ubuntu · Linux kernel **5.9.16** · nvidia-driver-455 |

---

## 📂 Project Structure

```
.
├── src/                     ⚙️ C main program
│   ├── main.c               ← main loop · OpenCL scheduling · filter logic
│   ├── network.c            socket recv/send
│   ├── loadData.c           load wagers / draw numbers / answer table
│   ├── argument.c           arg parsing + config loading
│   └── logger.c mystring.c utility.c hashmap.c myfile.c dateTime.c
├── header/                  📑 headers (common.h defines globals / VERSION)
├── kernels/
│   └── kernel_program.cl    🔥 two OpenCL kernels — the compute heart
├── configs/                 🎛️ per-game config (ports / paths)
│   ├── ssc_config.json      SSC  → 8702
│   ├── 11x5_config.json     11x5 → 8700
│   └── k3_config.json       K3   → 8701
├── data/                    📊 wagers / draw numbers / answer tables / test data
├── tools/                   🐍 Python upstream toolchain (Flask + table generators)
├── kernel-5.9.16/           🐧 pinned kernel .deb (nvidia-driver compatible)
├── Makefile                 🔨 builds bin/optimize_opencode
├── inti-system.sh           📦 one-shot dependency installer
└── run_{ssc,k3,11x5}.bash   🛡️ daemon launcher + GPU temperature watchdog
```

---

## 🏁 Quick Start

```bash
# 1. Install dependencies (OpenCL / json-c / Python toolchain)
sudo bash inti-system.sh

# 2. Build
make                 # produces bin/optimize_opencode
make ver=debug       # debug build (dumps detailed intermediate vectors)

# 3. Launch the engine (-k selects the game: ssc / k3 / 11x5 / pk10)
./bin/optimize_opencode -k ssc

# or use the daemon script (with GPU temperature watchdog)
bash run_ssc.bash
```

Once started it listens on the corresponding port, waits for upstream wagers, and returns results in sub-second time.

---

## 📡 Socket Protocol

```
Line 1 (params): wagerLength,expectId,direction,killRate,resultLength
Line 2+ (wagers): one wager per line
Row separator: '^'   ·   End of stream: '!' (chunked; each chunk acked "ok", final "done")
Reply: {draw number},{P&L amount}\n × N
```

| Param | Meaning |
|-------|---------|
| `expectId` | Round ID |
| `wagerLength` | Number of wagers this round |
| `direction` | +1 / -1 filter direction |
| `killRate` | Risk threshold ratio |
| `resultLength` | Number of results to return |

---

## 💡 Why It's Worth a Look

- **A GPU high-throughput system built from scratch** — nothing hidden behind a framework. Every kernel line and every allocation is out in the open — a living OpenCL case study.
- **Real engineering trade-offs** — answer-table space-for-time, dual-GPU sharding, host-ptr zero-copy, chunked socket transfer — all decisions forged in production.
- **One person × two GPUs × an idea from 5 years ago** — with no off-the-shelf solution, independently arriving at "precompute the win/loss table + GPU-parallel enumeration".

> 📌 A pure technical project, showcasing GPU parallel computing, OpenCL kernel design, and high-throughput system engineering.

---

## 📜 License

Unspecified — no LICENSE file is currently included in the project.

<div align="center">

<br>

**If this project sparked even a little excitement about GPU parallel computing, drop a ⭐!**

</div>
