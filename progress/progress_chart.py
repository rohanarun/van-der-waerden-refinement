"""Render progress/progress.png from progress/progress.json (needs matplotlib).

Step chart of the coefficient c over time, log scale. Each series holds its
value until it is superseded. Usage: python -B progress/progress_chart.py
"""
from datetime import datetime, timedelta, timezone
from fractions import Fraction
import json
from pathlib import Path

import matplotlib
matplotlib.use('Agg')
import matplotlib.dates as mdates
import matplotlib.pyplot as plt

HERE = Path(__file__).resolve().parent
data = json.loads((HERE / 'progress.json').read_text())

SURFACE = '#fcfcfb'
INK = '#0b0b0b'
INK2 = '#52514e'
GRID = '#e6e5e1'
COLORS = {'openai': '#eb6834', 'repo': '#2a78d6'}
MARKERS = {'openai': 's', 'repo': 'o'}


def parse(point):
    return (datetime.fromisoformat(point['date'].replace('Z', '+00:00')),
            float(Fraction(point['c'])))


end = max(parse(p)[0] for s in data['series'] for p in s['points']) + timedelta(days=3)
start = min(parse(p)[0] for s in data['series'] for p in s['points']) - timedelta(days=2)

fig, ax = plt.subplots(figsize=(10, 5.6), dpi=160)
fig.patch.set_facecolor(SURFACE)
ax.set_facecolor(SURFACE)

for series in data['series']:
    key = series['key']
    pts = [parse(p) for p in series['points']]
    xs = [t for t, _ in pts] + [end]
    ys = [c for _, c in pts] + [pts[-1][1]]
    ax.step(xs, ys, where='post', color=COLORS[key], linewidth=2,
            label=series['name'], zorder=3)
    ax.plot([t for t, _ in pts], [c for _, c in pts], linestyle='none',
            marker=MARKERS[key], markersize=8, color=COLORS[key],
            markeredgecolor=SURFACE, markeredgewidth=1.5, zorder=4)

# Selective direct labels: first OpenAI point, first and last repository points.
openai = data['series'][0]['points'][0]
repo = data['series'][1]['points']
for point, dx, dy, ha in ((openai, 0.5, 1.9, 'left'),
                          (repo[0], -0.6, 0.6, 'right'),
                          (repo[1], -0.3, 0.22, 'right'),
                          (repo[-1], -0.5, 1.9, 'right')):
    t, c = parse(point)
    ax.annotate(point['label'], (t, c),
                xytext=(t + timedelta(days=dx), c * dy),
                fontsize=9, color=INK2, ha=ha, va='center',
                arrowprops=dict(arrowstyle='-', color='#c9c8c3', lw=0.8,
                                shrinkA=0, shrinkB=5))

ax.set_yscale('log')
ax.set_ylim(3e-6, 2e-1)
ax.set_xlim(start, end)
ax.yaxis.set_major_formatter(matplotlib.ticker.FuncFormatter(
    lambda v, _: {1e-5: '1/100000', 1e-4: '1/10000', 1e-3: '1/1000',
                  1e-2: '1/100', 1e-1: '1/10'}.get(v, '')))
ax.xaxis.set_major_locator(mdates.DayLocator(interval=3))
ax.xaxis.set_major_formatter(mdates.DateFormatter('%b %d'))
ax.grid(axis='y', color=GRID, linewidth=1, zorder=0)
for side in ('top', 'right', 'left'):
    ax.spines[side].set_visible(False)
ax.spines['bottom'].set_color(GRID)
ax.tick_params(colors=INK2, labelsize=9, length=0)

fig.text(0.07, 0.95, 'Coefficient $c$ in $W_r(k) > k^{\\,c\\,k\\lfloor\\log_2 r\\rfloor}$ over time',
         fontsize=13, color=INK, va='top')
fig.text(0.07, 0.895, 'Log scale. Repository values are conditional on the upstream OpenAI lemmas and '
         'not independently reviewed.\nBefore Sept 23, 2026 no bound of this form was known (c = 0).',
         fontsize=8.5, color=INK2, va='top', linespacing=1.4)
fig.text(0.97, 0.02, 'Latest repository value is 4000× the OpenAI coefficient (and 7.7× the previous 1/193)',
         fontsize=9, color=INK, ha='right', va='bottom')
ax.legend(loc='upper left', frameon=False, fontsize=9, labelcolor=INK)
ax.yaxis.set_minor_locator(matplotlib.ticker.NullLocator())

fig.subplots_adjust(left=0.11, right=0.97, top=0.80, bottom=0.14)
fig.savefig(HERE / 'progress.png', facecolor=SURFACE)
fig.savefig(HERE / 'progress.svg', facecolor=SURFACE)
print('wrote', HERE / 'progress.png')
