# Step 1 — Set up the Lakehouse and load Domain A data

**Goal:** Create a Lakehouse named `BankingIQ_LH` and load the six Customer-domain CSVs into Delta tables.

## 1.1 Locate the data

The mock CSVs are already in this repo under [`data/batch/`](../../data/batch/). For Domain A you'll use:

| File | Purpose |
|---|---|
| `customers.csv` | Master customer (10,000 rows) |
| `customer_addresses.csv` | One+ addresses per customer |
| `customer_segments.csv` | 6 reference segments |
| `customer_segment_history.csv` | Current segment per customer |
| `kyc_records.csv` | KYC tier & risk |
| `customer_contacts.csv` | Phone / email / LINE channels |

## 1.2 Create the Lakehouse

1. In your Fabric workspace, click **+ New item → Lakehouse**.
2. Name it **`BankingIQ_LH`** and click **Create**.

`[screenshot: Fabric "New item" dialog with Lakehouse selected]`

## 1.3 Upload the CSVs to Files

1. In the Lakehouse explorer, right-click **Files → Upload → Upload folder** (or upload files individually).
2. Select all six CSVs from `data/batch/`.
3. Wait for upload to finish.

`[screenshot: Files folder showing 6 uploaded CSVs]`

## 1.4 Convert each CSV to a Delta table

For each file, right-click → **Load to tables → New table**, then accept defaults.

| Source CSV | Target table |
|---|---|
| `customers.csv` | `customers` |
| `customer_addresses.csv` | `customer_addresses` |
| `customer_segments.csv` | `customer_segments` |
| `customer_segment_history.csv` | `customer_segment_history` |
| `kyc_records.csv` | `kyc_records` |
| `customer_contacts.csv` | `customer_contacts` |

> **Tip:** If your tenant uses Schema-enabled Lakehouses, place all six tables under a schema named **`bank`** for cleaner cross-lab references.

`[screenshot: Lakehouse Tables view with 6 tables]`

## 1.5 Smoke test in the SQL endpoint

Open the **SQL analytics endpoint** of `BankingIQ_LH` and run:

```sql
SELECT COUNT(*) AS customer_count FROM customers;
SELECT TOP 5 customer_id, full_name, occupation, monthly_income_thb FROM customers;
```

You should see ~10,000 rows and Thai names like `สมชาย ใจดี`.

`[screenshot: SQL endpoint results showing Thai names]`

## 1.6 Done

You now have the **physical layer** ready. Next, [Step 2 — Create the Ontology](step-02-create-ontology.md) defines the **semantic layer** on top of it.
