#!/usr/bin/env python3
"""Auditable descriptive analysis of selected Lee et al. 2020 Table S1 cells.

Use --workbook /path/to/TableS1.xlsx, or download from the BioStudies archive.
No pooling of markers, animal matching, significance testing or prediction.
"""
import argparse
import csv
import hashlib
import json
import statistics as st
from pathlib import Path
from urllib.request import urlopen
import openpyxl

ROOT = Path(__file__).resolve().parent
SOURCE = 'https://www.ebi.ac.uk/biostudies/files/S-EPMC7755924/NIHMS1640106-supplement-Table_1.xlsx'
SOURCE_SHA256 = 'f7e31557b30b933c2d99029c8811a532ab3f3046a8f8c7cf4f240a27e8f2de46'
MARKERS = ['PD1', 'CTLA4', 'ICOS', 'IFNg', 'Tetramer abundance']
CONTRASTS = [
    dict(id='liver', label='Liver-associated change', short='Liver', sheet='Figure 3F', rows=[2,3,4,5],
         abundance_sheet='Figure 3E', abundance_row=2, header=1, a=list(range(3,18)), b=list(range(18,33)),
         a_label='SQ only', b_label='SQ + liver', source_a='SQ', source_b='SQ + Liver', expected=-1,
         description='Concurrent liver tumor minus SQ-only control; distant SQ-tumor immune cells.'),
    dict(id='dt', label='Treg depletion contrast', short='DT', sheet='Figure 3I', rows=[2,3,4,5],
         abundance_sheet='Figure 3H', abundance_row=2, header=1, a=list(range(13,23)), b=list(range(3,13)),
         a_label='DT−', b_label='DT+', source_a='SQ + Liver (-DT)', source_b='SQ + Liver (+DT)', expected=1,
         description='DT+ minus DT− in Foxp3-DTR mice with SQ and liver tumors; distinct experiment from the liver comparison.'),
    dict(id='9h10', label='Anti-CTLA-4 contrast', short='9H10', sheet='Figure 4D', rows=[8,9,10,11],
         abundance_sheet='Figure 4D', abundance_row=2, header=7, a=list(range(13,23)), b=list(range(3,13)),
         a_label='Isotype', b_label='9H10', source_a='iso', source_b='(9H10)', expected=1,
         description='9H10 minus isotype control in liver-tumor-bearing mice. This is NOT the 9H10 + anti-PD-1 combination.'),
    dict(id='ezh2', label='EZH2-inhibitor combination contrast', short='CPI-1205', sheet='Figure 4G', rows=[5,6,7,8],
         abundance_sheet='Figure 4G', abundance_row=2, header=4, a=list(range(3,8)), b=list(range(8,13)),
         a_label='Anti-PD-1', b_label='CPI-1205 + anti-PD-1', source_a='aPD1', source_b='EZH2i + aPD1', expected=1,
         description='CPI-1205 + anti-PD-1 minus anti-PD-1 alone in liver-tumor-bearing mice.'),
]

def delta(a, b):
    return st.mean(b) - st.mean(a)

def summarize(a, b):
    av, bv = [r['value'] for r in a], [r['value'] for r in b]
    estimates = [delta(av[:i]+av[i+1:], bv) for i in range(len(av))]
    estimates += [delta(av, bv[:i]+bv[i+1:]) for i in range(len(bv))]
    return dict(mean_a=st.mean(av), mean_b=st.mean(bv), delta=delta(av,bv),
                median_delta=st.median(bv)-st.median(av), loo_min=min(estimates),
                loo_max=max(estimates), n_a=len(av), n_b=len(bv))

def read_group(ws, row, cols, label):
    result=[]
    for col in cols:
        cell=ws.cell(row,col)
        if cell.value is None:
            continue
        assert isinstance(cell.value,(int,float)) and 0 <= cell.value <=100, cell.coordinate
        result.append(dict(value=float(cell.value), source_sheet=ws.title, source_cell=cell.coordinate, group=label))
    return result

