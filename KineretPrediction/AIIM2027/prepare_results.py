"""Build manuscript tables/figures from the immutable aggregate result import."""
from pathlib import Path
import hashlib
import shutil
import pandas as pd
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

HERE = Path(__file__).resolve().parent
SOURCE = HERE.parents[2] / 'Kineret-Prediction/results/aiim_results_2026-11-12'
# papers-drafts and Kineret-Prediction are sibling repositories.
TABLES = HERE / 'tables'
FIGURES = HERE / 'figures'
TABLES.mkdir(exist_ok=True)
FIGURES.mkdir(exist_ok=True)
ARMS = ['logreg', 'logreg_qa', 'strats', 'strats_qa', 'intervene_std',
        'intervene_sax', 'intervene_kb', 'intervene_kb_qa']
NAMES = ['Logistic Regression', 'Logistic Regression + QA', 'ss-STraTS', 'ss-STraTS + QA',
         'INTERVenE sigma', 'INTERVenE SAX', 'INTERVenE KB', 'INTERVenE KB + QA']
LABEL = dict(zip(ARMS, NAMES))
OUTCOMES = {
    'HYPERGLYCEMIA_EVENT': 'Hyperglycemia',
    'SEVERE_HYPERGLYCEMIA_EVENT': 'Severe hyperglycemia',
    'KIDNEY_COMPLICATION_EVENT': 'Kidney complication',
    'DEATH_EVENT': 'Mortality', 'HYPOGLYCEMIA_EVENT': 'Hypoglycemia',
    'SEVERE_HYPOGLYCEMIA_EVENT': 'Severe hypoglycemia',
    'CARDIO-VASCULAR_DISORDER_EVENT': 'Cardiovascular',
    'INFECTION_EVENT': 'Infection',
}

def read(name):
    return pd.read_csv(SOURCE / name)

def esc(value):
    return str(value).replace('&', r'\&').replace('_', r'\_').replace('%', r'\%')

def ci(row, key='estimate'):
    value = getattr(row, key)
    if pd.isna(value):
        return '--'
    return f"{value:.3f} [{row.lo:.3f}, {row.hi:.3f}]"

def table(name, headers, rows):
    columns = r'>{\raggedright\arraybackslash}p{3.2cm}>{\raggedright\arraybackslash}p{8.3cm}rr' if name == 'qa_attribution' else 'l' + 'r'*(len(headers)-1)
    text = '\\begin{tabular}{' + columns + '}\n\\toprule\n'
    if name == 'outcomes':
        text += r' & & & \multicolumn{2}{c}{Logistic Regression} & \multicolumn{2}{c}{ss-STraTS} & \multicolumn{3}{c}{INTERVenE} \\' + '\n'
        text += r'\cmidrule(lr){4-5}\cmidrule(lr){6-7}\cmidrule(lr){8-10}' + '\n'
    text += ' & '.join(headers) + r' \\' + '\n\\midrule\n'
    text += '\n'.join((r'\midrule' if row is None else row if isinstance(row, str) else ' & '.join(map(str, row)) + r' \\') for row in rows)
    text += '\n\\bottomrule\n\\end{tabular}\n'
    (TABLES / f'{name}.tex').write_text(text, encoding='utf-8')

metrics = read('primary/metrics.csv')
paired = read('primary/paired_contrasts.csv')
support = read('primary/support.csv')
assert set(metrics.arm) == set(ARMS)
assert metrics.n.unique().tolist() == [4508]
assert metrics.n_people.unique().tolist() == [3193]
assert set(metrics.k) == {4}
assert set(support.outcome) == set(OUTCOMES)
assert not metrics[(metrics.outcome.isin(['macro', 'weighted'])) &
                   metrics.metric.isin(['auprc', 'auroc'])].ci_reliable.eq(False).any()

MAIN_ARMS = [a for a in ARMS if a != 'intervene_std']
def bold(value, yes):
    return r'\textbf{' + value + '}' if yes else value

# QA model counts are calculated from the 13 means and 13 occurrence flags.
# Encoder totals include the supervised heads and are rounded (Supplementary Methods A).
PARAMETER_COUNTS = {
    'logreg': '25,687', 'logreg_qa': '26,129',
    'strats': '91,441', 'strats_qa': '94,769',
    'intervene_sax': '--', 'intervene_kb': r'$\approx$1.85M',
    'intervene_kb_qa': r'$\approx$1.86M',
}

