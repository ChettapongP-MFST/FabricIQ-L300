# Lab 3 — Data Agent grounded on Fabric IQ ontologies

> **Component focus:** Fabric IQ Data Agent + Microsoft Teams + (optional) Microsoft 365 Copilot Studio
> **Scenario:** A "Lead Qualification" assistant for Relationship Managers — natural-language Q&A over our 3 banking ontologies, published to Teams, optionally connected as an agent in M365 Copilot Studio.
> **Estimated time:** 75–90 minutes
> **Level:** 300–400
> **Prerequisite:** [Lab 2](../lab-02-cross-ontology-relationships/README.md) completed and all 3 ontologies published.

## What you'll build

A **Data Agent** that:
- Is grounded on `BankingIQ_Customer`, `BankingIQ_Products` and `BankingIQ_SalesEngagement`
- Answers Thai/English questions in natural language with tables + charts
- Lives in the Fabric portal, **and** in **Microsoft Teams**
- Can be plugged into **Microsoft 365 Copilot Studio** as a connected agent (optional)

Sample questions you'll be able to ask once it's live:

> *"Find high-potential Mass-Affluent leads in Bangkok this month: customers aged 30–45, income ≥ 80,000 THB, no credit card, who interacted with us at least twice in the last 30 days."*

> *"Which campaigns in Q1 2026 had the highest conversion rate by segment, and what's the average ticket size in THB?"*

> *"List dormant Affluent customers (no transactions in 90 days) with investment holdings > 1M THB so I can prioritise outreach."*

## Steps

| # | Step | Outcome |
|---|---|---|
| 1 | [Create the Data Agent](step-01-create-data-agent.md) | New `RM_Copilot` Data Agent in your workspace |
| 2 | [Attach the three ontologies and tune behavior](step-02-attach-ontology-and-tune.md) | Agent grounded on all 3 ontologies with custom instructions |
| 3 | [Publish to Microsoft Teams](step-03-publish-to-teams.md) | Agent reachable from Teams chat |
| 4 | [(Optional) Connect to Microsoft 365 Copilot Studio](step-04-optional-copilot-studio.md) | Agent appears as a connected agent in M365 Copilot |

## Sample prompts

A library of lead-qualification and analytics prompts is in [`prompts/lead-qualification-prompts.md`](prompts/lead-qualification-prompts.md). Use them to stress-test the agent in Step 2.

## Conventions

- The agent's display name in Teams will be **"RM Copilot"** (Thai: **"ผู้ช่วย RM"**).
- All currency answers should be in **THB**, all dates in **Asia/Bangkok** local time.
- The agent must **never expose `national_id` or full PAN** in answers — you'll enforce this in Step 2 instructions.