def extract(path):
    wb=openpyxl.load_workbook(path,data_only=True)
    rows=[]
    results=[]
    for spec in CONTRASTS:
        ws=wb[spec['sheet']]
        for cols, expected in [(spec['a'],spec['source_a']),(spec['b'],spec['source_b'])]:
            assert all(str(ws.cell(spec['header'],c).value).strip()==expected for c in cols)
        for marker,row in zip(MARKERS[:4],spec['rows']):
            assert ws.cell(row,1).value==marker
        for marker,row in zip(MARKERS,spec['rows']+[spec['abundance_row']]):
            sheet=wb[spec['abundance_sheet']] if marker==MARKERS[-1] else ws
            if marker==MARKERS[-1]:
                expected_a,expected_b=spec['source_a'],spec['source_b']
                if spec['id']=='dt': expected_a,expected_b='SQ + Liver (DT-)','SQ + Liver (DT+)'
                if spec['id']=='9h10': expected_b='9H10'
                assert all(str(sheet.cell(1,c).value).strip()==expected_a for c in spec['a'])
                assert all(str(sheet.cell(1,c).value).strip()==expected_b for c in spec['b'])
                assert 'tet' in str(sheet.cell(2,1).value).lower() or 'tet' in str(sheet.cell(1,2).value).lower()
            a=read_group(sheet,row,spec['a'],spec['a_label'])
            b=read_group(sheet,row,spec['b'],spec['b_label'])
            assert len(a)==len(spec['a']) and len(b)==len(spec['b']), 'Missing source values must be reviewed'
            denominator='CD8+ T cells' if marker==MARKERS[-1] else 'KSP-tetramer+ CD8+ T cells'
            item=dict(marker=marker,contrast=spec['id'],denominator=denominator,unit='percentage points',
                      groups=dict(a=a,b=b),**summarize(a,b))
            results.append(item)
            for record in a+b:
                rows.append(dict(contrast=spec['id'],marker=marker,denominator=denominator,**record))
    provenance=dict(paper_doi='10.1126/sciimmunol.aba0759',archive='S-EPMC7755924',source_url=SOURCE,
                    source_sha256=hashlib.sha256(path.read_bytes()).hexdigest(),source_bytes=path.stat().st_size,
                    retrieved='2026-11-10',unit='One published endpoint observation, not a unique animal identifier',
                    record_count=len(rows),sheets=sorted({r['source_sheet'] for r in rows}))
    return dict(provenance=provenance,markers=MARKERS,contrasts=CONTRASTS,results=results),rows

def candidates(data, threshold=5, robust=True):
    output=[]
    for marker in MARKERS[:4]:
        accepted=True
        for spec in CONTRASTS:
            r=next(x for x in data['results'] if x['marker']==marker and x['contrast']==spec['id'])
            score=(-r['loo_max'] if robust else -r['delta']) if spec['expected']==-1 else (r['loo_min'] if robust else r['delta'])
            accepted &= score >= threshold
        if accepted: output.append(marker)
    return output

def main():
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--workbook',type=Path)
    args=ap.parse_args()
    path=args.workbook
    if path is None:
        path=ROOT/'source-cache'/'TableS1.xlsx'
        if not path.exists():
            path.parent.mkdir(exist_ok=True)
            with urlopen(SOURCE,timeout=60) as response: content=response.read()
            assert content[:2]==b'PK' and len(content)==74411, 'Download not the expected workbook'
            path.write_bytes(content)
    assert path.stat().st_size==74411, 'Unexpected source file size'
    assert hashlib.sha256(path.read_bytes()).hexdigest()==SOURCE_SHA256, 'Source checksum changed: review before reuse'
    data,rows=extract(path)
    (ROOT/'analysis.json').write_text(json.dumps(data,indent=2)+'\n')
    (ROOT/'data.js').write_text('window.LEE_DATA = '+json.dumps(data,separators=(',',':'))+';\n')
    (ROOT/'PROVENANCE.json').write_text(json.dumps(data['provenance'],indent=2)+'\n')
    with (ROOT/'observations.csv').open('w',newline='') as f:
        writer=csv.DictWriter(f,fieldnames=list(rows[0]));writer.writeheader();writer.writerows(rows)
    print(json.dumps(dict(records=len(rows),default_candidates=candidates(data),strict10_candidates=candidates(data,10))))

if __name__=='__main__': main()