def primary_rows(arms):
    rows = []
    maxima = [metrics[(metrics.arm.isin(arms)) & (metrics.outcome==o) & (metrics.metric==m)].estimate.max()
              for o,m in [('weighted','auprc'),('weighted','auroc'),('macro','auprc')]]
    los_min=metrics[(metrics.arm.isin(arms))&(metrics.outcome=='length_of_stay')&(metrics.metric=='mae_hours')].estimate.min()
    for arm in arms:
        if arm in ['strats','intervene_sax']: rows.append(None)
        d = metrics[(metrics.arm==arm)&(metrics.outcome=='weighted')].set_index('metric')
        macro = metrics[(metrics.arm==arm)&(metrics.outcome=='macro')&(metrics.metric=='auprc')].iloc[0]
        rows.append([LABEL[arm], PARAMETER_COUNTS[arm], bold(ci(d.loc['auprc']),np.isclose(d.loc['auprc'].estimate,maxima[0])),
                     bold(ci(d.loc['auroc']),np.isclose(d.loc['auroc'].estimate,maxima[1])),
                     bold(f'{macro.estimate:.3f}',round(macro.estimate,3)==round(maxima[2],3)),
                     bold(f"{metrics[(metrics.arm==arm)&(metrics.outcome=='length_of_stay')&(metrics.metric=='mae_hours')].iloc[0].estimate:.2f}",np.isclose(metrics[(metrics.arm==arm)&(metrics.outcome=='length_of_stay')&(metrics.metric=='mae_hours')].iloc[0].estimate,los_min))])
    return rows
headers = ['Model', 'Parameters', 'Weighted AUPRC', 'Weighted AUROC', 'Macro AUPRC', 'LoS MAE (h)']
table('primary', headers, primary_rows(MAIN_ARMS))
table('primary_all', headers, primary_rows(MAIN_ARMS))

q = paired[(paired.outcome == 'weighted') & (paired.metric == 'auprc') & paired.contrast.isin(['KB vs STraTS','KB vs SAX','QA in KB','QA in STraTS','QA in LogReg'])]
table('contrasts', ['Contrast', r'$\Delta$ AUPRC (95\% CI)', r'$q$'],
      [[esc(r.contrast), ci(r, 'delta'), f'{r.q_value:.4f}'] for r in q.itertuples()])
q = paired[(paired.contrast == 'QA in KB') & (paired.metric == 'auprc')]
table('qa_outcomes', ['Outcome', r'$\Delta$ AUPRC (95\% CI)', r'$q$'],
      [[OUTCOMES[o], ci(q[q.outcome == o].iloc[0], 'delta'), f'{q[q.outcome == o].iloc[0].q_value:.4f}'] for o in OUTCOMES])

rows = []
for o, label in OUTCOMES.items():
    sup = support[(support.outcome==o)&(support.split=='test')].iloc[0]
    vals = [metrics[(metrics.arm==a)&(metrics.outcome==o)&(metrics.metric=='auprc')].iloc[0].estimate for a in MAIN_ARMS]
    rows.append([label,str(sup.n_pos),f'{100*sup.prevalence:.2f}'] +
                [bold(f'{v:.3f}',round(v,3)==round(max(vals),3)) for v in vals])
rows.insert(0,r'\multicolumn{10}{l}{\textit{AUPRC (higher is better)}} \\')
rows.append(None)
rows.append(r'\multicolumn{10}{l}{\textit{Complication-onset MAE in hours (lower is better)}} \\')
for o,label in OUTCOMES.items():
    sup=support[(support.outcome==o)&(support.split=='test')].iloc[0]
    vals=[metrics[(metrics.arm==a)&(metrics.outcome==o)&(metrics.metric=='mae_hours')].iloc[0].estimate for a in MAIN_ARMS]
    rows.append([label,str(sup.n_pos),'']+[bold(f'{v:.2f}',round(v,2)==round(min(vals),2)) for v in vals])
table('outcomes', ['Outcome', r'$n_+$', r'\%','LR','LR+QA','ST','ST+QA','SAX','KB','KB+QA'], rows)

