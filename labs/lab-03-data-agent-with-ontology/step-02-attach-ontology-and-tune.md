# Step 2 — Attach the ontologies and tune the agent

**Goal:** Ground `RM_Copilot` on all 3 ontologies, write a strong instruction prompt, and validate behavior with the prompt library.

## 2.1 Attach knowledge sources

In the agent designer → **Knowledge** tab → **+ Add knowledge**:

| # | Type | Item |
|---|---|---|
| 1 | Ontology | `BankingIQ_Customer` |
| 2 | Ontology | `BankingIQ_Products` |
| 3 | Ontology | `BankingIQ_SalesEngagement` |

> **Recommended:** also add the **Lakehouse `BankingIQ_LH`** as a fallback source (for ad-hoc columns not yet modeled).

For each ontology, set:
- **Use cross-ontology relationships:** ✅ ON
- **Default grounding priority:** Ontology > Lakehouse

`[screenshot: Knowledge tab with 3 ontologies attached]`

## 2.2 Write the agent instructions

Click the **Instructions** tab and paste the following (edit the bank name and policies for your real environment):

```text
You are "RM Copilot" — an assistant for Relationship Managers at a Thai retail bank.

LANGUAGE
- Reply in the user's language. Default to Thai if ambiguous. Render Thai names in Thai script.
- All monetary values are in THB; format with thousands separators and the ฿ symbol (e.g., ฿1,250,000).
- All dates are in Asia/Bangkok local time. Use ISO format (YYYY-MM-DD) for filters and "DD MMM YYYY" for display.

GROUNDING
- Use the three Fabric IQ ontologies as the source of truth: Customer, Products, SalesEngagement.
- Prefer ontology relationships over hand-written joins. Always traverse via cross-ontology edges
  (e.g., Customer.holdsCard, Customer.respondedTo, Customer.owns).
- If a question is ambiguous (e.g., "best customers"), ask one clarifying question before answering.

DATA POLICIES (must follow)
- Never reveal: national_id, full card numbers (PAN), or full account numbers. Mask them as XXXX-#### where applicable.
- Never disclose customers flagged with `KycRecord.pepFlag = true` to non-compliance roles. If asked,
  return "ข้อมูลนี้ไม่สามารถแสดงได้ในบริบทนี้" / "This information is not available in this context."
- Always include `customerId` (CUSxxxxxxx) in any list of customers so the RM can act on it.

ANSWER STYLE
- For list questions: return a Markdown table with at most 25 rows, plus a short Thai summary.
- For aggregate questions: return a 1-line headline number first, then a small breakdown table.
- For trend questions: return both the table and a chart suggestion ("show me a column chart of...").

LEAD QUALIFICATION DEFINITIONS (use these unless overridden)
- "High-potential lead" = active customer where:
    inSegment IN ('Mass-Affluent','Affluent') AND
    monthlyIncomeThb >= 80000 AND
    EXISTS Customer.respondedTo with outcome='Interested' in last 90 days AND
    NOT EXISTS Customer.holdsCard with cardType='Credit' AND status='Active'.
- "Dormant" = no ServiceInteraction AND no DepositTransaction in last 90 days.

OUT OF SCOPE
- Do not answer questions that require data not in the ontologies (e.g., live FX rates, stock prices).
- Do not give legal, tax, or specific investment advice. Suggest the customer contact a wealth advisor.
```

`[screenshot: Instructions tab populated with the prompt above]`

## 2.3 Test with the prompt library

Open the **Test** tab and run prompts from
[`prompts/lead-qualification-prompts.md`](prompts/lead-qualification-prompts.md). Iterate on the
instructions until each prompt returns a useful, on-policy response.

For each prompt, check:

| Check | Pass criteria |
|---|---|
| Grounded? | The reply cites entity / property names from the ontologies (e.g., `holdsCard`, `respondedTo`) |
| THB / Thai? | Amounts are `฿`-formatted; Thai names rendered in Thai script |
| PII safe? | No `national_id`, no full PAN, masked account numbers |
| Cross-ontology? | The answer joins across at least 2 ontologies for multi-hop prompts |
| Has `customerId`? | Lists include `CUS…` ids |

`[screenshot: Test tab showing a successful multi-hop answer]`

## 2.4 Tune by adding examples (few-shot)

If the agent gets a class of questions consistently wrong, add **example prompts + ideal answers** in the Instructions tab (most Data Agent flavors support a few-shot section). For example:

```text
EXAMPLES
Q: หาลูกค้า Mass-Affluent ในกรุงเทพที่ตอบ campaign บัตรเครดิตและยังไม่มีบัตรเครดิต
A: (return CUS-list table with fullName | province | segmentName | monthlyIncomeThb | lastResponseDate)
```

## 2.5 Save and version

Click **Save** to lock in this version. Most environments allow you to compare versions later when behavior regresses.

## 2.6 Publish

Click **Publish** when test prompts behave correctly. Publishing makes the agent available to other surfaces — Teams ([Step 3](step-03-publish-to-teams.md)) and Copilot Studio ([Step 4](step-04-optional-copilot-studio.md)).

`[screenshot: Publish dialog]`
