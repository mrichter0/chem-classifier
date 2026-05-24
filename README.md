# chem-classifier

**This is not a working model.**

This repository is a **design plan and experiment scaffold**, not a finished chemistry classifier. The current goal is to test whether molecular graphs can be serialized into a simple text format and used as prompt inputs for rapid LLM-based classification and substructure reasoning.

## Current Idea

The working design is:

- convert `.mol` and `.sd` chemistry files into simplified graph text
- prompt an LLM with those graphs
- compare model speed and correctness on controlled graph-search tasks
- use the results to decide whether this can become a practical rapid classifier

The current repository contains:

- small molecule and SD examples
- graph-generation scripts
- VF2 query scripts
- benchmark outputs
- an initial benchmark visualization

## Benchmark Snapshot

The benchmark below summarizes current timing and correctness results across the tested models:

![Benchmark results](benchmark_results_graph.png)

Important note:

- **Claude results in this repo were collected on a free account to avoid bias in the comparison.**

## Status

At the moment, this project should be read as:

- a prompt-and-graph design study
- a benchmark repo
- a staging area for future classifier work

It should **not** be interpreted as a validated production model, a finished structure-search engine, or a regulatory decision tool.

## TODO

- Full list for OPCW
- Controlled substances
- ATF
- Precursors
