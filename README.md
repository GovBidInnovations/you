# govbid-engine (v0.1)

This repository contains the **core engine** for GovBid’s compliance‑first, goods‑only solicitation intake system.  It is designed to be API‑first and ready for use in SaaS or investor‑grade environments.

The engine enforces the Prime Directive and policy pack controls by generating a structured **dossier** JSON from incoming solicitation data and rendering a deterministic Markdown report.  It is built around strict JSON schemas, deterministic gates, and versioned policy packs.

## What it does

* Produces an authoritative `dossier.json` matching your locked template.
* Generates a human‑readable `report.md` with gate outcomes and evidence.
* Enforces goods‑only scope, margin floors, funding hard stops and coverage rules.
* Provides a CLI entrypoint that can be wrapped by an API layer (e.g. FastAPI).

## Requirements

* Python 3.11+

## Getting started

1. **Install dependencies**:

   ```bash
   pip install -e ".[dev]"
   ```

2. **Add authoritative schemas**:  Place your locked schema files into `govbid/schemas/`:

   * `GovBid_DOSSIER_Template_v2.1.0.json`
   * `GovBid_Coverage_Bundle_v2.0.0.json`

3. **Build a new dossier**:

   ```bash
   govbid dossier new --out out/dossier.json
   ```

4. **Validate a dossier**:

   ```bash
   govbid dossier validate --in out/dossier.json
   ```

5. **Render a report**:

   ```bash
   govbid dossier render --in out/dossier.json --out out/report.md
   ```

6. **Run coverage gate**:

   ```bash
   govbid coverage gate --state "New York"
   ```

## Next steps

This engine is designed to be wrapped by a separate API layer (see the `govbid-api` repository) and front‑end interface.  Future enhancements include adding full PDF extraction, evidence ledger population and running all G0–G8 gates.
