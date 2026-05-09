# Step 4 — Bind entities to Lakehouse tables

**Goal:** Wire each entity to its physical Delta table in `BankingIQ_LH` so the ontology can preview live data.

## 4.1 The binding model

A **binding** in Fabric IQ has three parts:

1. **Source** — a Lakehouse / Warehouse / Eventhouse / Semantic Model
2. **Object** — the table or view (e.g., `customers`)
3. **Property mapping** — entity property → physical column (1-to-1)

You'll repeat the same flow 5 times.

## 4.2 Bind `Customer` → `customers`

1. Open the **Customer** entity in the canvas.
2. In the right rail, click **Data binding → + Add binding**.
3. **Source type:** Lakehouse → pick **`BankingIQ_LH`**.
4. **Table:** `customers`.
5. Map properties:

| Entity property | Lakehouse column |
|---|---|
| `customerId` | `customer_id` |
| `nationalId` | `national_id` |
| `fullName` | `full_name` |
| `gender` | `gender` |
| `dateOfBirth` | `date_of_birth` |
| `maritalStatus` | `marital_status` |
| `occupation` | `occupation` |
| `monthlyIncomeThb` | `monthly_income_thb` |
| `preferredLanguage` | `preferred_language` |
| `onboardingDate` | `onboarding_date` |
| `isActive` | `is_active` |

6. Click **Preview data** → you should see Thai names + THB incomes.

`[screenshot: Binding panel with Customer mapping + data preview rows]`

## 4.3 Bind the remaining 4 entities

Repeat for each:

| Entity | Lakehouse table | Notes |
|---|---|---|
| `Address` | `customer_addresses` | Map `addressId←address_id`, `customerId←customer_id`, `addressType←address_type`, `addressLine1←address_line1`, `postalCode←postal_code`, `isPrimary←is_primary`, others are 1:1 by name |
| `CustomerSegment` | `customer_segments` | `segmentId←segment_id`, `segmentName←segment_name`, `description←description` |
| `KycRecord` | `kyc_records` | `kycId←kyc_id`, `kycTier←kyc_tier`, `riskRating←risk_rating`, `pepFlag←pep_flag`, `lastReview←last_review`, `nextReview←next_review` |
| `CustomerContact` | `customer_contacts` | `contactId←contact_id`, `isPrimary←is_primary` |

> **Note about `customer_segment_history`:** that table is a *history* table — bind it later (Lab 2 advanced) as a separate entity if you need temporal segment data. For now, derive a customer's segment via the relationship in Step 5 using the latest record.

`[screenshot: Canvas showing all 5 entities each with a "bound" indicator]`

## 4.4 Validate column types

Fabric IQ flags type mismatches (e.g., string ↔ date). Common fixes for our CSV-loaded tables:

- `dateOfBirth` / `onboardingDate` come in as `STRING` from CSV. Either:
  - **Recommended:** create a Lakehouse view that casts them to `DATE` and bind to the view.
  - **Alternate:** change the entity property to `String` (loses type semantics — avoid).

A view (run in the Lakehouse SQL endpoint):

```sql
CREATE OR ALTER VIEW v_customers AS
SELECT
    customer_id, national_id, first_name, last_name, full_name,
    gender, CAST(date_of_birth AS DATE) AS date_of_birth,
    marital_status, occupation, monthly_income_thb,
    preferred_language, CAST(onboarding_date AS DATE) AS onboarding_date,
    is_active
FROM customers;
```

Then re-bind `Customer` to `v_customers`.

## 4.5 Test queries via the ontology preview

Right-click the `Customer` entity → **Preview data** → filter:
- `monthlyIncomeThb > 200000` → expect Affluent customers
- `province = 'กรุงเทพมหานคร'` (after binding `Address`)

`[screenshot: Preview pane showing filtered Bangkok customers]`

## 4.6 Done

All 5 entities are now **bound** and previewable. Add the **relationships** in [Step 5](step-05-create-relationships.md).
