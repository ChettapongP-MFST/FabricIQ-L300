# Workshop Prerequisites

This document is what attendees should set up **before** showing up to the FabricIQ-L300 workshop.

## 1. Microsoft Fabric

- A **Fabric capacity** that has Fabric IQ enabled. Either:
  - **F-SKU (F2 or higher)** — recommended for shared use.
  - **Fabric Trial** — fine for a self-paced learner; expect occasional throttling.
- A dedicated **Workspace** assigned to that capacity. Suggested name: `FabricIQ-L300-<your-handle>`.
- Workspace role on yourself: at least **Member** (or **Admin** if you want to manage roles for others).

## 2. Identity & permissions

- **Microsoft Entra ID** account in your tenant.
- Permission to create:
  - Lakehouse, Eventhouse (KQL DB)
  - Ontology, Data Agent (Fabric IQ items)
- (Lab 3 only) **Microsoft Teams** access in the same tenant; ability to install custom apps. If your tenant blocks custom app side-loading, talk to an admin.
- (Lab 3 optional) **Microsoft 365 Copilot** + **Copilot Studio** licenses.

## 3. Local machine

| Tool | Version | Purpose |
|---|---|---|
| Python | ≥ 3.10 | Run the data generator |
| `pip` | recent | Install Faker / pandas |
| Git | any | Clone this repo |
| Browser | Edge / Chrome | Use the Fabric portal |

```bash
git clone https://github.com/ChettapongP-MFST/FabricIQ-L300.git
cd FabricIQ-L300/data/generators
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
python generate_batch_data.py
```

You should end up with ~20 CSVs under `data/batch/` ready to upload to a Lakehouse.

## 4. Data prep before Lab 1

- Lakehouse name: **`BankingIQ_LH`**.
- All 20 CSVs uploaded and converted to Delta tables (Lab 1 Step 1 covers this in detail).

## 5. (Lab 4 future) Streaming prerequisites

- **Eventhouse (KQL DB)** in the same workspace, named **`FabricIQ_L300`**.
- The user / SPN running the streaming notebook needs **Database Ingestor** + **Database Viewer** roles on that KQL DB.
- Outbound network access from your Spark / Python session to the Eventhouse cluster URI.

## 6. Knowledge prerequisites

You should be comfortable with:
- Basic SQL / pandas
- Lakehouse vs Warehouse vs KQL DB conceptually (we recap in [docs/01-what-is-microsoft-fabric.md](../docs/01-what-is-microsoft-fabric.md))
- Star-schema or relational modeling at a glance

If you've completed the level-200 [`FabricIQ`](https://github.com/ChettapongP-MFST/FabricIQ) repo, you're well-positioned.

## 7. Troubleshooting cheat sheet

| Symptom | Likely cause | Fix |
|---|---|---|
| "Ontology" not in **+ New item** | Capacity has no Fabric IQ | Ask admin to enable on the capacity |
| Cannot save the ontology | Workspace Viewer role | Ask for Contributor / Member |
| Data Agent test answers "I don't have data" | Ontology not published | Re-publish; re-attach to the agent |
| Teams publish blocked | Tenant blocks custom apps | Get tenant admin approval; or stay in Fabric portal |
| KQL ingestion 401 | Missing Database Ingestor role | Grant role in the Eventhouse permissions panel |