table('support', ['Split', 'Admissions', 'People'],
      [[split, f'{g.n_admissions.iloc[0]:,}', f'{g.n_people.iloc[0]:,}'] for split, g in support.groupby('split', sort=False)])

loo = read('loo/site_metrics.csv')
HOSPITAL_NAMES = {'Barzilai':'Barzilai University Medical Center','Bz':'Bnai Zion Medical Center',
                  'Gmc':'Galilee Medical Center','Hy':'Hillel Yaffe Medical Center',
                  'Poria':'Tzafon Medical Center (Poria)','Shamir':'Shamir Medical Center'}
loo_rows, prevalence_rows = [], []
for site,g in loo.groupby('hospital'):
    d = g[(g.metric=='auprc') & g.outcome.isin(OUTCOMES)].set_index('outcome').loc[list(OUTCOMES)]
    baseline = (d.prevalence**2).sum()/d.prevalence.sum()
    auprc = g[(g.metric=='auprc')&(g.outcome=='weighted')].iloc[0]
    auroc = g[(g.metric=='auroc')&(g.outcome=='weighted')].iloc[0]
    loo_rows.append([HOSPITAL_NAMES[site],f'{auprc.n:,}',f'{baseline:.3f}',ci(auprc),ci(auroc)])
    prevalence_rows.append([HOSPITAL_NAMES[site]]+[f'{100*v:.2f}' for v in d.prevalence])
table('loo',['Held-out hospital','Admissions','PR reference','AUPRC (95\% CI)','AUROC (95\% CI)'],loo_rows)
site_short={'Barzilai':'Barzilai','Bz':'Bnai Zion','Gmc':'Galilee','Hy':'Hillel Yaffe','Poria':'Tzafon (Poria)','Shamir':'Shamir'}
site_order=list(site_short)
table('loo_prevalence',['Outcome']+[site_short[h] for h in site_order],
      [[label]+[f"{100*loo[(loo.hospital==h)&(loo.outcome==o)&(loo.metric=='auprc')].iloc[0].prevalence:.2f}" for h in site_order] for o,label in OUTCOMES.items()])

cal = read('primary/calibration.csv')
table('calibration', ['Arm', 'Variant', 'Mean Brier', 'Mean ECE'],
      [[LABEL[a], {'raw':'Uncalibrated','validation_temperature':'Temperature-scaled'}.get(v,esc(v)), f'{g.brier.mean():.4f}', f'{g.ece_15.mean():.4f}'] for (a,v),g in cal[cal.arm.isin(MAIN_ARMS)].groupby(['arm','variant'])])
xai = read('xai/named_concept_attribution.csv')
xai_rows = []
qa_names={'INSULIN_ON_HYPERGLYCEMIA_PATTERN':'Insulin after hyperglycemia',
          'ROUTINE_GLUCOSE_MEASURE_PATTERN':'Routine glucose monitoring',
          'ROUTINE_GLUCOSE_MEASURE_ON_ADMISSION_PATTERN':'Glucose monitoring on admission',
          'ROUTINE_BASAL_DOSAGE_PATTERN':'Routine basal dosage'}
for o,label in OUTCOMES.items():
    g=xai[xai.outcome==o].copy()
    g['rank']=g.mean_contribution.abs().rank(method='min',ascending=False)
    selected=g[g.named_concept.str.contains('PATTERN') & (g['rank']<=25)].sort_values('rank')
    if xai_rows and len(selected): xai_rows.append(None)
    for i,(_,r) in enumerate(selected.iterrows()):
        name=r.named_concept
        suffix=''
        for value in ['False','Partial','True']:
            if name.endswith('_'+value):
                name=name[:-(len(value)+1)];suffix=' ('+value+')';break
        concept=qa_names.get(name,name.replace('_PATTERN','').replace('_',' ').lower())+suffix
        xai_rows.append([label if i==0 else '',esc(concept),int(r['rank']),f'{r.mean_contribution:.4f}'])
table('qa_attribution',['Outcome','QA concept','Rank','Mean score'],xai_rows)

