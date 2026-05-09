# Step 1 — Create the Data Agent

**Goal:** Create a new Fabric IQ **Data Agent** item in your workspace.

## 1.1 Create the agent item

1. In your Fabric workspace, click **+ New item**.
2. Search for **Data Agent** (under Fabric IQ).
3. **Name:** `RM_Copilot`
4. **Display name:** `RM Copilot — ผู้ช่วย RM`
5. Click **Create**.

`[screenshot: New item picker → Data Agent]`

## 1.2 Tour the Data Agent designer

After creation, the designer opens with three tabs:

| Tab | Purpose |
|---|---|
| **Knowledge** | Where you attach Ontologies, Lakehouses, Semantic Models or KQL DBs as grounding sources |
| **Instructions** | Custom system prompt — tone, scope, do's & don'ts |
| **Test** | Chat playground to try prompts against the agent |

`[screenshot: Empty Data Agent designer with 3 tabs visible]`

## 1.3 Set basic identity

In the **Overview** / **Settings** pane:

- **Display name:** `RM Copilot — ผู้ช่วย RM`
- **Description:**
  > A relationship-manager assistant for our Thai retail bank. Answers natural-language questions over Customer, Products and Sales & Engagement ontologies. Use for lead qualification, cross-sell, and 1:1 customer briefings.
- **Default language:** `th-TH` (allow English fallback)

`[screenshot: Agent settings panel with name and description filled]`

## 1.4 Save

Click **Save** in the top bar. The agent is now created but not yet **grounded** — that's [Step 2](step-02-attach-ontology-and-tune.md).

## Common gotchas

- ❌ **Data Agent missing from "+ New item"** → capacity does not have Fabric IQ enabled, or you're in a personal workspace (Data Agent requires a non-My-Workspace).
- ⚠️ **Agent created in the wrong workspace** → ontologies and the agent should live in the same workspace for the simplest permission model.
