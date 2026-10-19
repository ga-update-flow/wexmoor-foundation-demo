"""Shared brand constants for the Wexmoor Foundation demo (used by image and PDF generators)."""
import json, os, random

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA = os.path.join(ROOT, "src", "data")

INDIGO = "#263B6A"
INDIGO_DARK = "#1B2B4F"
TERRA = "#CC5F3A"
GOLD = "#E3A73B"
SAGE = "#5E9A78"
SKY = "#8FB8C9"
CREAM = "#F5EFE6"
SAND = "#E6DED2"
INK = "#2E2E38"
FACETS = [INDIGO, "#3C5A93", TERRA, "#E07B4F", GOLD, "#F0C468", SAGE, "#7DB592", SKY]

# The "W" mark, in a 100 x 100 box.
W_POINTS = [(0, 8), (19, 8), (30, 60), (42, 20), (58, 20), (70, 60), (81, 8), (100, 8),
            (79, 92), (61, 92), (50, 48), (39, 92), (21, 92)]


def load(name):
    with open(os.path.join(DATA, name), encoding="utf-8") as f:
        return json.load(f)


def facet_triangles(seed=7, n=6):
    """Triangulated grid over the 100x100 box, each triangle with a palette colour."""
    rnd = random.Random(seed)
    step = 100 / n
    pts = {}
    for i in range(n + 1):
        for j in range(n + 1):
            jitter = 0 if i in (0, n) or j in (0, n) else step * 0.28
            pts[i, j] = (i * step + rnd.uniform(-jitter, jitter), j * step + rnd.uniform(-jitter, jitter))
    tris = []
    for i in range(n):
        for j in range(n):
            a, b, c, d = pts[i, j], pts[i + 1, j], pts[i + 1, j + 1], pts[i, j + 1]
            # colour drifts from indigo (left) to terracotta/gold (right)
            band = FACETS[min(len(FACETS) - 1, int((i + rnd.random() * 2) / (n + 2) * len(FACETS)))]
            band2 = rnd.choice(FACETS)
            tris.append(([a, b, c], band))
            tris.append(([a, c, d], band2 if rnd.random() < 0.35 else band))
    return tris
