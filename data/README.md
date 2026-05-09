# Data — FabricIQ-L300

All datasets in this repo are **synthetic** and tailored to a Thai retail-banking scenario.
Currency is **THB** (฿). Names and addresses are Thai. Branches are Bangkok-centric (with selected upcountry locations).

## Layout

```
data/
├── README.md                  ← this file
├── batch/                     ← CSV outputs (git-ignored)
├── generators/
│   ├── requirements.txt
│   ├── generate_batch_data.py        ← creates all batch CSVs
│   └── generate_streaming_sample.py  ← creates JSONL sample events
└── streaming/
    ├── card_transactions.sample.jsonl
    └── deposit_transactions.sample.jsonl
```

## Quick start

```bash
cd data/generators
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
python generate_batch_data.py            # writes CSVs into ../batch/
python generate_streaming_sample.py      # writes JSONL into ../streaming/
```

Then upload `data/batch/*.csv` to your Fabric **Lakehouse** (Files → Tables) and stream the JSONL events into your **Eventhouse** using the Fabric notebook in [`../notebooks/streaming_to_eventhouse.ipynb`](../notebooks/streaming_to_eventhouse.ipynb).

## Domains and tables

### Domain A — Customer

| Table | Approx. rows | Purpose |
|---|---:|---|
| `customers` | 10,000 | Master customer with Thai name, DOB, gender, occupation |
| `customer_addresses` | 12,000 | One+ address per customer (registered / mailing) with Thai province |
| `customer_segments` | 6 | Mass / Mass-Affluent / Affluent / Private / SME / Corporate |
| `customer_segment_history` | 10,000 | Current + historical segment assignment |
| `kyc_records` | 10,000 | KYC tier, risk rating, last review date |
| `customer_contacts` | 18,000 | Phone / email / line-id channels |

### Domain B — Products

| Table | Approx. rows | Purpose |
|---|---:|---|
| `product_categories` | 6 | Deposit, Loan, Card, Wealth, Insurance, Digital |
| `products` | 25 | Banking product catalog (e.g., *Savings Plus*, *KrungThep Platinum*) |
| `accounts` | 18,000 | Savings / Current / Salary accounts with THB balance |
| `cards` | 7,500 | Credit + Debit cards, issued against accounts/customers |
| `loans` | 4,000 | Personal / Auto / Home loans in THB |
| `loan_repayment_schedule` | 96,000 | Per-installment schedule per loan |
| `fixed_deposits` | 3,000 | Term deposits with maturity in THB |
| `investment_holdings` | 2,500 | Mutual fund / bond holdings |

### Domain C — Sales & Engagement

| Table | Approx. rows | Purpose |
|---|---:|---|
| `branches` | 50 | Bangkok-flavored branch network |
| `employees` | 500 | Relationship managers, tellers, contact-center agents |
| `marketing_campaigns` | 30 | Cross-sell / acquisition campaigns |
| `campaign_responses` | 25,000 | Customer reactions to campaigns |
| `support_tickets` | 8,000 | Service tickets with status & SLA |
| `service_interactions` | 50,000 | Branch / call / chat touchpoints |
| `leads` | 6,000 | Inbound / outbound leads with status |
| `sales_opportunities` | 3,000 | Open opportunities tied to leads |

### Streaming (Eventhouse)

| Stream | Sample file | Description |
|---|---|---|
| `card_transactions` | `streaming/card_transactions.sample.jsonl` | Authorize / capture events on cards |
| `deposit_transactions` | `streaming/deposit_transactions.sample.jsonl` | Deposit / withdraw / transfer events on accounts |

## Cross-domain keys (used in Lab 2)

| From | To | Key |
|---|---|---|
| `customers.customer_id` | `accounts.primary_customer_id` | Customer owns Account |
| `customers.customer_id` | `cards.customer_id` | Customer holds Card |
| `customers.customer_id` | `loans.customer_id` | Customer borrowed Loan |
| `customers.customer_id` | `campaign_responses.customer_id` | Customer responded to Campaign |
| `customers.customer_id` | `support_tickets.customer_id` | Customer raised Ticket |
| `branches.branch_id` | `accounts.branch_id` | Branch services Account |
| `employees.employee_id` | `support_tickets.assigned_employee_id` | Employee handles Ticket |
