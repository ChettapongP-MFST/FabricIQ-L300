# Step 2 — Create the Ontology and the Customer Business Domain

**Goal:** Create a Fabric IQ **Ontology** item and add a **Business Domain** called *Customer*.

## 2.1 Create the Ontology item

1. In your workspace, click **+ New item**.
2. Search for **Ontology** (under Fabric IQ).
3. Name it **`BankingIQ_Customer`** and click **Create**.

`[screenshot: New item picker → Ontology]`

> **Naming tip:** keep the ontology *domain-scoped* (`BankingIQ_Customer`, not `BankingIQ_All`). In Lab 2 you'll add ontologies for Products and Sales & Engagement and link them with cross-ontology relationships.

## 2.2 Tour the Ontology canvas

When the ontology opens you'll see four areas:

| Pane | Purpose |
|---|---|
| **Canvas** (center) | Visual graph of entities & relationships |
| **Left rail** | Entities, properties, relationships, business domains |
| **Right rail** | Properties of the selected node |
| **Top bar** | Save · Publish · Validate |

`[screenshot: Empty ontology canvas with the four UI areas highlighted]`

## 2.3 Add the *Customer* Business Domain

1. In the left rail, expand **Business domains** → click **+ New domain**.
2. **Name:** `Customer`
3. **Display name:** `ลูกค้า / Customer`
4. **Description:**
   > Master domain describing who the customer is — identity, demographics, segment, KYC and contact channels.
5. Click **Save**.

`[screenshot: Business domain side panel with Customer details]`

## 2.4 Save & version

Click **Save** in the top bar. Fabric IQ creates an initial version of the ontology so you can return to this baseline later.

## 2.5 What just happened

You now have:
- An **Ontology** item visible in your workspace
- An empty **Customer** Business Domain inside it
- Permission boundaries (workspace roles) automatically applied

There are still **no entities** — that's [Step 3](step-03-define-entities-properties.md).

## Common gotchas

- ❌ **Ontology not in the New item picker** → your capacity may not have Fabric IQ enabled. Ask your admin to enable it for the workspace's capacity.
- ❌ **Cannot save** → you may have only Viewer rights. You need at least Contributor on the workspace.
- ⚠️ **Two ontologies with the same name** → allowed but confusing; rename one.
