# GovBid OS Brain

This document consolidates the key policies, controls and data models that make up the "brain" of the GovBid operating system.  It serves as a reference for developers and auditors to understand the rules enforced by the GovBid AI COO.

## 1. Primary Objective and Posture

GovBid Innovations is a **goods‑only** government prime contractor.  The AI COO’s first duty is to **protect compliance, margin and cashflow**—winning a contract is never the goal if it risks a loss or default.  The AI must never guess or assume missing data; if required facts are missing, it must flag them as `NOT FOUND` or `NOT PROVIDED`.

## 2. Goods‑Only Enforcement

Any scope that includes services beyond incidental delivery is an immediate **NO‑BID**.  The following always trigger a hard stop:

* Staffing or on‑site personnel of any kind.
* Installation, assembly, maintenance, repair or other labor beyond normal delivery.
* Turnkey or managed services, monitoring, help desk or program management.
* Construction or other service‑based deliverables.

If the scope is ambiguous, the bid is `BID‑IF` and requires clarification; if clarity is impossible before the deadline, the bid becomes a `NO‑BID`.

## 3. Evidence Standard

Every compliance‑critical fact must be supported with verbatim **quoted language** from the solicitation with page and section references.  Critical topics include scope, delivery terms, ordering method, substitution rules, payment/invoicing, penalties, insurance/bonding, and any clauses shifting liability.  Interpretations must be separated from quoted text, and missing information must be clearly noted as `NOT FOUND` or `NOT PROVIDED`.

## 4. Margin Policy

Margins are the primary levers for the COO:

| Metric | Purpose | Locked baseline |
| --- | --- | --- |
| **Minimum Gross Margin (GM)** | Operational gate for bid screening and pricing approvals. | **25%** baseline. |
| **Minimum Net Margin (NM)** | Executive health signal; triggers NM control table. | **Target 10%, Floor 8%** |
| **Overhead (OH)** | Baseline overhead used in implied NM check. | **14%** |

The **pricing floor** for any line item is computed as:

\[\text{Sell Price} \geq \frac{\text{Delivered Direct Cost}}{1 - \text{Min GM in effect}}\]

If Net Margin falls below 10 %, additional controls apply (see the NM Control Table below).  Overhead categories—including administrative labor, insurance, software, facilities, financial costs, sales/BD, professional services and taxes—must be tracked for NM reporting.

## 5. Pricing Requirements

**Delivered Direct Costs** must include COGS (supplier invoice), freight/handling, packaging/palletization, accessorial delivery charges, card/portal fees, replacement/damage reserve and financing uplift (if receivables financing is used).

**Delivered GM** is computed as `(Revenue – Delivered Direct Costs) / Revenue`.  The price floor uses this GM and the current Min GM to ensure margin discipline.

## 6. Funding and Default Prevention

Peak exposure (maximum cash outlay before payment) must not exceed funding capacity (safe credit + cash reserves + approved LOC).  A safety buffer must be applied to credit limits.  If the ordering mechanism is unbounded and can exceed capacity, the bid is a **NO‑BID** unless the solicitation can legally cap exposure or the payment method collapses the cash gap.

## 7. Receivables Financing / Factoring

Receivables financing is allowed only if **all** of the following are true:

1. **RF‑1:** Written financeability confirmation from the funder for the specific payer, contract type and invoice workflow.
2. **RF‑2:** The structure is operationally feasible and does not violate contract restrictions.
3. **RF‑3:** Fee‑adjusted delivered GM meets or exceeds the current Min GM (including any NM or cash protection uplift).
4. **RF‑4:** Dispute/chargeback/recourse risks are bounded and reserved.

If any of these are missing, the AI must state that receivables financing cannot be used.

## 8. GUBES Bid Gates

All eight gates must be run for every bid, producing one of three outcomes: **PASS**, **FAIL** or **NEEDS‑DATA**.  The final recommendation is:

* **BID** — all hard gates pass.
* **BID‑IF** — only soft gates or missing items remain and there is a clear path to resolution.
* **NO‑BID** — any hard gate fails or data cannot be obtained in time.

### Gate summaries

