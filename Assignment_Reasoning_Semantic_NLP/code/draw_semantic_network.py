# Q2(a) - Draw the semantic network and save it as semantic_network.png
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyArrowPatch

from q2_semantic_network import semantic_network

# Hand-placed positions so the labels do not overlap
pos = {
    "Airline": (0.0, 3.0),
    "Flight": (3.0, 3.0),
    "Passenger": (6.0, 3.0),
    "Departure Time": (1.2, 5.0),
    "Destination": (4.8, 5.0),
    "Delayed": (1.5, 1.2),
    "Cancelled": (4.5, 1.2),
    "Passenger Complaint": (6.0, -0.6),
    "Customer Support": (1.2, -0.6),
}
mine = {("Cancelled", "may cause", "Passenger Complaint"),
        ("Passenger", "makes", "Passenger Complaint"),
        ("Passenger Complaint", "is prioritised by", "Customer Support")}

fig, ax = plt.subplots(figsize=(11, 7.5))
for s, r, o in semantic_network:
    (x1, y1), (x2, y2) = pos[s], pos[o]
    colour = "#c0504d" if (s, r, o) in mine else "#4a5d73"
    # Horizontal edges must clear half the box width, which depends on the name length
    horizontal = abs(y2 - y1) < 0.3
    shrink_a = 4.5 * len(s) + 14 if horizontal else 38
    shrink_b = 4.5 * len(o) + 14 if horizontal else 38
    ax.add_patch(FancyArrowPatch((x1, y1), (x2, y2), arrowstyle="-|>", mutation_scale=18,
                                 color=colour, lw=1.6, shrinkA=shrink_a, shrinkB=shrink_b,
                                 linestyle="--" if (s, r, o) in mine else "-"))
    ax.text((x1 + x2) / 2, (y1 + y2) / 2, r, ha="center", va="center", fontsize=10, color=colour,
            style="italic", bbox=dict(boxstyle="round,pad=0.2", fc="white", ec="none"))
for name, (x, y) in pos.items():
    ax.text(x, y, name, ha="center", va="center", fontsize=11, fontweight="bold",
            bbox=dict(boxstyle="round,pad=0.55", fc="#dbe6f4", ec="#4a5d73", lw=1.4))

ax.plot([], [], color="#4a5d73", lw=1.6, label="Relationship from the given facts")
ax.plot([], [], color="#c0504d", lw=1.6, ls="--", label="My own added relationship")
ax.legend(loc="upper right", fontsize=9, frameon=False)
ax.set_xlim(-1.2, 7.4); ax.set_ylim(-1.4, 5.8); ax.axis("off")
ax.set_title("Semantic network – airline knowledge", fontsize=14, fontweight="bold")
out = Path(__file__).resolve().parent.parent / "semantic_network.png"
fig.savefig(out, dpi=160, bbox_inches="tight")
print("Saved", out)
