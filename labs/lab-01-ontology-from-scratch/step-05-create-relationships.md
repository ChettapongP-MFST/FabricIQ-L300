# Step 5 — Create intra-domain relationships

**Goal:** Add typed relationships between the 5 entities so AI agents and Copilot can traverse the Customer domain naturally.

## 5.1 Relationships to add

| Name | From | To | Cardinality | Foreign key |
|---|---|---|---|---|
| `hasAddress` | `Customer` | `Address` | one-to-many | `Address.customerId → Customer.customerId` |
| `hasContact` | `Customer` | `CustomerContact` | one-to-many | `CustomerContact.customerId → Customer.customerId` |
| `hasKyc` | `Customer` | `KycRecord` | one-to-many (logical 1:1 current) | `KycRecord.customerId → Customer.customerId` |
| `inSegment` | `Customer` | `CustomerSegment` | many-to-one | via `customer_segment_history.segment_id` (latest) |

## 5.2 Add `hasAddress`

1. In the canvas, hover the **`Customer`** entity → drag the relationship handle to **`Address`**.
2. In the right rail:
   - **Name:** `hasAddress`
   - **Display name:** `มีที่อยู่`
   - **Cardinality:** One-to-many
   - **Description:** *A customer may have one or more addresses (registered, mailing).*
3. **Join keys:** `Customer.customerId = Address.customerId`.
4. Save.

`[screenshot: Relationship panel for hasAddress]`

## 5.3 Add `hasContact` and `hasKyc`

Repeat the same flow:

- `hasContact` — `Customer.customerId = CustomerContact.customerId`, one-to-many.
- `hasKyc` — `Customer.customerId = KycRecord.customerId`, one-to-many (most customers have one current KYC record).

## 5.4 Add `inSegment` (via the history table)

The current segment is the row in `customer_segment_history` where `is_current = true`. Two ways:

**Option A — bind a "current segment" view** (recommended):

Create a Lakehouse view:
```sql
CREATE OR ALTER VIEW v_customer_current_segment AS
SELECT customer_id, segment_id
FROM customer_segment_history
WHERE is_current = TRUE;
```

Then in the ontology, add a relationship:
- **From:** `Customer`
- **To:** `CustomerSegment`
- **Name:** `inSegment`
- **Cardinality:** Many-to-one
- **Join:** `Customer.customerId = v_customer_current_segment.customer_id` AND `v_customer_current_segment.segment_id = CustomerSegment.segmentId`

If your tenant supports **bridge tables** in relationships, model `v_customer_current_segment` as the bridge. Otherwise, expose `currentSegmentId` as a derived property on `Customer`.

**Option B — derived property** (simpler but less explicit):

Expose `currentSegmentId` on `Customer` (bind it to a view that joins the history) and create a direct relationship `Customer.currentSegmentId → CustomerSegment.segmentId`.

`[screenshot: Final canvas showing the 4 relationships]`

## 5.5 Add good relationship descriptions

For each relationship, write 1–2 sentences. Example for `inSegment`:

> Each customer belongs to exactly one *current* segment (Mass, Mass-Affluent, Affluent, Private, SME, Corporate) at a point in time. Historical segment changes live in `customer_segment_history`.

Agents in Lab 3 use these descriptions to pick the right path when answering questions.

## 5.6 Validate, save, publish

1. Click **Validate** — should be 0 errors, 5 entities, 4 relationships.
2. Click **Save**.
3. Click **Publish** to make this version available to other Fabric IQ items (Data Agent in Lab 3).

`[screenshot: Publish dialog confirming version 1.0]`

## 5.7 Try a sanity question

In the **Ontology Explorer** (or the Copilot pane on the ontology), ask:

> *List 5 Mass-Affluent customers in Bangkok with a primary phone number.*

Fabric IQ should resolve the path:
`Customer → inSegment → CustomerSegment(Mass-Affluent)`
`Customer → hasAddress → Address(province='กรุงเทพมหานคร', isPrimary=true)`
`Customer → hasContact → CustomerContact(channel='Phone', isPrimary=true)`

If you get coherent results, your ontology is healthy.

`[screenshot: Sample Q&A in the ontology Copilot pane]`

## 🎉 Lab 1 complete

You've built a **fully bound, validated, published** Customer ontology. Next: [Lab 2 — Cross-Ontology Relationships](../lab-02-cross-ontology-relationships/README.md) where you'll add Products & Sales-and-Engagement and link them to Customer.