diag = read('xai/reconstruction_validation.csv')
table('reconstruction', ['Layer', r'$R^2$', 'Active fraction', 'Validation tokens'],
      [[int(r.layer), f'{r.r2:.3f}', f'{r.active_fraction:.4f}', int(r.validation_tokens)] for r in diag.itertuples()])
stability = read('mediator_stability/stability_summary.csv')
table('stability', ['Perturbation', 'Family', 'Agreement (95\% CI)', 'Lost coverage (95\% CI)'],
      [[esc(c), f, ci(g[g.metric=='label_duration_agreement'].iloc[0]), ci(g[g.metric=='lost_baseline_coverage'].iloc[0])]
       for (c,f),g in stability.groupby(['condition','family'])])
reg = metrics[metrics.metric == 'mae_hours']
table('regression', ['Outcome'] + ['LR', 'LR+QA', 'ST', 'ST+QA', 'SAX', 'KB', 'KB+QA'],
      [[label] + [f'{reg[(reg.arm==a)&(reg.outcome==o)].iloc[0].estimate:.2f}' for a in MAIN_ARMS]
       for o,label in list(OUTCOMES.items())+[('length_of_stay','Length of stay')]])

los = reg[reg.outcome=='length_of_stay'].set_index('arm')
table('los', ['Model', 'LoS MAE, hours (95\% CI)'],
      [[LABEL[a], bold(ci(los.loc[a]), a=='intervene_kb')] for a in MAIN_ARMS])

plt.rcParams.update({'font.size':9, 'axes.spines.top':False, 'axes.spines.right':False,
                     'pdf.fonttype':42, 'savefig.dpi':300})
def save(fig, name):
    fig.savefig(FIGURES / (name+'.pdf'), bbox_inches='tight')
    fig.savefig(FIGURES / (name+'.png'), bbox_inches='tight')
    plt.close(fig)

fig, axes = plt.subplots(1,2,figsize=(10,4),layout='constrained')
for ax,metric,title in zip(axes,['auprc','auroc'],['A  Support-weighted AUPRC','B  Support-weighted AUROC']):
    d=metrics[(metrics.outcome=='weighted')&(metrics.metric==metric)].set_index('arm').loc[ARMS]
    y=np.arange(len(d)); ax.barh(y,d.estimate,color=['#9BA7B4']*4+['#D2A365','#C6B57B','#3679A8','#23988C'])
    ax.errorbar(d.estimate,y,xerr=np.maximum(0,np.vstack([d.estimate-d.lo,d.hi-d.estimate])),fmt='none',color='black',capsize=2,lw=.8)
    ax.set(yticks=y,yticklabels=NAMES if metric=='auprc' else ['']*len(y),xlabel=metric.upper(),title=title)
    ax.invert_yaxis()
save(fig,'updated_ladder')

fig,axes=plt.subplots(1,2,figsize=(10,4.5),layout='constrained')
for ax,outcomes,title in [(axes[0],['weighted','macro'],'A  Aggregate QA effect'),(axes[1],list(OUTCOMES),'B  Outcome-specific QA effect')]:
    d=paired[(paired.contrast=='QA in KB')&(paired.metric=='auprc')].set_index('outcome').loc[outcomes]
    y=np.arange(len(d)); ax.axvline(0,color='.65',ls='--',lw=.8)
    ax.errorbar(d.delta,y,xerr=np.maximum(0,np.vstack([d.delta-d.lo,d.hi-d.delta])),fmt='o',capsize=3,color='#3679A8')
    ax.set(yticks=y,yticklabels=[OUTCOMES.get(o,o.capitalize()) for o in outcomes],xlabel='AUPRC difference (KB + QA minus KB)',title=title)
    ax.invert_yaxis()
save(fig,'updated_qa_effect')

for src,name in [('embedding_geometry/embedding_umap','updated_embedding_umap'),
                 ('primary/reliability','updated_reliability')]:
    for ext in ['pdf','png']:
        shutil.copy2(SOURCE/(src+'.'+ext),FIGURES/(name+'.'+ext))

