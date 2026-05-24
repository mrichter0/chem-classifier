# chem-classifier

**This is not a working model.**

This repository is a **design plan and experiment scaffold**, not a finished chemistry classifier. The current goal is to design a **chemical database / classifier for rapid intent screening** by representing flagged chemicals in structural graph form and testing whether LLMs can reason over those graphs quickly and consistently.

## Purpose

The core idea is to support fast chemistry safety checks by scanning user context against a structure-based red-flag list.

Why this matters:

- chemical synthesis pathways are complex
- keyword filtering alone is easy to over-trigger or miss
- a structural representation should allow faster and more precise chemistry checks
- this may reduce keyword-based overmoderation while still surfacing genuinely risky cases

## Current Idea

The working design is:

- build a red-flag chemistry list in structural form
- convert `.mol` and `.sd` chemistry files into simplified graph text
- prompt an LLM with those graphs
- compare model speed and correctness on controlled graph-search tasks
- use the results to decide whether this can become a practical rapid classifier for intent screening

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
- the benchmark is included to justify the approach by showing that the graph-based method can work across **multiple model families**, not just a single provider

## Status

At the moment, this project should be read as:

- a prompt-and-graph design study
- a proposed structure-based intent-classification approach
- a benchmark repo
- a staging area for future classifier work

It should **not** be interpreted as a validated production model, a finished structure-search engine, or a regulatory decision tool.

## TODO

- Full list for OPCW
- Controlled substances
- ATF
- Precursors
