#!/usr/bin/env python3

import os
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch

HERE = os.path.dirname(os.path.abspath(__file__))
PLOTS = os.path.join(HERE, "plots")
RESULTS = os.path.join(HERE, "results")
os.makedirs(PLOTS, exist_ok=True)

TEAL, MAROON, SAGE, GOLD, SLATE, PLUM, PALE = \
    "#0d5c63", "#8c2f39", "#4c7a5a", "#b8860b", "#3d4a5c", "#5e3a72", "#f3f1ea"


def box(ax, x, y, w, h, text, fc=PALE, ec=SLATE, fs=9.5, tc="black"):
    ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.02,rounding_size=0.07",
                                linewidth=1.3, edgecolor=ec, facecolor=fc))
    if text:
        ax.text(x + w / 2, y + h / 2, text, ha="center", va="center", fontsize=fs, color=tc)


def arrow(ax, x1, y1, x2, y2, color=SLATE):
    ax.add_patch(FancyArrowPatch((x1, y1), (x2, y2), arrowstyle="-|>",
                                 mutation_scale=13, linewidth=1.2, color=color))


# ============================ SYSTEM MAP ===================================
# A vertical, single-column "stacked layers" layout (deliberately different
# from a left-right box-and-arrow architecture diagram).
fig, ax = plt.subplots(figsize=(7.6, 9.6))
ax.set_xlim(0, 8); ax.set_ylim(0, 13); ax.axis("off")
ax.text(4, 12.6, "urbanflow - layered system map", ha="center", fontsize=13,
        fontweight="bold", color=TEAL)

box(ax, 0.4, 10.7, 7.2, 1.5, "", fc="white", ec=SLATE)
ax.text(4, 11.95, "Configuration layer", ha="center", fontsize=10.5, fontweight="bold", color=SLATE)
box(ax, 0.7, 10.85, 2.2, 0.85, "scenarios/*.cfg\n(mesh size, ticks,\nrates)", fc=PALE, ec=SLATE, fs=8)
box(ax, 3.1, 10.85, 2.0, 0.85, "thirdparty/\nPeerSim 1.0.5 jars", fc=PALE, ec=SLATE, fs=8)
box(ax, 5.3, 10.85, 2.0, 0.85, "code/urbanflow/\n*.java (9 classes)", fc=PALE, ec=SLATE, fs=8)

arrow(ax, 4, 10.7, 4, 10.15)

box(ax, 0.4, 7.4, 7.2, 2.55, "", fc="#eef4f2", ec=TEAL)
ax.text(4, 9.65, "Road mesh - N junctions, Watts-Strogatz overlay (k=8, beta=0.08)",
        ha="center", fontsize=9.6, fontweight="bold", color=TEAL)
for i, cx in enumerate([0.75, 2.35, 3.95, 5.55]):
    box(ax, cx, 8.2, 1.35, 1.2, "", fc="white", ec=TEAL)
    ax.text(cx + 0.67, 9.15, f"junction {i+1}", ha="center", fontsize=6.6, color=TEAL)
    box(ax, cx + 0.08, 8.65, 1.19, 0.42, "flow / junction\nprotocol", fc="#dcebe8", ec=TEAL, fs=5.4)
    box(ax, cx + 0.08, 8.28, 1.19, 0.32, "mesh view", fc="#f1e6d6", ec=GOLD, fs=5.4)
for x in [2.1, 3.7, 5.3]:
    arrow(ax, x, 8.8, x + 0.25, 8.8, color=GOLD)
ax.text(4, 7.65, "trip agents (TripAgentDispatcher) hop across this same mesh, layer above",
        ha="center", fontsize=7.4, color=SLATE, style="italic")

arrow(ax, 4, 7.4, 4, 6.85)

box(ax, 0.4, 4.9, 7.2, 1.85, "", fc="#f6efe3", ec=GOLD)
ax.text(4, 6.55, "Round-driven controls", ha="center", fontsize=10.2, fontweight="bold", color=GOLD)
box(ax, 0.65, 5.05, 2.15, 1.15, "Seeding\nWireWS mesh init,\nFlowSeedInit /\nJunctionSeedInit", fc="white", ec=GOLD, fs=7.2)
box(ax, 2.95, 5.05, 1.95, 1.15, "Dynamics\nDisruptionInjector,\nTripAgentDispatcher", fc="white", ec=GOLD, fs=7.4)
box(ax, 5.05, 5.05, 2.35, 1.15, "Logging\nFlowStatsLogger,\nJunctionStatsLogger,\nTripStatsLogger", fc="white", ec=GOLD, fs=7.0)

arrow(ax, 4, 4.9, 4, 4.35)

box(ax, 0.4, 2.3, 7.2, 1.9, "", fc="#efeaf2", ec=PLUM)
ax.text(4, 3.95, "Analysis pipeline", ha="center", fontsize=10.2, fontweight="bold", color=PLUM)
box(ax, 0.65, 2.45, 2.15, 1.1, "stdout tagged rows\n(log|, meshlog|, triplog|)", fc="white", ec=PLUM, fs=7.4)
box(ax, 3.0, 2.45, 1.9, 1.1, "results/*.dat", fc="white", ec=PLUM, fs=8.2)
box(ax, 5.1, 2.45, 2.3, 1.1, "generate_plots.py\n->  plots/chart*.png", fc="white", ec=PLUM, fs=7.6)
arrow(ax, 2.8, 3.0, 3.0, 3.0, color=PLUM)
arrow(ax, 4.9, 3.0, 5.1, 3.0, color=PLUM)