# Display the original top twelve signed contributions per outcome with clinical labels.
def clinical_label(concept):
    special = {
        'ANTIBIOTIC_BITZUA_EVENT_IV': 'IV antibiotic administration',
        'HYPERTONIC-SALINE_BITZUA_EVENT': 'Hypertonic saline administration',
        'INSULIN_ON_HYPERGLYCEMIA_PATTERN_False': 'Insulin after hyperglycemia (false)',
        'ROUTINE_BASAL_DOSAGE_PATTERN_False': 'Routine basal insulin dose (false)',
        'ROUTINE_GLUCOSE_MEASURE_PATTERN': 'Routine glucose monitoring',
    }
    if concept in special:
        return special[concept]
    return (concept.replace('_MEASURE_STATE_', ' state: ').replace('_MEASURE_TREND_', ' trend: ')
            .replace('_CONTEXT_', ' context: ').replace('_BITZUA', ' administration')
            .replace('_', ' ').lower().capitalize())

attributions = read('xai/named_concept_attribution.csv')
fig, axes = plt.subplots(4, 2, figsize=(12, 14), layout='constrained')
for ax, (outcome, group) in zip(axes.flat, attributions.groupby('outcome', sort=False)):
    ranked = group.loc[group.mean_contribution.abs().nlargest(12).index].sort_values('mean_contribution')
    ax.barh(ranked.named_concept.map(clinical_label), ranked.mean_contribution,
            color=np.where(ranked.mean_contribution >= 0, '#b44', '#4682b4'))
    ax.set_title(OUTCOMES[outcome])
    ax.tick_params(axis='y', labelsize=8)
    ax.axvline(0, color='black', linewidth=.5)
save(fig, 'updated_named_attribution')

# Audit narrative is maintained separately; regeneration must not overwrite author confirmations.
print('Generated manuscript tables and figures; retained manually maintained audit notes.')

fig, axes = plt.subplots(4,2,figsize=(11,11.5),layout='constrained',sharex=True)
plot_arms = ['logreg','strats','intervene_kb','intervene_kb_qa']
plot_labels = ['Logistic Regression','ss-STraTS','INTERVenE KB','INTERVenE KB + QA']
colors = ['#929ba5','#c39b45','#3679A8','#23988C']
for ax,(outcome,label) in zip(axes.flat,OUTCOMES.items()):
    d=metrics[(metrics.metric=='auprc')&(metrics.outcome==outcome)].set_index('arm').loc[plot_arms]
    prev=float(support[(support.split=='test')&(support.outcome==outcome)].prevalence.iloc[0])
    y=np.arange(len(plot_arms))
    ax.barh(y,d.estimate,color=colors,height=.6,alpha=.9)
    ax.errorbar(d.estimate,y,xerr=np.maximum(0,np.vstack([d.estimate-d.lo,d.hi-d.estimate])),fmt='none',ecolor='black',capsize=3,lw=1)
    ax.axvline(prev,color='#9c3046',ls='--',lw=1.4)
    ax.set(yticks=y,yticklabels=plot_labels,xlim=(0,.85),title=f'{label} (prevalence {prev:.2%})')
    ax.invert_yaxis(); ax.grid(axis='x',alpha=.16); ax.set_axisbelow(True)
    ax.tick_params(axis='both',labelsize=9)
for ax in axes[-1]:ax.set_xlabel('AUPRC')
fig.suptitle('Outcome-specific predictive discrimination',fontsize=15)
save(fig,'updated_prevalence_gain')

windows = read('multi_k/window_metrics.csv')
fig, ax = plt.subplots(figsize=(8,4.5),layout='constrained')
for a in ['strats','strats_qa','intervene_sax','intervene_kb','intervene_kb_qa']:
    d=windows[(windows.arm==a)&(windows.outcome=='weighted')&(windows.metric=='auprc')].sort_values('k')
    line,=ax.plot(d.k,d.estimate,marker='o',label=LABEL[a])
    ax.fill_between(d.k.to_numpy(),d.lo.to_numpy(),d.hi.to_numpy(),alpha=.12,color=line.get_color())
