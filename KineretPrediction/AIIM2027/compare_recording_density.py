"""Descriptive recording-density comparison; no model evaluation or patient-level export."""
from pathlib import Path
import pandas as pd
import json
HERE = Path(__file__).resolve().parent
SOURCE = HERE.parents[2] / 'mimic-dataset/output/concept_events.csv'
SELECTED = ['GLUCOSE_MEASURE','CREATININE_SERUM_MEASURE','HEART_RATE_MEASURE','BODY_TEMPERATURE_MEASURE','BODY_TEMPERATURE']
parts, anchors, ends = [], [], []
for chunk in pd.read_csv(SOURCE, usecols=['PatientId','ConceptName','StartDateTime'], chunksize=1000000):
    chunk['ConceptName'] = chunk.ConceptName.replace({'BODY_TEMPERATURE':'BODY_TEMPERATURE_MEASURE'})
    chunk['StartDateTime'] = pd.to_datetime(chunk.StartDateTime, errors='raise')
    anchors.append(chunk.loc[chunk.ConceptName=='ADMISSION'].groupby('PatientId').StartDateTime.min())
    ends.append(chunk.groupby('PatientId').StartDateTime.max())
    parts.append(chunk.loc[chunk.ConceptName.isin(SELECTED)].copy())
anchor = pd.concat(anchors).groupby(level=0).min()
end = pd.concat(ends).groupby(level=0).max()
eligible = anchor.index[(end.reindex(anchor.index)-anchor).dt.total_seconds()>96*3600]
r = pd.concat(parts,ignore_index=True)
r = r.loc[r.PatientId.isin(eligible)].copy()
r['hour']=(r.StartDateTime-r.PatientId.map(anchor)).dt.total_seconds()/3600
r = r.loc[r.hour.between(0,96)]
before=len(r); r=r.drop_duplicates(['PatientId','ConceptName','StartDateTime'])
rows=[]
for c,g in r.groupby('ConceptName'):
    counts=g.groupby('PatientId').size().reindex(eligible,fill_value=0)/4
    ordered=g.sort_values(['PatientId','StartDateTime'])
    gaps=ordered.groupby('PatientId').hour.diff().groupby(ordered.PatientId).median().dropna()
    rows.append(dict(concept=c,n_admissions=len(eligible),coverage=(counts>0).mean(),daily_median=counts.median(),daily_q25=counts.quantile(.25),daily_q75=counts.quantile(.75),gap_n=len(gaps),gap_median=gaps.median(),gap_q25=gaps.quantile(.25),gap_q75=gaps.quantile(.75)))
result=pd.DataFrame(rows)
result.to_csv(HERE/'mimic_recording_density.csv',index=False)
(HERE/'mimic_recording_density_design.json').write_text(json.dumps(dict(window_hours=96,source=str(SOURCE),population='processed MIMIC cohort admissions with explicit admission marker and any raw timestamp beyond 96 hours; all partitions, not original test split',deduplicate='admission/concept/timestamp',duplicates_removed=before-len(r)),indent=2))
print(result.to_string(index=False))
