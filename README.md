# James Lee Lab readout explorer

A small, AI-assisted descriptive reanalysis of published endpoint measurements. It asks which shared readouts satisfy a transparent directional rule across four contrasts, then exports a blank specimen-record template for a possible follow-up. It is a personal exploratory project, not a Lee Lab product or endorsement.

Start with [WALKTHROUGH.md](WALKTHROUGH.md) for a manual tour.

## What is included

- Four state/function readouts: PD-1, CTLA-4, ICOS and IFNγ.
- Four separate contrasts from one paper, each compared with its own control.
- Tetramer-positive abundance as context with a different denominator.
- 400 endpoint records and 20 descriptive comparisons. These are **not 400 unique mice**.
- Mean and median differences, source-cell references and leave-one-observation sensitivity ranges.

The default five-percentage-point rule, with the omission check enabled, retains ICOS and IFNγ. At ten points, only ICOS remains. These are rule-dependent, retrospective selections—not independent validation, treatment rankings, an optimal panel or a new mechanism. The shared-marker subset and direction rule were informed by this same paper.

## Run locally

The website is static and has no JavaScript build step. From the repository root:

```sh
python3 -m http.server 8000 --bind 127.0.0.1
```

Open [the local page](http://127.0.0.1:8000). Stop the server with Ctrl-C.

For analysis and tests, use Python 3.10 or newer and the pinned dependency in `requirements.txt`. The checked environment was Python 3.12.14 with openpyxl 3.1.5.

```sh
python3 -m venv .venv
.venv/bin/python -m pip install -r requirements.txt
.venv/bin/python -m unittest discover -s tests -v
```

## Reproduce the extract

Source: Lee JC et al. (2020), *Regulatory T cell control of systemic immunity and immunotherapy response in liver metastasis*, [doi:10.1126/sciimmunol.aba0759](https://doi.org/10.1126/sciimmunol.aba0759). Table S1 is available through [BioStudies S-EPMC7755924](https://www.ebi.ac.uk/biostudies/studies/S-EPMC7755924) and its [workbook download](https://www.ebi.ac.uk/biostudies/files/S-EPMC7755924/NIHMS1640106-supplement-Table_1.xlsx).

The complete source workbook is not redistributed. This command downloads it to `source-cache/TableS1.xlsx` if absent and regenerates `analysis.json`, `data.js`, `PROVENANCE.json` and `observations.csv`:

```sh
.venv/bin/python analysis.py
.venv/bin/python -m unittest discover -s tests -v
```

Alternatively, obtain the workbook from the archive, save it at that relative path, and run:

```sh
.venv/bin/python analysis.py --workbook source-cache/TableS1.xlsx
```

The verified source is 74,411 bytes; SHA-256:

```text
f7e31557b30b933c2d99029c8811a532ab3f3046a8f8c7cf4f240a27e8f2de46
```

Tests do not download data. They check shipped records, independently checked numerical fixtures and shortlist behavior. If `source-cache/TableS1.xlsx` is present, they also check its checksum and extraction; otherwise that source-dependent test is explicitly skipped. To test a workbook saved elsewhere without copying it into the repository, set `LEE_SOURCE_WORKBOOK` to its path when running the test command.

## Limits and attribution

Comparisons are unpaired. The extract supplies no stable animal IDs, batch IDs, raw FCS files, compensation information or gate-level counts; columns are not joined across panels. No source observations within the selected ranges are removed or imputed. No p-values are recalculated. Omission ranges are sensitivity ranges, not confidence intervals or evidence of between-experiment reproducibility.

Figure 3F has 15 nonempty workbook values per group, whereas the [Figure 3 caption](https://pmc.ncbi.nlm.nih.gov/articles/PMC7755924/#F3) gives n=15 for E and n=10 for the other panels. This project retains all 15 values per group and flags, rather than resolves, that discrepancy.

Analysis, interface and documentation were developed with AI assistance. The project does not establish Cathy's independent implementation or bench proficiency. Original measurements remain the authors' work. See [THIRD_PARTY_NOTICES.md](THIRD_PARTY_NOTICES.md) for source and reuse boundaries.
