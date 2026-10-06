"""Build thesis evidence figures without running model inference or training.

Run with Python 3, numpy, scipy and matplotlib. Reads the local VAD export
and saved classification summaries in VAD_analysis_SHAP.ipynb.
"""
from pathlib import Path
import csv
import json
import re
import hashlib
import numpy as np
from scipy.stats import gaussian_kde, spearmanr, mannwhitneyu
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent.parent
OUT = HERE / 'media'
OUT.mkdir(exist_ok=True)
plt.rcParams.update({'font.family': 'DejaVu Sans', 'font.size': 10,
                     'axes.spines.top': False, 'axes.spines.right': False,
                     'axes.labelsize': 10, 'axes.titlesize': 11,
                     'savefig.dpi': 300, 'axes.axisbelow': True})
COLORS = {'control': '#0072B2', 'depression': '#D55E00'}
DIMS = ['valence', 'arousal', 'dominance']
KEYS = [f'{source}_{d}' for source in ['tweet', 'lyric'] for d in DIMS]
sums, counts, labels = {}, {}, {}
blank_rows = 0
csv.field_size_limit(100_000_000)
with (ROOT / 'tweet_lyrics_vad.csv').open(newline='') as f:
    for row in csv.DictReader(f):
        if row['disorder'] not in COLORS:
            continue
        aid = row['anonymized_author_id']
        if not aid:
            continue
        raw = np.array([float(row[k]) for k in KEYS])
        if not np.isfinite(raw).all():
            continue
        if not ((raw >= 1).all() and (raw <= 5).all()):
            raise ValueError('Raw VAD values outside expected [1,5] scale')
        x = np.clip((raw - 3) / 2, -1, 1)
        gap = np.abs(x[:3] - x[3:])
        features = np.r_[x, gap, np.linalg.norm(gap)]
        if aid in labels and labels[aid] != row['disorder']:
            raise ValueError('Conflicting participant labels')
        sums[aid] = sums.get(aid, np.zeros(10)) + features
        counts[aid] = counts.get(aid, 0) + 1
        labels[aid] = row['disorder']
        blank_rows += not row.get('tweet_model_text', '').strip()
ids = sorted(sums)
x = np.array([sums[k] / counts[k] for k in ids])
y = np.array([labels[k] for k in ids])
ns = {g: int((y == g).sum()) for g in COLORS}
assert ns == {'control': 3823, 'depression': 829}, ns

def finish(fig, name):
    fig.savefig(OUT / f'{name}.png', bbox_inches='tight', facecolor='white')
    plt.close(fig)

# Equal participant weights; densities normalized independently in each group.
fig, axes = plt.subplots(2, 3, figsize=(8.4, 5.6), layout='constrained')
for r, source in enumerate(['lyric', 'tweet']):
    for j, d in enumerate(DIMS):
        ax = axes[r,j]
        col = KEYS.index(f'{source}_{d}')
        lo, hi = x[:,col].min(), x[:,col].max()
        grid = np.linspace(max(-1,lo-.08), min(1,hi+.08), 300)
        for group,color in COLORS.items():
            density = gaussian_kde(x[y == group,col])(grid)
            ax.plot(grid,density,color=color,lw=1.8)
            ax.fill_between(grid,density,color=color,alpha=.12)
        ax.set_title(f'{source.title()} {d}')
        ax.set_xlabel('Participant mean score')
        if j == 0: ax.set_ylabel('Density')
        ax.grid(alpha=.15)
fig.legend([Line2D([],[],color=c,lw=2) for c in COLORS.values()],
           [f'{g.title()} (n = {ns[g]:,})' for g in COLORS],
           loc='upper center', bbox_to_anchor=(.5,1.09),ncol=2,frameon=False)
finish(fig,'evidence_vad_distributions')

# Replicate notebook's ten-test family, using U to compute Cliff's delta.
names = ['Tweet valence','Tweet arousal','Tweet dominance',
         'Lyric valence','Lyric arousal','Lyric dominance',
         'Absolute valence gap','Absolute arousal gap','Absolute dominance gap',
         'Euclidean VAD distance']
ps, deltas = [], []
for j in range(10):
    a,b = x[y=='depression',j],x[y=='control',j]
    u,p = mannwhitneyu(a,b,alternative='two-sided')
    ps.append(p);deltas.append(2*u/(len(a)*len(b))-1)
ps,deltas=np.array(ps),np.array(deltas)
order=np.argsort(ps)
q=np.empty(10)
q[order]=np.minimum(1,np.minimum.accumulate((ps[order]*10/np.arange(1,11))[::-1])[::-1])
order=np.argsort(deltas)
fig,ax=plt.subplots(figsize=(8.4,4.9),layout='constrained')
for pos,j in enumerate(order):
    ax.barh(pos,deltas[j],color=COLORS['depression'] if q[j]<.05 else '#90B5CD',height=.58)
    ax.text(.112,pos,f'{deltas[j]:+.3f}     {q[j]:.4f}',va='center',fontsize=9)
