# chem-classifier
Purpose - Build **chemical classifier for rapid conversation screening** by representing and compiling all scheduled chemicals in structural graph form.

Why this matters:

- chemical synthesis pathways are complex
- keyword filtering alone often leads to overmoderation
- chemical nomenclature is difficult and inconsistent across IUPAC names, common names, salts, abbreviations, and minor wording variants
- many model deployments may not have reliable access to external chemistry databases during inference, so the classifier should not depend on live database lookup
- a structural representation should allow faster and more precise chemistry checks
- this may reduce keyword-based overmoderation while still surfacing genuinely risky cases

## Sarin Sample Set

The benchmark below summarizes current timing and correctness results across the tested models using the structure of Sarin and it's derivatives. 

![Benchmark results](benchmark_results_graph.png)

Important note:

- **Claude results in this repo were collected on a free account.**
- the benchmark is included to justify the approach by showing that the graph-based method can work across **multiple model families**, not just a single provider

## TODO

- Full list for OPCW
- Controlled substances
- ATF
- Precursors
