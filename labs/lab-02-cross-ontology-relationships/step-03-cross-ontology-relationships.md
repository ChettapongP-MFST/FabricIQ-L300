# Step 3 — Cross-ontology relationships

**Goal:** Connect the three ontologies (`BankingIQ_Customer`, `BankingIQ_Products`, `BankingIQ_SalesEngagement`) so an agent can answer questions that span domains — without anyone hand-coding joins.

## 3.1 What is a cross-ontology relationship?

A **cross-ontology relationship** is a relationship whose source and target entities live in **different ontology items**. Fabric IQ resolves the join at query time using the bound physical keys.

You define them in the ontology that *owns* the relationship semantically. For us:

- **Ownership** entities (Customer holds Card, Customer raised Ticket) → defined in `BankingIQ_Customer` (or in the *child* ontology, depending on tenant policy).
- **Reference** relationships (Account servicedBy Branch) → defined wherever the FK lives.

Both directions work; pick the one that's easier to discover for agents.

## 3.2 Cross-relationships to add

### From `BankingIQ_Customer`

In the Customer ontology canvas, add **External entity references** (right rail → **+ External entity**) to:
- `Account`, `Card`, `Loan`, `FixedDeposit`, `InvestmentHolding` (from `BankingIQ_Products`)
- `CampaignResponse`, `SupportTicket`, `ServiceInteraction`, `Lead` (from `BankingIQ_SalesEngagement`)

Then add the relationships:

| Name | From | To (external) | Cardinality | Join |
|---|---|---|---|---|
| `owns` | Customer | Products.`Account` | one-to-many | `customers.customer_id = accounts.primary_customer_id` |
| `holdsCard` | Customer | Products.`Card` | one-to-many | `customers.customer_id = cards.customer_id` |
| `borrowed` | Customer | Products.`Loan` | one-to-many | `customers.customer_id = loans.customer_id` |
| `holdsFd` | Customer | Products.`FixedDeposit` | one-to-many | `customers.customer_id = fixed_deposits.customer_id` |
| `holdsInvestment` | Customer | Products.`InvestmentHolding` | one-to-many | `customers.customer_id = investment_holdings.customer_id` |
| `respondedTo` | Customer | SE.`CampaignResponse` | one-to-many | `customers.customer_id = campaign_responses.customer_id` |
| `raised` | Customer | SE.`SupportTicket` | one-to-many | `customers.customer_id = support_tickets.customer_id` |
| `engagedIn` | Customer | SE.`ServiceInteraction` | one-to-many | `customers.customer_id = service_interactions.customer_id` |
| `linkedToLead` | Customer | SE.`Lead` | one-to-many (nullable) | `customers.customer_id = leads.customer_id` |

`[screenshot: Customer ontology canvas with external references and 9 cross-domain edges]`

### From `BankingIQ_Products`

| Name | From | To (external) | Cardinality | Join |
|---|---|---|---|---|
| `servicedBy` | Account | SE.`Branch` | many-to-one | `accounts.branch_id = branches.branch_id` |
| `originatedAt` | Loan | SE.`Branch` | many-to-one | `loans.branch_id = branches.branch_id` |

### From `BankingIQ_SalesEngagement`

| Name | From | To (external) | Cardinality | Join |
|---|---|---|---|---|
| `targetsProduct` | MarketingCampaign | Products.`Product` | many-to-one | `marketing_campaigns.target_product_id = products.product_id` |
| `targetsSegment` | MarketingCampaign | Customer.`CustomerSegment` | many-to-one | `marketing_campaigns.target_segment_id = customer_segments.segment_id` |
| `interestedIn` | Lead | Products.`Product` | many-to-one | `leads.interested_product_id = products.product_id` |

## 3.3 Add high-value descriptions

Cross-ontology descriptions are extra important — agents use them to *choose* between paths. Examples:

> **`Customer.holdsCard → Card`** — Cards (credit or debit) issued in the customer's name. Use this when the user asks about *cards*, *credit limit*, *outstanding card balance*, or *card transactions* (the latter joins to streaming `CardTransactions` via `card_id`).

> **`Customer.respondedTo → CampaignResponse`** — Customer reactions to marketing campaigns. Filter on `outcome = 'Converted'` for revenue contribution; on `outcome IN ('Interested','No Response')` to find untapped warm leads.

## 3.4 Validate the graph

Open each ontology and click **Validate**. Each should report:

| Ontology | Entities | Internal rels | External rels | Errors |
|---|---:|---:|---:|---:|
| `BankingIQ_Customer` | 5 | 4 | 9 | 0 |
| `BankingIQ_Products` | 7 | 7 | 2 | 0 |
| `BankingIQ_SalesEngagement` | 8 | 7 | 3 | 0 |

`[screenshot: Each ontology's validation summary]`

## 3.5 Try a multi-hop business question

In the Copilot pane on `BankingIQ_Customer`, ask:

> *Show me Mass-Affluent customers in Bangkok who responded to a Credit Card campaign in the last 90 days but don't currently hold any credit card.*

Fabric IQ should resolve:
- `Customer → inSegment → Mass-Affluent`
- `Customer → hasAddress → Address(province='กรุงเทพมหานคร')`
- `Customer → respondedTo → CampaignResponse → ofCampaign → MarketingCampaign → targetsProduct → Product(category='Card')`
- *NOT EXISTS* `Customer → holdsCard → Card(cardType='Credit', status='Active')`

`[screenshot: Multi-hop answer with rows]`

If you see a coherent list of customers, **the cross-ontology graph is working**. This is exactly what the Data Agent in Lab 3 will reason over.

## 🎉 Lab 2 complete

You now have a **3-ontology, multi-domain semantic graph** wired across the entire Thai retail-banking dataset. Continue to [Lab 3 — Data Agent grounded on these ontologies](../lab-03-data-agent-with-ontology/README.md).
