import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import Polygon
import numpy as np
import json

with open('data/geojson/sample_cadastral.geojson') as f:
    geo = json.load(f)

fig, ax = plt.subplots(figsize=(6, 4), dpi=150)
ax.set_aspect('equal')
colors = ['#1B3A2A', '#BFA15F', '#C19A6B', '#4A7C59', '#D4AF37']
for i, feat in enumerate(geo['features'][:5]):
    coords = feat['geometry']['coordinates'][0]
    lons = [c[0] for c in coords]
    lats = [c[1] for c in coords]
    poly = Polygon(np.column_stack([lons, lats]), closed=True, facecolor=colors[i%len(colors)], edgecolor='#0F2847', alpha=0.75, linewidth=1.5)
    ax.add_patch(poly)
    cx, cy = np.mean(lons), np.mean(lats)
    ax.text(cx, cy, feat['properties']['khasra_no'], fontsize=7, ha='center', va='center', color='white', weight='bold')

ax.set_xlim(85.823, 85.835)
ax.set_ylim(20.295, 20.305)
ax.axis('off')
ax.set_title('Sample Cadastral Layer — Khordha\nParcel Polygons (Balarampur / Golabai)', fontsize=10, pad=10, color='#0F2847', weight='bold')
legend_text = "BLR-118/2  ·  BLR-118/4  ·  GOL-227/1  ·  JNK-340\nArea: 0.46 ha  ·  0.30 ha  ·  0.81 ha  ·  1.21 ha"
ax.text(0.02, 0.02, legend_text, transform=ax.transAxes, fontsize=6, verticalalignment='bottom',
        bbox=dict(boxstyle='round,pad=0.3', facecolor='white', alpha=0.9, edgecolor='#1B3A2A', linewidth=0.8))
plt.tight_layout()
plt.savefig('assets/gis_map.png', dpi=150, bbox_inches='tight', facecolor='white')
plt.close()
print('GIS map generated at assets/gis_map.png')
