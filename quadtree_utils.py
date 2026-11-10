"""Data generation, Quadtree building and plotting (adapted from quadtree_stations.ipynb)."""
import base64
import io

import matplotlib
matplotlib.use("Agg")  # non-GUI backend, required on a server / in Docker
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
import numpy as np
import pandas as pd
from pyquadtree import QuadTree  # package installed as "e-pyquadtree"

BBOX = (0, 0, 1000, 1000)


def generate_data(seed=42):
    """Simulated bike stations around centers of interest + random new stations."""
    rng = np.random.default_rng(seed)
    centers = {"Suburbs": (300, 650, 180, 90),
               "Petit-Port": (750, 250, 40, 30),
               "City-Centre": (200, 200, 50, 60),
               "Campus": (800, 800, 50, 20)}  # (x, y, dispersion, n)
    rows = []
    for name, (cx, cy, s, n) in centers.items():
        rows += [(x, y, name) for x, y in rng.normal([cx, cy], s, size=(n, 2))]
    rows += [(x, y, "New-Stations") for x, y in rng.uniform(0, 1000, size=(40, 2))]
    df = pd.DataFrame(rows, columns=["x", "y", "category"])
    # Clip inside the 1000 x 1000 map so every point fits in the Quadtree bbox
    df[["x", "y"]] = df[["x", "y"]].clip(0, 999.9).round(2)
    df.insert(0, "id", range(1, len(df) + 1))
    return df


def build_qt(df, capacity=8, depth_max=8):
    """Build a Quadtree; a node splits when it holds more than `capacity` points."""
    qt = QuadTree(bbox=BBOX, max_elements=capacity, max_depth=depth_max)
    qt.capacity = capacity
    qt.depth_max = depth_max
    for row in df.itertuples():
        qt.add(row.id, (row.x, row.y))
    return qt


def tracer(df, qt):
    """Draw Quadtree cells and stations; return the figure."""
    fig, ax = plt.subplots(figsize=(8, 7))
    for (x0, y0, x1, y1) in qt.get_all_bbox():
        ax.add_patch(Rectangle((x0, y0), x1 - x0, y1 - y0,
                               fill=False, edgecolor="black", linewidth=0.6))
    for q, g in df.groupby("category"):
        ax.scatter(g.x, g.y, s=6, label=q, zorder=3)
    ax.set_xlim(0, 1000)
    ax.set_ylim(0, 1000)
    ax.legend(fontsize=8)
    ax.set_title(f"Quadtree capacity = {qt.capacity}")
    return fig


def figure_to_base64(fig):
    """Encode a matplotlib figure as a base64 PNG for embedding in HTML."""
    buf = io.BytesIO()
    fig.savefig(buf, format="png", bbox_inches="tight")
    plt.close(fig)  # free memory between requests
    return base64.b64encode(buf.getvalue()).decode("ascii")


def generate_plot(capacity):
    """Full pipeline: data -> Quadtree -> base64 image + number of nodes."""
    df = generate_data()
    qt = build_qt(df, capacity=capacity)
    n_nodes = len(qt.get_all_bbox())
    return figure_to_base64(tracer(df, qt)), n_nodes
