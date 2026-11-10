# A manual walkthrough

This guide explains what to click, what should change and what the result means. The page works from the checked-in data; running Python is only needed to regenerate the extract or run tests.

## 1. Read the question before the shortlist

The project compares percentages reported in Table S1 of [Lee et al., 2020](https://doi.org/10.1126/sciimmunol.aba0759), obtained through [BioStudies](https://www.ebi.ac.uk/biostudies/studies/S-EPMC7755924). It is a structured analysis of published endpoint values, not a reanalysis of raw flow-cytometry events.

The question is deliberately narrow: which shared readouts decrease in the liver-associated comparison and increase in each of three intervention comparisons? Each comparison has its own control. Do not treat the four columns as a head-to-head treatment trial or combine their animals.

| Column | Difference calculated | State/function source | Values per group |
| --- | --- | --- | --- |
| Liver | SQ + liver minus SQ only | Figure 3F | 15 |
| DT | DT+ minus DT− | Figure 3I | 10 |
| 9H10 | 9H10 minus isotype | Figure 4D | 10 |
| CPI-1205 | CPI-1205 + anti-PD-1 minus anti-PD-1 | Figure 4G | 5 |

The 9H10 column is the antibody-versus-isotype contrast, not the 9H10 plus anti-PD-1 combination. DT is the source's diphtheria-toxin depletion comparison. These labels identify the reported groups; the page is not an experimental protocol.

## 2. Change the cutoff

Leave the cutoff at **5 percentage points** and keep the single-observation omission check enabled. The shortlist should show **ICOS + IFNγ**.

Change the cutoff to **10 points**. Only **ICOS** remains. IFNγ's full-data DT mean difference is +10.333 points, but its smallest one-observation-omission difference is +9.147 points. It therefore misses the stricter sensitivity rule. Disable the omission checkbox at ten points: IFNγ returns because the full-data differences all pass.

The cutoff is an exploratory choice, not a biological standard. A marker outside this rule can still be useful for another question. Increasing a cutoff does not validate the remaining marker.

## 3. Inspect one comparison

Select **ICOS** and **Liver-associated change**. The plot shows every included endpoint value. Black horizontal lines show group means:

- SQ only: 63.616%.
- SQ + liver: 24.687%.
- Difference: −38.929 percentage points.

A percentage-point difference is subtraction of percentages, not a relative percent change. The median difference is −45.9 points. The omission range is approximately −41.552 to −37.683 points.

For that range, remove one value from one group, recompute the mean difference, restore it, and repeat for every value in both groups. Report the minimum and maximum. This does not remove a matched pair or a whole animal across markers. It is not a confidence interval and cannot test batch reproducibility.

Open **Inspect source values and calculation**. Each record has its group, value and workbook sheet/cell. This table is also the alternative to hovering over dots. It lets a reader trace, for example, ICOS in Figure 3F to rows 4, columns C:Q and R:AF.

## 4. Keep the denominator visible

The state/function plot reports marker-positive percentages within KSP-tetramer-positive CD8+ cells. The abundance plot reports tetramer-positive percentages within all CD8+ cells. Those are different quantities.

The abundance plot follows the selected comparison but is not paired with the marker plot by animal. It is excluded from the shortlist rule and retained in every prospective template. A small abundance difference does not demonstrate equivalence or explain a state change.

## 5. Download a prospective record template

At the default setting, **Download readout / specimen template** produces a CSV with three endpoint rows: the abundance anchor, ICOS and IFNγ. At ten points with omission checking, it has two rows: abundance and ICOS.

The IDs, tissue site, aliquot, batch and measured values are intentionally blank. These are future records, not recovered identities. The export preserves the chosen cutoff and omission setting. It distinguishes phenotype measurements from stimulated intracellular cytokine measurements and includes fields for preparation/stimulation, acquisition/gating versions and QC exclusions.

This is a proposed recording schema, not a validated staining panel, acquisition method or laboratory protocol. A lab would need to review feasibility, controls and analysis plans before using it.

## 6. Finish with the limits

The 400 records are endpoint measurements, not 400 distinct mice. Stable animal/batch IDs and raw FCS files are unavailable in this extract; no cross-panel matching is inferred. Figure 3F contains 15 values per group despite the caption's general n=10 statement for panels other than E. All nonempty selected source values are retained; the discrepancy remains unresolved.

All contrasts come from one paper, and both the marker subset and directional rule were chosen retrospectively. The result is neither independent validation nor a novel mechanism. The project was developed with AI assistance and is not evidence that Cathy independently wrote all code or performed the source experiments.

For installation, checksum verification and tests, see [README.md](README.md).