box(ax, 0.4, 0.4, 7.2, 1.5, "docs/ - written report referencing plots/*.png\n(Section 4 of the coursework document)",
    fc=PALE, ec=SLATE, fs=9)
arrow(ax, 4, 2.3, 4, 1.9, color=SLATE)

plt.tight_layout()
plt.savefig(os.path.join(PLOTS, "map0_system_layers.png"), dpi=140)
plt.close()

# ============================ ROUND WORKFLOW ===============================
# A vertical swimlane, distinct from a horizontal step diagram.
fig, ax = plt.subplots(figsize=(8.6, 7.2))
ax.set_xlim(0, 10); ax.set_ylim(0, 12); ax.axis("off")
ax.text(5, 11.6, "One experiment, round by round", ha="center", fontsize=13,
        fontweight="bold", color=TEAL)

steps = [
    (10.3, "Step 0 - parse scenarios/*.cfg, allocate N junction nodes", PALE, SLATE),
    (9.3, "Step 1 - init.mesh wires the Watts-Strogatz overlay", "#eef4f2", TEAL),
    (8.3, "Step 2 - init.seed sets each junction's starting reading / queue", "#eef4f2", TEAL),
]
for y, txt, fc, ec in steps:
    box(ax, 0.6, y, 8.8, 0.75, txt, fc=fc, ec=ec, fs=9.2)
    arrow(ax, 5.0, y, 5.0, y - 0.25, color=SLATE)

box(ax, 0.5, 4.5, 9.0, 3.55, "", fc="#f6efe3", ec=GOLD)
ax.text(5.0, 7.75, "repeat for every configured round", ha="center", fontsize=10.4,
        fontweight="bold", color=GOLD)
box(ax, 0.8, 6.6, 4.0, 0.95, "(a) controls fire:\nreshuffle order, disrupt / dispatch trips,\nloggers print one tagged row", fc="white", ec=GOLD, fs=7.6)
box(ax, 5.2, 6.6, 3.9, 0.95, "(b) every junction runs\none protocol step\n(gossip average or diffusion)", fc="white", ec=TEAL, fs=8.2)
arrow(ax, 4.8, 7.05, 5.2, 7.05, color=SLATE)
box(ax, 0.8, 5.3, 4.0, 1.05, "flow sensing:\npair with a neighbour,\nadopt the shared average", fc="#dcebe8", ec=TEAL, fs=8.0)
box(ax, 5.2, 5.3, 3.9, 1.05, "adaptive rerouting:\nshift queued vehicles to a\nquieter neighbour", fc="#eef4ec", ec=SAGE, fs=8.0)
arrow(ax, 2.8, 6.6, 2.8, 6.35, color=TEAL)
arrow(ax, 7.15, 6.6, 7.15, 6.35, color=SAGE)
arrow(ax, 9.3, 6.0, 9.3, 7.4, color=GOLD)
ax.text(9.62, 6.7, "next round", rotation=90, va="center", fontsize=8, color=GOLD)

box(ax, 2.5, 3.0, 5.0, 1.0, "Step 3 - redirect tagged stdout -> results/*.dat\n-> generate_plots.py -> plots/", fc=PALE, ec=SLATE, fs=9)
arrow(ax, 5.0, 4.5, 5.0, 4.0, color=SLATE)

plt.tight_layout()
plt.savefig(os.path.join(PLOTS, "map_round_workflow.png"), dpi=140)
plt.close()

# ====================== TERMINAL CAPTURE ====================================
def render_terminal(txt_file, png_file, title, max_lines=40):
    with open(os.path.join(RESULTS, txt_file), encoding="utf-8", errors="replace") as f:
        lines = [l.rstrip("\n") for l in f][:max_lines]
    h = 0.27 * (len(lines) + 3)
    fig = plt.figure(figsize=(10.2, h))
    ax = fig.add_axes([0, 0, 1, 1]); ax.axis("off")
    ax.add_patch(plt.Rectangle((0, 0), 1, 1, color="#161a1d"))
    ax.add_patch(plt.Rectangle((0, 0.965), 1, 0.035, color="#33383d"))
    for cx, cc in zip((0.015, 0.030, 0.045), ("#e0605a", "#e0b155", "#5cb37a")):
        ax.add_patch(plt.Circle((cx, 0.982), 0.007, color=cc))
    ax.text(0.5, 0.982, title, ha="center", va="center", color="#c9c9c9", fontsize=9.0,
            family="monospace")
    y = 0.94
    for ln in lines:
        if ln.startswith("$"):
            color = "#7ec98f"
        elif ln.startswith("#"):
            color = "#8a8f96"
        elif ln.startswith(("log|", "meshlog|", "triplog|")):
            color = "#7fb2d9"
        else:
            color = "#e2e2e2"
        ax.text(0.012, y, ln, ha="left", va="top", color=color, fontsize=7.8, family="monospace")
        y -= 0.90 / max(len(lines), 1)
    fig.savefig(png_file, dpi=150, facecolor="#161a1d")
    plt.close()


render_terminal("console_dump.txt",
                os.path.join(PLOTS, "term1_scenario_dump.png"),
                "python3 simulate_offline.py  -  scenario 1 + scenario 2 (mesh=12,000)")
render_terminal("full_run_dump.txt",
                os.path.join(PLOTS, "term2_full_run_dump.png"),
                "python3 simulate_offline.py  -  complete validation pass")

print("diagrams + terminal captures written to", PLOTS)