ax.text(.112,-1,'Delta       FDR q',fontsize=9,fontweight='bold')
ax.set_yticks(range(10),[names[j] for j in order]);ax.invert_yaxis()
ax.axvline(0,color='#444444',lw=.8)
ax.set_ylim(9.6,-1.5);ax.set_xlim(-.12,.205);ax.set_xticks([-.10,-.05,0,.05,.10])
ax.set_xlabel("Cliff's delta (depression minus control)")
ax.grid(axis='x',alpha=.15)
fig.legend([Line2D([],[],color=COLORS['depression'],lw=7),Line2D([],[],color='#90B5CD',lw=7)],
           ['FDR q < 0.05','FDR q ≥ 0.05'],loc='upper center', bbox_to_anchor=(.5,1.09),ncol=2,frameon=False)
finish(fig,'evidence_group_effects')

# One point per participant, plus coefficients for the overall/within-group claims.
fig,axes=plt.subplots(1,3,figsize=(8.4,3.8),layout='constrained')
correlations={}
for j,d in enumerate(DIMS):
    ax=axes[j];ly=x[:,j+3];tw=x[:,j]
    for group,color in COLORS.items():
        mask=y==group
        ax.scatter(ly[mask],tw[mask],s=5,alpha=.25,color=color,edgecolors='none',rasterized=True)
    correlations[d]={}
    values=[]
    for group,mask in [('Overall',np.ones(len(x),dtype=bool)),('Control',y=='control'),('Depression',y=='depression')]:
        rho=float(spearmanr(ly[mask],tw[mask]).statistic)
        correlations[d][group]=rho
        values.append(f'{group}: {rho:+.3f}')
    ax.set_title(d.title());ax.set_xlabel('Mean lyric score')
    ax.text(.03,.97,'Spearman rho\n'+'\n'.join(values),transform=ax.transAxes,va='top',fontsize=8,
            bbox={'facecolor':'white','alpha':.92,'edgecolor':'none','pad':3})
    if j==0:ax.set_ylabel('Mean tweet score')
    ax.margins(y=.3);ax.grid(alpha=.15)
fig.legend([Line2D([],[],marker='o',ls='',color=c) for c in COLORS.values()],
           [g.title() for g in COLORS],loc='upper center', bbox_to_anchor=(.5,1.09),ncol=2,frameon=False)
finish(fig,'evidence_vad_alignment')

# Parse stored printed summaries; retain their population fold SD (ddof=0).
nb=json.loads((ROOT/'VAD_analysis_SHAP.ipynb').read_text())
runs=[]
for index in [32,33,34,39]:
    txt=''.join(''.join(o.get('text',[])) for o in nb['cells'][index].get('outputs',[]))
    auc=re.findall(r'AUROC: ([\d.]+) \+/- ([\d.]+)',txt)
    ba=re.findall(r'Balanced Acc: ([\d.]+) \+/- ([\d.]+)',txt)
    assert len(auc)==len(ba) and auc
    runs.extend([list(map(float,a+b)) for a,b in zip(auc,ba)])
assert len(runs)==5
runs=np.array(runs)
methods=['Row-wise CV\nRandom forest','Participant-grouped CV\nRandom forest',
         'Grouped CV\nShuffled row labels','Participant means\nLogistic regression',
         'Participant means\nRandom forest']
fig,axes=plt.subplots(1,2,figsize=(8.4,4.0),sharey=True,layout='constrained')
for ax,start,title in zip(axes,[0,2],['AUROC','Balanced accuracy']):
    for i,row in enumerate(runs):
        ax.errorbar(row[start],i,xerr=row[start+1],fmt='o',capsize=3,
                    color='#D55E00' if i==0 else '#0072B2',ms=5)
        ax.text(.985,i-.20,f'{row[start]:.3f} ± {row[start+1]:.3f}',ha='right',fontsize=8)
    ax.axvline(.5,color='#555555',ls='--',lw=1)
    ax.set_xlim(.35,1);ax.set_ylim(4.6,-.65);ax.set_title(title)
    ax.set_xlabel('Mean score ± fold SD');ax.grid(axis='x',alpha=.15)
axes[0].set_yticks(range(5),methods)
finish(fig,'evidence_validation')

manifest={'data':'tweet_lyrics_vad.csv','notebook':'VAD_analysis_SHAP.ipynb',
          'rows':sum(counts.values()),'participants':ns,'blank_text_rows_retained':blank_rows,
          'normalization':'(raw - 3) / 2; clipped [-1,1]',
          'aggregation':'Mean by participant. Gaps/distance computed before aggregation.',
          'correlations':correlations,
          'group_tests':[{'feature':n,'delta':float(d),'p':float(p),'q':float(v)} for n,d,p,v in zip(names,deltas,ps,q)],
          'validation_summary':runs.tolist(),'validation_cells_zero_based':[32,33,34,39],
          'validation_error_bars':'Saved printed fold SD, ddof=0, rounded to three decimals',
          'inference_or_training_rerun':False}
(HERE/'evidence_figures_sources.json').write_text(json.dumps(manifest,indent=2)+'\n')
print('Created four figures for',ns,'participants; rows:',sum(counts.values()))