ax.set(xlabel='Observed days K (forecast ends at day 14)',ylabel='Support-weighted AUPRC',xticks=[2,3,4,5,6])
ax.legend(fontsize=8);save(fig,'updated_window_sensitivity')
# Full original training-support matrix documents the fixed head-selection decision.
# These historical training values must not be relabeled as current test prevalences.
from matplotlib.patches import Rectangle
support_design=pd.read_csv(SOURCE.parent/'full_bench_results/figures/fig1_target_support.csv')
order=list(OUTCOMES)+['KETOACIDOSIS_EVENT','HYPEROSMOLALITY_EVENT']
grid=support_design.pivot(index='target',columns='k',values='prevalence_train')
# Outcome spellings in historical export use the canonical *_EVENT names.
grid=grid.loc[order,sorted(grid.columns)]
heat=grid.to_numpy()*100
labels=list(OUTCOMES.values())+['Ketoacidosis (excluded)','Hyperosmolality (excluded)']
fig,ax=plt.subplots(figsize=(10.5,5.8),layout='constrained')
im=ax.imshow(heat,cmap='Blues',aspect='auto',vmin=0,vmax=48)
for i in range(heat.shape[0]):
    for j in range(heat.shape[1]):
        if heat[i,j]<1:
            ax.add_patch(Rectangle((j-.5,i-.5),1,1,fill=False,hatch='///',edgecolor='#aaaaaa',linewidth=0))
        ax.text(j,i,f'{heat[i,j]:.1f}%',ha='center',va='center',fontsize=8.2,color='white' if heat[i,j]>24 else '#222')
j=list(grid.columns).index(4)
ax.add_patch(Rectangle((j-.5,-.5),1,len(grid),fill=False,edgecolor='black',linestyle=':',linewidth=1.6))
ax.set(xticks=range(len(grid.columns)),xticklabels=[f'{k}' for k in grid.columns],yticks=range(len(labels)),yticklabels=labels,xlabel='Observation cutoff K (days)',title='Training support: hatching below 1%; dotted column K=4')
fig.colorbar(im,ax=ax,label='Training prevalence (%)',shrink=.7)
save(fig,'updated_support_heatmap')

# Descriptive subgroups on the existing pooled primary test predictions.
sg=read('primary/subgroups.csv')
subrows=[]
for typ in ['sex','age_band','hospital']:
    if subrows: subrows.append(None)
    names=sg[(sg.arm=='intervene_kb')&(sg.outcome=='weighted')&(sg.subgroup_type==typ)].subgroup.drop_duplicates()
    for name in names:
        d=sg[(sg.arm=='intervene_kb')&(sg.outcome=='weighted')&(sg.subgroup_type==typ)&(sg.subgroup==name)].set_index('metric')
        if typ=='sex':label={'0.0':'Female','1.0':'Male'}[str(name)]
        elif typ=='hospital':label=HOSPITAL_NAMES[name]
        else:
            label=str(name).replace('\ufffd','--').replace('?','--')+' years'
        def value(metric):
            row=d.loc[metric]
            return ci(row)+(r'$^{\dagger}$' if not row.ci_reliable else '') if pd.notna(row.estimate) else '--'
        subrows.append([esc(label),f'{d.n.iloc[0]:,}',value('auprc'),value('auroc')])
table('subgroups',['Subgroup','Admissions','Weighted AUPRC (95\% CI)','Weighted AUROC (95\% CI)'],subrows)
# Reliability diagrams with readable model labels and an explicit diagonal reference.
rel=read('primary/reliability.csv')
fig,axes=plt.subplots(4,2,figsize=(8.8,11),layout='constrained')
for ax,(outcome,label) in zip(axes.flat,OUTCOMES.items()):
    ax.plot([0,1],[0,1],color='.5',ls=':',lw=1)
    for arm,color in [('intervene_kb','#3679A8'),('intervene_kb_qa','#23988C')]:
        for variant,style in [('raw','-'),('validation_temperature','--')]:
            d=rel[(rel.outcome==outcome)&(rel.arm==arm)&(rel.variant==variant)].sort_values('mean_pred')
            ax.plot(d.mean_pred,d.mean_obs,marker='o',ms=3,color=color,ls=style,
                    label=('KB' if arm=='intervene_kb' else 'KB + QA')+(' uncalibrated' if variant=='raw' else ' temperature-scaled'))
    ax.set(title=label,xlabel='Mean predicted risk',ylabel='Observed proportion',xlim=(-.02,1.02),ylim=(-.02,1.02))
handles,labels=axes[0,0].get_legend_handles_labels()
fig.legend(handles,labels,loc='outside lower center',ncol=2,fontsize=9)
save(fig,'updated_reliability')
