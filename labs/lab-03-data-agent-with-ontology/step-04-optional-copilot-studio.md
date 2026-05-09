# Step 4 — (Optional) Connect to Microsoft 365 Copilot Studio

**Goal:** Surface `RM_Copilot` inside Microsoft 365 Copilot as a **connected agent** so RMs can talk to it in the M365 Copilot pane (Word, Outlook, Teams, web Copilot).

> Only proceed if your tenant has **Microsoft 365 Copilot** licenses and **Copilot Studio**.

## 4.1 Prerequisites

- ✅ Step 3 completed (agent in Teams).
- ✅ A Copilot Studio license (per-user or per-tenant).
- ✅ Permission to create / edit Copilot Studio agents in your tenant.

## 4.2 Create a connected agent in Copilot Studio

1. Go to <https://copilotstudio.microsoft.com>.
2. Click **+ New agent**.
3. Choose **Build from blank** (we're wrapping the Fabric Data Agent).
4. Name it **`RM Copilot (Banking)`**.

`[screenshot: Copilot Studio new agent screen]`

## 4.3 Add the Fabric Data Agent as a knowledge source

1. In the Copilot Studio agent designer, open **Knowledge → + Add knowledge**.
2. Select **Microsoft Fabric → Data Agent**.
3. Pick the workspace, then `RM_Copilot`.

`[screenshot: Add knowledge dialog choosing Fabric Data Agent]`

## 4.4 Topic-route business questions

Add a high-priority **Topic** that routes any RM-style question (Thai or English) to the Fabric agent:

- **Trigger phrases:**
  - `lead qualification`
  - `customer 360`
  - `cross-sell`
  - `campaign performance`
  - `dormant customers`
  - `แนะนำลูกค้า`
  - `ลูกค้าศักยภาพสูง`
  - `ลูกค้า dormant`
- **Action:** Send query to the **Fabric Data Agent (`RM_Copilot`)** knowledge source.
- **Fallback:** Apologize and suggest the user open Fabric directly.

## 4.5 Test in Copilot Studio's test pane

Run the same prompts from [`prompts/lead-qualification-prompts.md`](prompts/lead-qualification-prompts.md). Expected behavior: the answer comes from the Fabric Data Agent, with the same tone and PII rules.

`[screenshot: Copilot Studio test pane with Fabric-grounded answer]`

## 4.6 Publish to M365 Copilot

1. Click **Channels → Microsoft 365 Copilot**.
2. Submit for tenant admin approval (if your tenant requires it).
3. Once approved, the agent appears in the **agents** picker inside M365 Copilot in Outlook / Teams / Word / web Copilot.

`[screenshot: M365 Copilot agent picker showing RM Copilot]`

## 4.7 End-to-end demo

In Outlook, draft an email to a customer. In the Copilot pane, choose **RM Copilot (Banking)** and ask:

> *Brief me on customer CUS0001234 — segment, products held, recent service tickets and any open campaign response.*

The agent should call into the Fabric Data Agent, traverse all 3 ontologies, and return a structured 1:1 customer brief — straight inside Outlook.

`[screenshot: Outlook with M365 Copilot pane showing customer brief]`

## 🎉 Lab 3 complete

You've turned a Fabric IQ ontology into a **published, governed AI assistant** sitting inside Teams *and* M365 Copilot. That is the headline payoff of Fabric IQ: business-shaped data, accessed by humans and agents, with one consistent semantic.

Lab 4 (Operations Agent on Digital Twin Builder + streaming) will be added later — the building blocks are in place.
