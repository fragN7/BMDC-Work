#!/usr/bin/env python3

import os
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

HERE = os.path.dirname(os.path.abspath(__file__))
RESULTS = os.path.join(HERE, "results")
PLOTS = os.path.join(HERE, "plots")
os.makedirs(PLOTS, exist_ok=True)

MESH_SIZES = [1200, 12000, 120000]
DISRUPT_RATES = ["0.01", "0.02", "0.05", "0.10", "0.20"]

PALETTE = {"teal": "#0d5c63", "maroon": "#8c2f39", "gold": "#b8860b",
          "slate": "#3d4a5c", "sage": "#4c7a5a", "plum": "#5e3a72"}
plt.rcParams.update({"font.size": 10.5, "axes.grid": True, "grid.alpha": 0.25,
                     "figure.dpi": 130, "axes.edgecolor": "#555555"})


def load(name):
    return np.genfromtxt(os.path.join(RESULTS, name), names=True)


def tick_to_settle(d, threshold=0.02):
    below = np.where(d["devi"] < threshold)[0]
    return int(d["tick"][below[0]]) if len(below) else None


digest = []

# ---- Chart A: settling of the reading spread (log scale) -----------------
plt.figure(figsize=(6.8, 4.2))
for n, c in zip(MESH_SIZES, [PALETTE["teal"], PALETTE["sage"], PALETTE["gold"]]):
    d = load(f"flowsense_{n}.dat")
    spread = np.clip(d["spread"], 1e-16, None)
    plt.semilogy(d["tick"], spread, "-", marker="o", ms=3, color=c, label=f"mesh size {n:,}")
plt.xlabel("Gossip round")
plt.ylabel("Reading spread (log scale)")
plt.title("Flow sensing settles onto the true mesh-wide average")
plt.legend()
plt.tight_layout()
plt.savefig(os.path.join(PLOTS, "chartA_flow_settling.png"))
plt.close()

# ---- Chart B: reading band collapsing onto the mean (mid-size mesh) ------
d = load("flowsense_12000.dat")
plt.figure(figsize=(6.8, 4.2))
plt.fill_between(d["tick"], d["lo"], d["hi"], color=PALETTE["teal"], alpha=0.18,
                 label="lowest-highest reading band")
plt.plot(d["tick"], d["mean"], color=PALETTE["maroon"], lw=2, label="mesh-wide mean (ground truth)")
plt.plot(d["tick"], d["lo"], color=PALETTE["teal"], lw=0.8)
plt.plot(d["tick"], d["hi"], color=PALETTE["teal"], lw=0.8)
plt.xlabel("Gossip round")
plt.ylabel("Sensed occupancy")
plt.title("Every junction settles on the same reading (mesh = 12,000)")
plt.ylim(0, 1)
plt.legend()
plt.tight_layout()
plt.savefig(os.path.join(PLOTS, "chartB_reading_band.png"))
plt.close()

# ---- Chart C: rerouting relief and lockups (mid-size mesh) ---------------
d = load("meshload_12000.dat")
fig, axL = plt.subplots(figsize=(6.8, 4.2))
lA = axL.plot(d["tick"], d["overCapShare"] * 100, "-", marker="o", ms=3, color=PALETTE["teal"],
             label="junctions past rerouting cap (%)")
axL.set_xlabel("Gossip round")
axL.set_ylabel("Over-cap junctions (%)", color=PALETTE["teal"])
axL.tick_params(axis="y", labelcolor=PALETTE["teal"])
axR = axL.twinx()
lB = axR.plot(d["tick"], d["peakLoad"], "-", marker="s", ms=3, color=PALETTE["maroon"], label="peak junction load")
axR.axhline(1.0, color=PALETTE["maroon"], ls="--", lw=1)
axR.set_ylabel("Peak load (fraction of capacity)", color=PALETTE["maroon"])
axR.tick_params(axis="y", labelcolor=PALETTE["maroon"])
axR.grid(False)
lines = lA + lB
axL.legend(lines, [l.get_label() for l in lines], loc="upper right")
plt.title("Adaptive rerouting relieves the mesh (size = 12,000)")
fig.tight_layout()
plt.savefig(os.path.join(PLOTS, "chartC_rerouting_relief.png"))
plt.close()

