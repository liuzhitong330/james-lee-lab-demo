# Verification record

Checked 10 November 2026.

- Original archived workbook: 74,411 bytes; SHA-256 is recorded in PROVENANCE.json and asserted before analysis.
- Independent numeric audit used decimal arithmetic and a separate source-cell mapping, without importing the analysis module: all 400 source values, 20 comparisons, means, median differences and one-observation omission extrema agree within 1.2e-14.
- Selected source ranges contain no missing values. Figure 3F contains 15 observations per group; the caption discrepancy is retained as a limitation.
- Regression suite covers all contrasts, CSV/JSON agreement, denominators, source cells, unpaired omission logic and threshold-dependent shortlists.
- Static Ramani shell validator and JavaScript syntax check passed. The first viewport was compared with the Ramani reference at the same browser size.
- Browser: all 16 marker/contrast selections checked; 5-, 10- and 20-point states checked; omission toggle changes the 10-point shortlist as expected. Keyboard activation of a readout button updates the plot. Source values are available without hover.
- CSV export downloaded and inspected: blank prospective identifiers, one abundance anchor and two marker rows at the default setting; no fabricated measured values.
- Responsive review used a 390px iframe viewport, not a physical mobile device. Controls wrap, the shortlist remains readable, and native form controls remain available.
- Browser console showed no errors or warnings during the tested interactions.

These checks establish arithmetic, traceability and tested interface behavior—not experimental validity, clinical utility, adoption by the lab or independent prospective validation.