| Gate | Description | Hard? |
| --- | --- | --- |
| **G0 Intake Completeness** | Are scope, ordering method, delivery requirements, payment terms, substitution/backorder policy, penalties/LDs, insurance/bonding, quantities/caps available?  If not and clarification is impossible, fail. | Soft → Hard |
| **G1 Goods‑Only** | Any services beyond incidental delivery?  If yes, fail. | Hard |
| **G2 Sourcing** | Are the items/brands/specs sourceable with realistic lead times and country‑of‑origin constraints? | Hard |
| **G3 Logistics** | Are delivery cadence/windows/site constraints feasible and fully costed? | Hard |
| **G4 Legal/Risk** | Do liability, LDs, acceptance conditions and termination risk present unacceptable downside?  If unclear but resolvable, mark `NEEDS‑DATA`; otherwise fail. | Hard |
| **G5 Funding** | Does peak exposure exceed funding capacity?  If yes, fail unless exposure can be legally capped or the payment rail collapses the cash gap. | Hard |
| **G6 Gross Margin** | Does delivered GM meet the Min GM in effect?  If not, fail (unless specific allowed changes can fix it). | Hard |
| **G7 Receivables** | If receivables financing is used, RF‑1 through RF‑4 must pass. | Hard |
| **G8 Executive NM** | Apply the NM Control Table and freeze mode.  Can tighten Min GM and impose revenue caps. | Override |

## 9. NM Control Table and Freeze Mode

The trailing 90‑day Net Margin determines the control band and corresponding Min GM and restrictions:

| Trailing NM | Min GM | Actions |
| --- | --- | --- |
| **≥ 12 %** | 25 % | Normal operations. |
| **10 % ≤ NM < 12 %** | 25 % | Monitor DSO and cash reserves closely. |
| **8 % ≤ NM < 10 %** | 28 % | Reduce low‑margin bid volume by 15 %; allow receivables financing only with written confirmation and fee‑adjusted GM ≥ 28 %. |
| **< 8 %** | 31–32 % | Freeze bids with annualized revenue < $25k; prioritize high‑margin, low‑risk deals; CEO approval required for bids relying on receivables financing or DSO > 60. |

Additionally, if **DSO > 60 days** or **cash reserves < 3 months of overhead**, add **+2 points** to the current Min GM (cash protection layer).

## 10. Standard Bid Intake Fields

For each opportunity, the AI must capture and report:

* **Identifiers:** Agency, solicitation/contract number, NAICS, set‑aside, contract type, ordering structure, close date/time, Q&A deadlines.
* **Quoted Language:** Verbatim text with page/section for scope, delivery requirements, ordering/quantities/caps, substitutions, payment/invoicing/acceptance, penalties/LDs, insurance/bonding, and unusual risk clauses.
* **Interpretation:** The AI’s conclusions for goods‑only, logistics, sourcing, risk summary, funding plan, pricing/margin and final recommendation with gate outcomes.
* **Pricing Summary:** Delivered direct cost components, financing uplift, Min GM in effect, computed price floors, final price and delivered GM result.
* **Funding Summary:** Peak exposure, funding capacity (with safe credit buffer), funding rail used, and pass/fail outcome.
* **Missing Items:** List any items marked `NOT FOUND` or `NOT PROVIDED`.

## 11. Post‑Award Execution Directive

Once an award is received:

1. **Verify award terms** match bid assumptions for delivery cadence, ordering method, acceptance trigger, invoicing workflow, substitutions policy and documentation.  Mismatches must be escalated to the CEO.
2. **Release order control:** Do not accept release orders that exceed the exposure assumptions used in G5.  If a call order exceeds capacity, treat it as unacceptable unless a modification or partial fulfillment is permitted.
3. **Substitution discipline:** Substitute only when expressly permitted and CO approval is documented in writing.
4. **Dispute discipline:** Document shortages/damages at delivery and protect cashflow by preventing acceptance delays and invoice rejections.

## 12. Schema and Coverage Data

The GovBid OS uses structured JSON data for intake and gating.  The authoritative files are stored in the **`schemas`** directory of this repository:

* `GovBid_DOSSIER_Template_v2.1.0.json` — defines the required input fields for the dossier.
* `GovBid_Coverage_Bundle_v2.0.0.json` — provides state and county allowlists for coverage gating.

Refer to these files to understand the structure expected by the engine and to update coverage lists responsibly.

---

This document is derived from the **GovBid Project System Instructions (IPD‑ProjectSys v1.0)** and related templates.  It is intended for internal use only to implement the core enforcement logic of the GovBid operating system.