# ---- Chart D: trip agent throughput and detours (mid-size mesh) ----------
d = load("tripflow_12000.dat")
fig, axL = plt.subplots(figsize=(6.8, 4.2))
lA = axL.plot(d["tick"], d["arrived"], "-", marker="o", ms=3, color=PALETTE["sage"], label="trips arrived (cumulative)")
lB = axL.plot(d["tick"], d["diverted"], "-", marker="s", ms=3, color=PALETTE["plum"], label="trips diverted around load (cumulative)")
axL.set_xlabel("Gossip round")
axL.set_ylabel("Trips (cumulative)")
axR = axL.twinx()
lC = axR.plot(d["tick"], d["avgHops"], "-", marker="^", ms=3, color=PALETTE["gold"], label="avg hops per arrival")
axR.set_ylabel("Average hops", color=PALETTE["gold"])
axR.tick_params(axis="y", labelcolor=PALETTE["gold"])
axR.grid(False)
lines = lA + lB + lC
axL.legend(lines, [l.get_label() for l in lines], loc="upper left")
plt.title("Trip agents: local, load-aware routing (mesh = 12,000)")
fig.tight_layout()
plt.savefig(os.path.join(PLOTS, "chartD_trip_agents.png"))
plt.close()

# ---- Chart E: resilience under disruption rates ---------------------------
plt.figure(figsize=(6.8, 4.2))
cmap = [PALETTE["teal"], PALETTE["sage"], PALETTE["gold"], PALETTE["plum"], PALETTE["maroon"]]
for r, c in zip(DISRUPT_RATES, cmap):
    d = load(f"disruption_{r}.dat")
    plt.plot(d["tick"], d["devi"], "-", color=c, label=f"disruption {int(float(r)*100)}%/round")
plt.xlabel("Gossip round")
plt.ylabel("Reading spread (std. dev.)")
plt.title("Flow sensing under disruption: bounded, not broken")
plt.legend()
plt.tight_layout()
plt.savefig(os.path.join(PLOTS, "chartE_disruption_resilience.png"))
plt.close()

# ---- Chart F: scale-out summary (two panels) ------------------------------
fig, (axL, axR) = plt.subplots(1, 2, figsize=(9.6, 3.8))
labels = [f"{n:,}" for n in MESH_SIZES]
settle = [tick_to_settle(load(f"flowsense_{n}.dat")) for n in MESH_SIZES]
axL.bar(labels, settle, color=PALETTE["teal"])
for i, v in enumerate(settle):
    axL.text(i, v + 0.3, str(v), ha="center")
axL.set_xlabel("Mesh size")
axL.set_ylabel("Rounds to settle (devi < 0.02)")
axL.set_title("Flow sensing: settling time holds steady")

relief = [(1 - load(f"meshload_{n}.dat")["overCapShare"][-1] /
           load(f"meshload_{n}.dat")["overCapShare"][0]) * 100 for n in MESH_SIZES]
axR.bar(labels, relief, color=PALETTE["sage"])
for i, v in enumerate(relief):
    axR.text(i, v + 0.5, f"{v:.1f}%", ha="center")
axR.set_xlabel("Mesh size")
axR.set_ylabel("Drop in over-cap junctions (%)")
axR.set_title("Rerouting: relief holds steady")
axR.set_ylim(0, 105)
fig.tight_layout()
plt.savefig(os.path.join(PLOTS, "chartF_scaleout_summary.png"))
plt.close()

# ---- digest of headline numbers -------------------------------------------
for n in MESH_SIZES:
    m = load(f"flowsense_{n}.dat")
    digest.append(f"Flow sensing  size={n:>7}: devi<0.02 by round {tick_to_settle(m)}, "
                  f"final devi={m['devi'][-1]:.4f}, ground truth={m['mean'][-1]:.4f}")
for n in MESH_SIZES:
    ml = load(f"meshload_{n}.dat")
    tr = load(f"tripflow_{n}.dat")
    digest.append(f"Rerouting     size={n:>7}: overCap {ml['overCapShare'][0]*100:.1f}%->"
                  f"{ml['overCapShare'][-1]*100:.1f}%, peakLoad={ml['peakLoad'][-1]:.2f}, "
                  f"lockups={int(ml['lockups'][-1])}, arrived={int(tr['arrived'][-1])}, "
                  f"divertShare={tr['divertShare'][-1]*100:.1f}%, avgHops={tr['avgHops'][-1]:.2f}")
for r in DISRUPT_RATES:
    d = load(f"disruption_{r}.dat")
    tail = d["devi"][-10:]
    digest.append(f"Disruption {int(float(r)*100):>2}%: settled devi ~ {tail.mean():.4f} "
                  f"(mean tracks ground truth = {d['mean'][-10:].mean():.4f})")

text = "\n".join(digest)
with open(os.path.join(RESULTS, "digest.txt"), "w") as f:
    f.write(text + "\n")
print(text)
print("\nCharts written to:", PLOTS)
