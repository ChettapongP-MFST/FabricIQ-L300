# Instructor Guide — FabricIQ-L300 Workshop

This guide is for facilitators delivering the FabricIQ-L300 hands-on workshop. It covers timing, demo flow, common pitfalls, and quality bars.

## Audience profile

- Data architects, BI leads, AI / data engineers
- Comfortable with one cloud data platform (Synapse, Databricks, Snowflake, etc.)
- Have completed the level-200 [`FabricIQ`](https://github.com/ChettapongP-MFST/FabricIQ) workshop or equivalent

## Outcomes

By the end, every attendee should be able to:

1. Articulate where Fabric IQ sits in the Microsoft Fabric stack.
2. Author an ontology with entities, properties, bindings, and relationships.
3. Connect ontologies across business domains.
4. Build, tune, and publish a Data Agent grounded on those ontologies into Microsoft Teams.
5. (Optional) Surface the agent inside Microsoft 365 Copilot via Copilot Studio.

## Suggested 1-day agenda (Bangkok time)

| Time | Block | Notes |
|---|---|---|
| 09:00–09:30 | **Welcome + concept docs 01-02** | Lecture; use [docs/01-what-is-microsoft-fabric.md](../docs/01-what-is-microsoft-fabric.md) and [docs/02-what-is-fabric-iq.md](../docs/02-what-is-fabric-iq.md) |
| 09:30–10:00 | **Ontology theory** | [docs/03-ontology-concepts.md](../docs/03-ontology-concepts.md) — interactive, ask audience for examples from their org |
| 10:00–10:15 | Break + data generation kickoff | Have attendees run `python generate_batch_data.py` in the background |
| 10:15–11:45 | **Lab 1 — Ontology from scratch** | Customer domain only |
| 11:45–13:00 | Lunch | |
| 13:00–14:45 | **Lab 2 — Cross-Ontology** | Products + SalesEngagement + cross-domain edges |
| 14:45–15:00 | Break | |
| 15:00–16:30 | **Lab 3 — Data Agent + Teams** | Steps 1–3 mandatory; Step 4 (Copilot Studio) only if tenant allows |
| 16:30–17:00 | Wrap-up + Q&A | Demonstrate Lab 3 in Teams and (if available) M365 Copilot |

## 2-day expansion

- **Day 1**: Concepts + Lab 1 + Lab 2 + design clinic (attendees sketch ontologies for their own org)
- **Day 2**: Lab 3 in depth + Copilot Studio + roadmap to Lab 4 (Operations Agent on Digital Twin Builder)

## Demo flow tips

### Concept lecture
- Open Fabric portal in one tab, the docs in another. After explaining a concept, switch and *show* it (e.g., where Ontology lives in the workspace).
- Use the architecture mermaid diagrams in `docs/02` rather than ad-hoc whiteboarding.

### Lab 1
- Pre-create the Lakehouse for slow attendees from a fresh tenant.
- Common stuck point: type mismatches on `date_of_birth` and `onboarding_date`. Pre-stage the SQL view (Step 4.4) on a slide.

### Lab 2
- The big "aha" moment is **multi-hop questions** in 3.5 — budget time for the audience to play.
- If the cross-ontology UI behaves differently in your tenant, demo with the **Customer ontology** as the relationship owner and reference external entities only there.

### Lab 3
- Tenant policy almost always blocks side-loading Teams apps the first time. Loop in an admin **before** the workshop.
- Have a **canary prompt** ready that reliably exercises all 3 ontologies (use prompt A1 from the prompt library).

## Quality bars (instructor-grade)

| Lab | "Working" looks like | Stretch goal |
|---|---|---|
| 1 | All 5 entities bound + 4 relationships + previews show Thai names | Add `currentSegment` derived property via the history table |
| 2 | All 3 ontologies validate at 0 errors; one cross-domain question returns rows | Add geographic relationship `Branch nearTo Address` using lat/lon |
| 3 | Agent answers prompt A1 from the prompt library cleanly | Pass *all* negative tests in the prompt library (E1-E3) |

## Scoring rubric (for capstone / certification)

- Modeling quality: entity/property descriptions, naming consistency (10pt)
- Bindings: type cleanliness, view usage where needed (10pt)
- Relationships: correct cardinality, descriptive names, no orphan FKs (10pt)
- Agent behavior: grounded answers, PII enforcement, THB/Thai formatting (15pt)
- Storytelling: a 5-minute end-to-end demo of "find lead → brief → outreach" (5pt)

## Common audience questions & answers

**Q: Can I use my own data?**
Yes — the labs are dataset-agnostic. Replace the Lakehouse tables and adjust property names. Keep the 3-domain shape; it generalizes well.

**Q: Does Fabric IQ replace Power BI semantic models?**
No. Power BI semantic models are a *report-level* semantic. Fabric IQ ontologies are an *enterprise-level* business semantic that *can* feed semantic models, agents, twins, etc. They complement each other.

**Q: How does it handle row-level security?**
Permissions follow the underlying data sources (Lakehouse / Warehouse / KQL). The ontology + agent **don't** add row-level filters by themselves; layer RLS in the source.

**Q: Can ontologies be source-controlled?**
Yes via Fabric Git integration on the workspace — commit, branch, and PR ontology JSON like any other Fabric item.

## Post-workshop assets

- This repo (clone, fork, or use as workshop template)
- `prompts/lead-qualification-prompts.md` — keep extending it; it's the agent's regression suite
- `notebooks/streaming_to_eventhouse.ipynb` — bridge to Lab 4 when published
