# Step 1 — Build the Products ontology

**Goal:** Create `BankingIQ_Products` with 7 entities bound to the Lakehouse.

## 1.1 Create the ontology

1. **+ New item → Ontology**
2. Name: **`BankingIQ_Products`**
3. Add a Business Domain named **`Products`** with description:
   > Banking products and the customer holdings against them — accounts, cards, loans, fixed deposits and investments. All amounts in THB.

`[screenshot: New Products ontology canvas]`

## 1.2 Entities & key properties

For each entity below, repeat the create-entity → add-properties → bind flow from Lab 1.

### `Product`
| Property | Type | Notes |
|---|---|---|
| `productId` | String, ✅ identifier | e.g., `PRD-CC02` |
| `categoryId` | String | FK to `ProductCategory` |
| `productNameTh` | String | Thai name |
| `productNameEn` | String | English name |
| `currency` | String | `THB` |
| `isActive` | Boolean | |

Bind to **`products`** table.

### `ProductCategory`
| Property | Type | Notes |
|---|---|---|
| `categoryId` | String, ✅ | e.g., `PC-CRD` |
| `categoryName` | String | Deposit/Loan/Card/Wealth/Insurance/Digital |
| `description` | String | Thai description |

Bind to **`product_categories`**.

### `Account`
| Property | Type | Notes |
|---|---|---|
| `accountId` | String, ✅ | |
| `accountNumber` | String, sensitive | |
| `primaryCustomerId` | String | Cross-domain FK → Customer |
| `productId` | String | FK → Product |
| `branchId` | String | Cross-domain FK → Branch |
| `openDate` | Date | |
| `currentBalanceThb` | Decimal | |
| `availableBalanceThb` | Decimal | |
| `status` | String | Active/Dormant/Closed |

Bind to **`accounts`**.

### `Card`
| Property | Type | Notes |
|---|---|---|
| `cardId` | String, ✅ | |
| `cardNumberMasked` | String, sensitive | |
| `customerId` | String | Cross-domain FK → Customer |
| `productId` | String | FK → Product |
| `linkedAccountId` | String | Optional FK → Account |
| `cardType` | String | Credit/Debit |
| `creditLimitThb` | Decimal | |
| `currentOutstandingThb` | Decimal | |
| `status` | String | |

Bind to **`cards`**.

### `Loan`
| Property | Type | Notes |
|---|---|---|
| `loanId` | String, ✅ | |
| `customerId` | String | Cross-domain FK |
| `productId` | String | FK → Product |
| `branchId` | String | Cross-domain FK |
| `principalThb` | Decimal | |
| `interestRatePct` | Decimal | |
| `termMonths` | Integer | |
| `outstandingBalanceThb` | Decimal | |
| `status` | String | Current/Late/Default/Closed |

Bind to **`loans`**. (Optionally also create `LoanInstallment` bound to `loan_repayment_schedule`.)

### `FixedDeposit`
| Property | Type |
|---|---|
| `fdId` | String, ✅ |
| `customerId` | String |
| `productId` | String |
| `branchId` | String |
| `principalThb` | Decimal |
| `interestRatePct` | Decimal |
| `termMonths` | Integer |
| `maturityDate` | Date |
| `autoRollover` | Boolean |
| `status` | String |

Bind to **`fixed_deposits`**.

### `InvestmentHolding`
| Property | Type |
|---|---|
| `holdingId` | String, ✅ |
| `customerId` | String |
| `productId` | String |
| `unitsHeld` | Decimal |
| `marketValueThb` | Decimal |

Bind to **`investment_holdings`**.

`[screenshot: Products ontology canvas with 7 entities]`

## 1.3 Intra-Products relationships

Add inside this ontology only:

| Name | From | To | Cardinality |
|---|---|---|---|
| `inCategory` | `Product` | `ProductCategory` | many-to-one |
| `ofProduct` | `Account` | `Product` | many-to-one |
| `ofProduct` | `Card` | `Product` | many-to-one |
| `ofProduct` | `Loan` | `Product` | many-to-one |
| `ofProduct` | `FixedDeposit` | `Product` | many-to-one |
| `ofProduct` | `InvestmentHolding` | `Product` | many-to-one |
| `linkedTo` | `Card` | `Account` | many-to-one (debit only) |

## 1.4 Validate, save, publish

`[screenshot: Validation result — 7 entities, 7 relationships, 0 errors]`

Move on to [Step 2](step-02-build-sales-engagement-ontology.md).
