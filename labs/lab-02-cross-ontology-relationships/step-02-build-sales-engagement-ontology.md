# Step 2 — Build the Sales & Engagement ontology

**Goal:** Create `BankingIQ_SalesEngagement` with 8 entities covering branches, employees, marketing, service and lead flow.

## 2.1 Create the ontology

1. **+ New item → Ontology**
2. Name: **`BankingIQ_SalesEngagement`**
3. Business Domain: **`SalesEngagement`** with description:
   > Channels and touchpoints — physical (Branch), human (Employee), marketing (Campaign + Response), service (Ticket + Interaction), and pipeline (Lead + Opportunity).

## 2.2 Entities and key properties

### `Branch`
| Property | Type |
|---|---|
| `branchId` | String, ✅ |
| `branchName` | String |
| `branchType` | String |
| `province` | String |
| `district` | String |
| `latitude` | Decimal |
| `longitude` | Decimal |
| `isActive` | Boolean |

Bind to **`branches`**.

### `Employee`
| Property | Type |
|---|---|
| `employeeId` | String, ✅ |
| `fullName` | String, PII |
| `role` | String |
| `branchId` | String |
| `email` | String, PII |
| `isActive` | Boolean |

Bind to **`employees`**.

### `MarketingCampaign`
| Property | Type |
|---|---|
| `campaignId` | String, ✅ |
| `campaignName` | String |
| `objective` | String |
| `channel` | String |
| `targetProductId` | String | Cross-domain → Product |
| `targetSegmentId` | String | Cross-domain → CustomerSegment |
| `startDate` | Date |
| `endDate` | Date |
| `budgetThb` | Decimal |
| `status` | String |

Bind to **`marketing_campaigns`**.

### `CampaignResponse`
| Property | Type |
|---|---|
| `responseId` | String, ✅ |
| `campaignId` | String |
| `customerId` | String | Cross-domain → Customer |
| `responseDate` | Date |
| `channel` | String |
| `outcome` | String |
| `converted` | Boolean |
| `conversionValueThb` | Decimal |

Bind to **`campaign_responses`**.

### `SupportTicket`
| Property | Type |
|---|---|
| `ticketId` | String, ✅ |
| `customerId` | String | Cross-domain → Customer |
| `assignedEmployeeId` | String |
| `category` | String |
| `channel` | String |
| `priority` | String |
| `status` | String |
| `openedAt` | DateTime |
| `closedAt` | DateTime |
| `csatScore` | Integer |

Bind to **`support_tickets`**.

### `ServiceInteraction`
| Property | Type |
|---|---|
| `interactionId` | String, ✅ |
| `customerId` | String | Cross-domain → Customer |
| `employeeId` | String |
| `branchId` | String |
| `channel` | String |
| `interactionType` | String |
| `interactionAt` | DateTime |
| `durationSeconds` | Integer |

Bind to **`service_interactions`**.

### `Lead`
| Property | Type |
|---|---|
| `leadId` | String, ✅ |
| `leadSource` | String |
| `customerId` | String | Cross-domain → Customer (nullable for cold leads) |
| `leadFullName` | String, PII |
| `phone` | String, PII |
| `email` | String, PII |
| `interestedProductId` | String | Cross-domain → Product |
| `ownerEmployeeId` | String |
| `status` | String |
| `score` | Integer |

Bind to **`leads`**.

### `SalesOpportunity`
| Property | Type |
|---|---|
| `opportunityId` | String, ✅ |
| `leadId` | String |
| `stage` | String |
| `expectedValueThb` | Decimal |
| `probabilityPct` | Integer |
| `expectedCloseDate` | Date |

Bind to **`sales_opportunities`**.

`[screenshot: SalesEngagement canvas with 8 entities bound]`

## 2.3 Intra-SalesEngagement relationships

| Name | From | To | Cardinality |
|---|---|---|---|
| `worksAt` | `Employee` | `Branch` | many-to-one |
| `assignedTo` | `SupportTicket` | `Employee` | many-to-one |
| `ofCampaign` | `CampaignResponse` | `MarketingCampaign` | many-to-one |
| `atBranch` | `ServiceInteraction` | `Branch` | many-to-one (nullable) |
| `handledBy` | `ServiceInteraction` | `Employee` | many-to-one (nullable) |
| `ownedBy` | `Lead` | `Employee` | many-to-one |
| `generatedFrom` | `SalesOpportunity` | `Lead` | many-to-one |

`[screenshot: SalesEngagement canvas with relationships drawn]`

Save & publish, then continue to [Step 3](step-03-cross-ontology-relationships.md).
