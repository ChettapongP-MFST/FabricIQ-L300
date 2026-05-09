# Step 3 — Define entities and properties

**Goal:** Add 5 entities to the *Customer* business domain, each with the right typed properties and a clear business description.

## 3.1 The 5 entities

| Entity | Singular display | Plural display | Purpose |
|---|---|---|---|
| `Customer` | ลูกค้า | ลูกค้า | The customer master |
| `Address` | ที่อยู่ | ที่อยู่ | Customer addresses (Registered, Mailing) |
| `CustomerSegment` | กลุ่มลูกค้า | กลุ่มลูกค้า | Reference segment (Mass, Affluent, …) |
| `KycRecord` | ข้อมูล KYC | ข้อมูล KYC | KYC tier, risk and review dates |
| `CustomerContact` | ช่องทางติดต่อ | ช่องทางติดต่อ | Phone / Email / LINE |

For each, in the left rail click **Entities → + New entity**, fill the panel, and **Save**.

`[screenshot: New entity panel with name and display names filled]`

## 3.2 Property cheatsheet

Use this table when adding properties. Always include:
- **Business name** (camelCase, used by agents)
- **Display name** (Thai+English friendly)
- **Data type**
- **Description** (a sentence the agent can ground on)
- **Identifier** flag for the primary key
- **PII / Sensitive** flag where relevant

### Customer

| Property | Type | Identifier | Sensitive | Description |
|---|---|---|---|---|
| `customerId` | String | ✅ | | Unique customer id (e.g., `CUS0000001`). |
| `nationalId` | String | | ✅ PII | Thai national ID (13-digit). |
| `fullName` | String | | ✅ PII | Full Thai name. |
| `gender` | String | | | `M` / `F`. |
| `dateOfBirth` | Date | | ✅ PII | Date of birth. |
| `maritalStatus` | String | | | Single / Married / Divorced / Widowed. |
| `occupation` | String | | | Self-declared occupation (Thai). |
| `monthlyIncomeThb` | Decimal | | ✅ Sensitive | Monthly income in THB. |
| `preferredLanguage` | String | | | `TH` / `EN`. |
| `onboardingDate` | Date | | | Date the customer was onboarded. |
| `isActive` | Boolean | | | Active flag. |

### Address

| Property | Type | Identifier | Description |
|---|---|---|---|
| `addressId` | String | ✅ | Unique address id. |
| `customerId` | String | | FK to Customer. |
| `addressType` | String | | `Registered` / `Mailing`. |
| `addressLine1` | String | | Street address (Thai). |
| `district` | String | | Amphoe / Khet. |
| `province` | String | | Thai province (e.g., `กรุงเทพมหานคร`). |
| `postalCode` | String | | 5-digit postal code. |
| `country` | String | | ISO-2; always `TH` here. |
| `isPrimary` | Boolean | | Primary address flag. |

### CustomerSegment

| Property | Type | Identifier | Description |
|---|---|---|---|
| `segmentId` | String | ✅ | e.g., `SEG-MAFF`. |
| `segmentName` | String | | Mass / Mass-Affluent / Affluent / Private / SME / Corporate. |
| `description` | String | | Short Thai description. |

### KycRecord

| Property | Type | Identifier | Description |
|---|---|---|---|
| `kycId` | String | ✅ | Unique KYC record id. |
| `customerId` | String | | FK to Customer. |
| `kycTier` | String | | `Tier1` / `Tier2` / `Tier3`. |
| `riskRating` | String | | `Low` / `Medium` / `High`. |
| `pepFlag` | Boolean | | Politically Exposed Person flag. |
| `lastReview` | Date | | Last KYC review date. |
| `nextReview` | Date | | Next required review date. |
| `status` | String | | `Approved` / `Pending` / `Rejected`. |

### CustomerContact

| Property | Type | Identifier | Sensitive | Description |
|---|---|---|---|---|
| `contactId` | String | ✅ | | Unique contact-channel id. |
| `customerId` | String | | | FK to Customer. |
| `channel` | String | | | `Phone` / `Email` / `LINE`. |
| `value` | String | | ✅ PII | Channel value (number, email, line-id). |
| `isPrimary` | Boolean | | | Primary channel flag. |
| `verified` | Boolean | | | Channel-verified flag. |

`[screenshot: Customer entity expanded showing property list]`

## 3.3 Add good descriptions

Descriptions are what AI agents read. Bad: *"customer name"*. Good:

> The customer's full Thai legal name as captured during onboarding KYC. Use this when the user asks for a customer "by name" — match against this property in case-insensitive Thai.

Spend the most time on the **Customer** entity descriptions; Lab 3's Data Agent quality depends on them.

## 3.4 Save and validate

Click **Validate** in the top bar — it should report 0 errors. Each entity should show its properties in the right rail when selected.

`[screenshot: Validation panel showing 0 errors, 5 entities, 0 relationships]`

Move on to [Step 4 — Bind to Lakehouse](step-04-bind-to-lakehouse.md).
