"""
generate_batch_data.py
======================
Generate synthetic Thai retail-banking data for the FabricIQ-L300 labs.

Outputs CSV files into ../batch/ covering 3 business domains:
  A — Customer
  B — Products
  C — Sales & Engagement

All amounts are in THB. Names and addresses are Thai-localized.

Run:
    pip install -r requirements.txt
    python generate_batch_data.py
"""

from __future__ import annotations

import os
import random
from datetime import datetime, timedelta
from pathlib import Path

import pandas as pd
from faker import Faker

# ---------------------------------------------------------------------------
# Config
# ---------------------------------------------------------------------------

SEED = 4242
random.seed(SEED)

fake_th = Faker("th_TH")
fake_th.seed_instance(SEED)
fake_en = Faker("en_US")
fake_en.seed_instance(SEED)

OUTPUT_DIR = Path(__file__).resolve().parent.parent / "batch"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

N_CUSTOMERS = 10_000
N_ACCOUNTS = 18_000
N_CARDS = 7_500
N_LOANS = 4_000
N_FIXED_DEPOSITS = 3_000
N_INVESTMENTS = 2_500
N_BRANCHES = 50
N_EMPLOYEES = 500
N_CAMPAIGNS = 30
N_CAMPAIGN_RESP = 25_000
N_TICKETS = 8_000
N_INTERACTIONS = 50_000
N_LEADS = 6_000
N_OPPORTUNITIES = 3_000

TODAY = datetime(2026, 5, 1)

# ---------------------------------------------------------------------------
# Reference data — Thailand-flavored
# ---------------------------------------------------------------------------

THAI_PROVINCES = [
    "กรุงเทพมหานคร", "นนทบุรี", "ปทุมธานี", "สมุทรปราการ", "สมุทรสาคร",
    "เชียงใหม่", "เชียงราย", "ขอนแก่น", "นครราชสีมา", "อุดรธานี",
    "ชลบุรี", "ระยอง", "ภูเก็ต", "สงขลา", "สุราษฎร์ธานี",
    "นครปฐม", "พระนครศรีอยุธยา", "ลำปาง", "พิษณุโลก", "อุบลราชธานี",
]

BANGKOK_DISTRICTS = [
    "พระนคร", "ปทุมวัน", "บางรัก", "สาทร", "วัฒนา", "คลองเตย",
    "ห้วยขวาง", "จตุจักร", "ลาดพร้าว", "บางกะปิ", "พญาไท",
    "ดินแดง", "ราชเทวี", "ภาษีเจริญ", "ธนบุรี", "บางนา",
    "ประเวศ", "สวนหลวง", "มีนบุรี", "ดอนเมือง",
]

OCCUPATIONS_TH = [
    "พนักงานบริษัท", "ข้าราชการ", "ครู / อาจารย์", "แพทย์", "พยาบาล",
    "วิศวกร", "นักบัญชี", "พนักงานธนาคาร", "ค้าขาย / เจ้าของกิจการ",
    "ฟรีแลนซ์", "นักเรียน / นักศึกษา", "เกษตรกร", "เกษียณ",
]

GENDERS = ["M", "F"]

SEGMENTS = [
    ("SEG-MASS", "Mass", "ลูกค้าทั่วไป รายได้ปานกลาง"),
    ("SEG-MAFF", "Mass-Affluent", "รายได้ดี มีศักยภาพสูง"),
    ("SEG-AFFL", "Affluent", "ลูกค้ามั่งคั่ง"),
    ("SEG-PRIV", "Private", "ลูกค้า Private Banking"),
    ("SEG-SME",  "SME", "ผู้ประกอบการขนาดกลางและย่อม"),
    ("SEG-CORP", "Corporate", "ลูกค้านิติบุคคลขนาดใหญ่"),
]

PRODUCT_CATEGORIES = [
    ("PC-DEP", "Deposit",  "บัญชีเงินฝาก"),
    ("PC-LON", "Loan",     "สินเชื่อ"),
    ("PC-CRD", "Card",     "บัตรเครดิต/เดบิต"),
    ("PC-WLT", "Wealth",   "บริการบริหารความมั่งคั่ง"),
    ("PC-INS", "Insurance","ประกันภัย"),
    ("PC-DIG", "Digital",  "ผลิตภัณฑ์ดิจิทัล"),
]

PRODUCTS = [
    # (product_id, category_id, name_th, name_en, currency)
    ("PRD-SAV01", "PC-DEP", "บัญชีออมทรัพย์ Plus",        "Savings Plus",          "THB"),
    ("PRD-SAV02", "PC-DEP", "บัญชีออมทรัพย์ดิจิทัล",      "Digital Savings",       "THB"),
    ("PRD-CUR01", "PC-DEP", "บัญชีกระแสรายวัน",            "Current Account",       "THB"),
    ("PRD-SAL01", "PC-DEP", "บัญชีเงินเดือน",              "Salary Account",        "THB"),
    ("PRD-FD01",  "PC-DEP", "เงินฝากประจำ 6 เดือน",       "Fixed Deposit 6M",      "THB"),
    ("PRD-FD02",  "PC-DEP", "เงินฝากประจำ 12 เดือน",      "Fixed Deposit 12M",     "THB"),
    ("PRD-FD03",  "PC-DEP", "เงินฝากประจำ 24 เดือน",      "Fixed Deposit 24M",     "THB"),
    ("PRD-CC01",  "PC-CRD", "บัตรเครดิตกรุงเทพคลาสสิก",   "KrungThep Classic",     "THB"),
    ("PRD-CC02",  "PC-CRD", "บัตรเครดิตกรุงเทพแพลทินัม",  "KrungThep Platinum",    "THB"),
    ("PRD-CC03",  "PC-CRD", "บัตรเครดิตซิกเนเจอร์",       "Signature",             "THB"),
    ("PRD-CC04",  "PC-CRD", "บัตรเครดิตอินฟินิท",          "Infinite",              "THB"),
    ("PRD-DC01",  "PC-CRD", "บัตรเดบิต Be1st",            "Be1st Debit",           "THB"),
    ("PRD-DC02",  "PC-CRD", "บัตรเดบิตเวอร์ชวล",          "Virtual Debit",         "THB"),
    ("PRD-LN01",  "PC-LON", "สินเชื่อบุคคล",                "Personal Loan",         "THB"),
    ("PRD-LN02",  "PC-LON", "สินเชื่อรถยนต์",               "Auto Loan",             "THB"),
    ("PRD-LN03",  "PC-LON", "สินเชื่อบ้าน",                  "Home Loan",             "THB"),
    ("PRD-LN04",  "PC-LON", "สินเชื่อ SME",                  "SME Loan",              "THB"),
    ("PRD-WL01",  "PC-WLT", "กองทุนรวมตราสารหนี้",         "Bond Fund",             "THB"),
    ("PRD-WL02",  "PC-WLT", "กองทุนรวมตราสารทุน",          "Equity Fund",           "THB"),
    ("PRD-WL03",  "PC-WLT", "กองทุนรวม SSF",                "SSF Fund",              "THB"),
    ("PRD-WL04",  "PC-WLT", "กองทุนรวม RMF",                "RMF Fund",              "THB"),
    ("PRD-IN01",  "PC-INS", "ประกันชีวิตคุ้มครองครอบครัว", "Life Family Shield",    "THB"),
    ("PRD-IN02",  "PC-INS", "ประกันสุขภาพพรีเมียร์",        "Health Premier",        "THB"),
    ("PRD-DG01",  "PC-DIG", "กระเป๋าเงินดิจิทัล",            "Digital Wallet",        "THB"),
    ("PRD-DG02",  "PC-DIG", "QR PromptPay Plus",             "QR PromptPay Plus",     "THB"),
]

CAMPAIGN_CHANNELS = ["SMS", "Email", "LINE OA", "Mobile App", "Branch", "Outbound Call"]
CAMPAIGN_OBJECTIVES = ["Acquisition", "Cross-sell", "Up-sell", "Retention", "Reactivation"]
RESPONSE_OUTCOMES = ["Interested", "Not Interested", "No Response", "Converted", "Opted Out"]

TICKET_CATEGORIES = [
    "Card lost/stolen", "ATM dispute", "Fee inquiry", "Loan inquiry",
    "Mobile banking issue", "PromptPay issue", "Statement request",
    "Account closure", "Fraud report", "Branch service complaint",
]
TICKET_STATUSES = ["Open", "In Progress", "Resolved", "Closed", "Escalated"]
TICKET_CHANNELS = ["Branch", "Call Center", "Mobile App", "LINE OA", "Email"]
TICKET_PRIORITIES = ["Low", "Medium", "High", "Critical"]

INTERACTION_CHANNELS = ["Branch", "Call Center", "Mobile App", "Internet Banking", "LINE OA", "ATM"]
INTERACTION_TYPES = ["Inquiry", "Transaction", "Complaint", "Advisory", "Onboarding"]

LEAD_SOURCES = ["Web Form", "Branch Walk-in", "Referral", "Campaign", "Partner", "Cold Call"]
LEAD_STATUSES = ["New", "Contacted", "Qualified", "Disqualified", "Converted"]
OPP_STAGES = ["Prospecting", "Qualification", "Proposal", "Negotiation", "Closed Won", "Closed Lost"]

EMPLOYEE_ROLES = [
    "Branch Manager", "Relationship Manager", "Teller",
    "Contact Center Agent", "Wealth Advisor", "Loan Officer",
]


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def thai_phone() -> str:
    return f"0{random.choice([6,8,9])}{random.randint(10000000, 99999999)}"

def thai_id_card() -> str:
    return f"{random.randint(1, 8)}-{random.randint(1000, 9999)}-{random.randint(10000, 99999)}-{random.randint(10, 99)}-{random.randint(0, 9)}"

def random_date(start: datetime, end: datetime) -> datetime:
    delta = (end - start).days
    return start + timedelta(days=random.randint(0, max(delta, 1)),
                             hours=random.randint(0, 23),
                             minutes=random.randint(0, 59))

def to_csv(df: pd.DataFrame, name: str) -> None:
    path = OUTPUT_DIR / f"{name}.csv"
    df.to_csv(path, index=False, encoding="utf-8-sig")
    print(f"  ✓ {name:32s} {len(df):>8,} rows  →  {path.name}")


# ---------------------------------------------------------------------------
# Domain A — Customer
# ---------------------------------------------------------------------------

def gen_customer_segments() -> pd.DataFrame:
    return pd.DataFrame(
        [{"segment_id": s[0], "segment_name": s[1], "description": s[2]} for s in SEGMENTS]
    )

def gen_customers() -> pd.DataFrame:
    rows = []
    for i in range(1, N_CUSTOMERS + 1):
        gender = random.choice(GENDERS)
        if gender == "M":
            first, last = fake_th.first_name_male(), fake_th.last_name_male()
        else:
            first, last = fake_th.first_name_female(), fake_th.last_name_female()
        dob = fake_th.date_of_birth(minimum_age=20, maximum_age=75)
        rows.append({
            "customer_id":    f"CUS{i:07d}",
            "national_id":    thai_id_card(),
            "first_name":     first,
            "last_name":      last,
            "full_name":      f"{first} {last}",
            "gender":         gender,
            "date_of_birth":  dob.isoformat(),
            "marital_status": random.choice(["Single", "Married", "Divorced", "Widowed"]),
            "occupation":     random.choice(OCCUPATIONS_TH),
            "monthly_income_thb": round(random.choice([
                random.uniform(15_000, 35_000),
                random.uniform(35_000, 80_000),
                random.uniform(80_000, 200_000),
                random.uniform(200_000, 1_500_000),
            ]), 2),
            "preferred_language": random.choices(["TH", "EN"], weights=[0.9, 0.1])[0],
            "onboarding_date":    random_date(datetime(2018, 1, 1), TODAY).date().isoformat(),
            "is_active":          random.choices([True, False], weights=[0.92, 0.08])[0],
        })
    return pd.DataFrame(rows)

def gen_customer_addresses(customers: pd.DataFrame) -> pd.DataFrame:
    rows = []
    for cid in customers["customer_id"]:
        for addr_type in ["Registered"] + (["Mailing"] if random.random() < 0.2 else []):
            province = random.choices(
                THAI_PROVINCES, weights=[6] + [1] * (len(THAI_PROVINCES) - 1)
            )[0]
            district = random.choice(BANGKOK_DISTRICTS) if province == "กรุงเทพมหานคร" else fake_th.city()
            rows.append({
                "address_id":   f"ADR{len(rows)+1:07d}",
                "customer_id":  cid,
                "address_type": addr_type,
                "address_line1": fake_th.street_address(),
                "district":      district,
                "province":      province,
                "postal_code":   fake_th.postcode(),
                "country":       "TH",
                "is_primary":    addr_type == "Registered",
            })
    return pd.DataFrame(rows)

def gen_customer_segment_history(customers: pd.DataFrame) -> pd.DataFrame:
    rows = []
    for _, c in customers.iterrows():
        # weight current segment by income
        income = c["monthly_income_thb"]
        if income < 35_000:
            seg = "SEG-MASS"
        elif income < 80_000:
            seg = "SEG-MAFF"
        elif income < 200_000:
            seg = "SEG-AFFL"
        else:
            seg = random.choice(["SEG-PRIV", "SEG-CORP", "SEG-SME"])
        rows.append({
            "history_id":   f"CSH{len(rows)+1:07d}",
            "customer_id":  c["customer_id"],
            "segment_id":   seg,
            "valid_from":   c["onboarding_date"],
            "valid_to":     None,
            "is_current":   True,
        })
    return pd.DataFrame(rows)

def gen_kyc_records(customers: pd.DataFrame) -> pd.DataFrame:
    rows = []
    for cid in customers["customer_id"]:
        rows.append({
            "kyc_id":        f"KYC{len(rows)+1:07d}",
            "customer_id":   cid,
            "kyc_tier":      random.choices(["Tier1", "Tier2", "Tier3"], weights=[0.5, 0.4, 0.1])[0],
            "risk_rating":   random.choices(["Low", "Medium", "High"], weights=[0.7, 0.25, 0.05])[0],
            "pep_flag":      random.random() < 0.01,
            "last_review":   random_date(datetime(2024, 1, 1), TODAY).date().isoformat(),
            "next_review":   random_date(TODAY, datetime(2027, 12, 31)).date().isoformat(),
            "status":        random.choices(["Approved", "Pending", "Rejected"], weights=[0.95, 0.04, 0.01])[0],
        })
    return pd.DataFrame(rows)

def gen_customer_contacts(customers: pd.DataFrame) -> pd.DataFrame:
    rows = []
    for cid in customers["customer_id"]:
        # phone always
        rows.append({
            "contact_id":   f"CNT{len(rows)+1:07d}",
            "customer_id":  cid,
            "channel":      "Phone",
            "value":        thai_phone(),
            "is_primary":   True,
            "verified":     True,
        })
        # email ~80%
        if random.random() < 0.8:
            rows.append({
                "contact_id":   f"CNT{len(rows)+1:07d}",
                "customer_id":  cid,
                "channel":      "Email",
                "value":        fake_en.email(),
                "is_primary":   False,
                "verified":     random.random() < 0.9,
            })
        # LINE ~50%
        if random.random() < 0.5:
            rows.append({
                "contact_id":   f"CNT{len(rows)+1:07d}",
                "customer_id":  cid,
                "channel":      "LINE",
                "value":        f"@{fake_en.user_name()}",
                "is_primary":   False,
                "verified":     False,
            })
    return pd.DataFrame(rows)


# ---------------------------------------------------------------------------
# Domain C reference data needed early — Branches & Employees
# ---------------------------------------------------------------------------

def gen_branches() -> pd.DataFrame:
    rows = []
    for i in range(1, N_BRANCHES + 1):
        in_bkk = i <= 30
        province = "กรุงเทพมหานคร" if in_bkk else random.choice(THAI_PROVINCES[1:])
        district = random.choice(BANGKOK_DISTRICTS) if in_bkk else fake_th.city()
        rows.append({
            "branch_id":   f"BR{i:04d}",
            "branch_name": f"สาขา {district}",
            "branch_type": random.choices(["Flagship", "Standard", "Mini", "Digital"], weights=[0.1, 0.6, 0.2, 0.1])[0],
            "province":    province,
            "district":    district,
            "address":     fake_th.street_address(),
            "postal_code": fake_th.postcode(),
            "phone":       thai_phone(),
            "open_date":   random_date(datetime(1995, 1, 1), datetime(2024, 1, 1)).date().isoformat(),
            "latitude":    round(random.uniform(13.5, 14.0) if in_bkk else random.uniform(6.0, 19.0), 6),
            "longitude":   round(random.uniform(100.3, 100.9) if in_bkk else random.uniform(98.0, 105.0), 6),
            "is_active":   True,
        })
    return pd.DataFrame(rows)

def gen_employees(branches: pd.DataFrame) -> pd.DataFrame:
    rows = []
    branch_ids = branches["branch_id"].tolist()
    for i in range(1, N_EMPLOYEES + 1):
        gender = random.choice(GENDERS)
        first = fake_th.first_name_male() if gender == "M" else fake_th.first_name_female()
        last = fake_th.last_name_male() if gender == "M" else fake_th.last_name_female()
        rows.append({
            "employee_id": f"EMP{i:05d}",
            "first_name":  first,
            "last_name":   last,
            "full_name":   f"{first} {last}",
            "role":        random.choice(EMPLOYEE_ROLES),
            "branch_id":   random.choice(branch_ids),
            "email":       fake_en.email(),
            "phone":       thai_phone(),
            "hire_date":   random_date(datetime(2005, 1, 1), TODAY).date().isoformat(),
            "is_active":   random.random() < 0.95,
        })
    return pd.DataFrame(rows)


# ---------------------------------------------------------------------------
# Domain B — Products
# ---------------------------------------------------------------------------

def gen_product_categories() -> pd.DataFrame:
    return pd.DataFrame(
        [{"category_id": c[0], "category_name": c[1], "description": c[2]} for c in PRODUCT_CATEGORIES]
    )

def gen_products() -> pd.DataFrame:
    return pd.DataFrame([
        {
            "product_id":     p[0],
            "category_id":    p[1],
            "product_name_th": p[2],
            "product_name_en": p[3],
            "currency":       p[4],
            "is_active":      True,
        } for p in PRODUCTS
    ])

def gen_accounts(customers: pd.DataFrame, branches: pd.DataFrame) -> pd.DataFrame:
    cust_ids = customers["customer_id"].tolist()
    branch_ids = branches["branch_id"].tolist()
    deposit_products = [p[0] for p in PRODUCTS if p[1] == "PC-DEP" and not p[0].startswith("PRD-FD")]
    rows = []
    for i in range(1, N_ACCOUNTS + 1):
        cid = random.choice(cust_ids)
        rows.append({
            "account_id":         f"ACC{i:08d}",
            "account_number":     f"{random.randint(100, 999)}-{random.randint(0, 9)}-{random.randint(10000, 99999)}-{random.randint(0, 9)}",
            "primary_customer_id": cid,
            "product_id":         random.choice(deposit_products),
            "branch_id":          random.choice(branch_ids),
            "open_date":          random_date(datetime(2018, 1, 1), TODAY).date().isoformat(),
            "currency":           "THB",
            "current_balance_thb": round(random.choice([
                random.uniform(0, 20_000),
                random.uniform(20_000, 200_000),
                random.uniform(200_000, 2_000_000),
            ]), 2),
            "available_balance_thb": 0.0,  # filled below
            "status":             random.choices(["Active", "Dormant", "Closed"], weights=[0.9, 0.07, 0.03])[0],
        })
    df = pd.DataFrame(rows)
    df["available_balance_thb"] = (df["current_balance_thb"] * 0.98).round(2)
    return df

def gen_cards(customers: pd.DataFrame, accounts: pd.DataFrame) -> pd.DataFrame:
    cust_ids = customers["customer_id"].tolist()
    credit_products = [p[0] for p in PRODUCTS if p[0].startswith("PRD-CC")]
    debit_products = [p[0] for p in PRODUCTS if p[0].startswith("PRD-DC")]
    acct_by_cust = accounts.groupby("primary_customer_id")["account_id"].apply(list).to_dict()
    rows = []
    for i in range(1, N_CARDS + 1):
        cid = random.choice(cust_ids)
        is_credit = random.random() < 0.6
        prod = random.choice(credit_products if is_credit else debit_products)
        linked_acct = None
        if not is_credit and cid in acct_by_cust:
            linked_acct = random.choice(acct_by_cust[cid])
        rows.append({
            "card_id":          f"CRD{i:07d}",
            "card_number_masked": f"{random.choice(['4','5'])}{random.randint(100,999)}-XXXX-XXXX-{random.randint(1000,9999)}",
            "customer_id":      cid,
            "product_id":       prod,
            "linked_account_id": linked_acct,
            "card_type":        "Credit" if is_credit else "Debit",
            "issue_date":       random_date(datetime(2020, 1, 1), TODAY).date().isoformat(),
            "expiry_date":      random_date(TODAY, datetime(2030, 12, 31)).date().isoformat(),
            "credit_limit_thb": round(random.uniform(20_000, 1_500_000), 2) if is_credit else 0.0,
            "current_outstanding_thb": round(random.uniform(0, 200_000), 2) if is_credit else 0.0,
            "status":           random.choices(["Active", "Blocked", "Expired"], weights=[0.93, 0.04, 0.03])[0],
        })
    return pd.DataFrame(rows)

def gen_loans(customers: pd.DataFrame, branches: pd.DataFrame) -> pd.DataFrame:
    loan_products = [p[0] for p in PRODUCTS if p[0].startswith("PRD-LN")]
    cust_ids = customers["customer_id"].tolist()
    branch_ids = branches["branch_id"].tolist()
    rows = []
    for i in range(1, N_LOANS + 1):
        product = random.choice(loan_products)
        amount = {
            "PRD-LN01": random.uniform(50_000, 1_500_000),
            "PRD-LN02": random.uniform(300_000, 2_500_000),
            "PRD-LN03": random.uniform(1_000_000, 15_000_000),
            "PRD-LN04": random.uniform(500_000, 10_000_000),
        }[product]
        term_months = random.choice([12, 24, 36, 48, 60, 84, 120, 180, 240, 360])
        rate = round(random.uniform(3.5, 22.0), 2)
        start = random_date(datetime(2020, 1, 1), TODAY).date()
        rows.append({
            "loan_id":            f"LON{i:07d}",
            "customer_id":        random.choice(cust_ids),
            "product_id":         product,
            "branch_id":          random.choice(branch_ids),
            "principal_thb":      round(amount, 2),
            "interest_rate_pct":  rate,
            "term_months":        term_months,
            "start_date":         start.isoformat(),
            "end_date":           (start + timedelta(days=term_months * 30)).isoformat(),
            "monthly_payment_thb": round(amount * (rate / 100 / 12) /
                                         (1 - (1 + rate / 100 / 12) ** -term_months), 2),
            "outstanding_balance_thb": round(amount * random.uniform(0.1, 1.0), 2),
            "status":             random.choices(
                ["Current", "Late", "Default", "Closed"], weights=[0.78, 0.1, 0.02, 0.10])[0],
        })
    return pd.DataFrame(rows)

def gen_loan_repayment_schedule(loans: pd.DataFrame) -> pd.DataFrame:
    """Generate up to 24 schedule rows per loan to keep file size reasonable."""
    rows = []
    for _, l in loans.iterrows():
        n = min(24, l["term_months"])
        start = datetime.fromisoformat(l["start_date"])
        for k in range(1, n + 1):
            due = start + timedelta(days=30 * k)
            rows.append({
                "schedule_id":      f"LRS{len(rows)+1:08d}",
                "loan_id":          l["loan_id"],
                "installment_no":   k,
                "due_date":         due.date().isoformat(),
                "principal_due_thb": round(l["monthly_payment_thb"] * 0.7, 2),
                "interest_due_thb":  round(l["monthly_payment_thb"] * 0.3, 2),
                "total_due_thb":     round(l["monthly_payment_thb"], 2),
                "paid":              due < TODAY and random.random() < 0.95,
            })
    return pd.DataFrame(rows)

def gen_fixed_deposits(customers: pd.DataFrame, branches: pd.DataFrame) -> pd.DataFrame:
    fd_products = [p[0] for p in PRODUCTS if p[0].startswith("PRD-FD")]
    cust_ids = customers["customer_id"].tolist()
    branch_ids = branches["branch_id"].tolist()
    rows = []
    for i in range(1, N_FIXED_DEPOSITS + 1):
        product = random.choice(fd_products)
        term = {"PRD-FD01": 6, "PRD-FD02": 12, "PRD-FD03": 24}[product]
        start = random_date(datetime(2022, 1, 1), TODAY).date()
        rows.append({
            "fd_id":            f"FD{i:07d}",
            "customer_id":      random.choice(cust_ids),
            "product_id":       product,
            "branch_id":        random.choice(branch_ids),
            "principal_thb":    round(random.uniform(50_000, 5_000_000), 2),
            "interest_rate_pct": round(random.uniform(1.2, 3.5), 2),
            "term_months":      term,
            "start_date":       start.isoformat(),
            "maturity_date":    (start + timedelta(days=term * 30)).isoformat(),
            "auto_rollover":    random.random() < 0.6,
            "status":           random.choices(["Active", "Matured"], weights=[0.7, 0.3])[0],
        })
    return pd.DataFrame(rows)

def gen_investment_holdings(customers: pd.DataFrame) -> pd.DataFrame:
    wealth_products = [p[0] for p in PRODUCTS if p[0].startswith("PRD-WL")]
    cust_ids = customers["customer_id"].tolist()
    rows = []
    for i in range(1, N_INVESTMENTS + 1):
        units = round(random.uniform(100, 50000), 4)
        nav = round(random.uniform(8.0, 35.0), 4)
        rows.append({
            "holding_id":     f"INV{i:07d}",
            "customer_id":    random.choice(cust_ids),
            "product_id":     random.choice(wealth_products),
            "units_held":     units,
            "average_cost_thb": round(nav * random.uniform(0.7, 1.2), 4),
            "current_nav_thb":  nav,
            "market_value_thb": round(units * nav, 2),
            "as_of_date":     TODAY.date().isoformat(),
        })
    return pd.DataFrame(rows)


# ---------------------------------------------------------------------------
# Domain C — Sales & Engagement
# ---------------------------------------------------------------------------

def gen_marketing_campaigns() -> pd.DataFrame:
    rows = []
    targets = [p[0] for p in PRODUCTS]
    for i in range(1, N_CAMPAIGNS + 1):
        start = random_date(datetime(2024, 1, 1), TODAY)
        end = start + timedelta(days=random.randint(14, 90))
        rows.append({
            "campaign_id":   f"CMP{i:04d}",
            "campaign_name": f"แคมเปญ {fake_th.word()} {start.year}",
            "objective":     random.choice(CAMPAIGN_OBJECTIVES),
            "channel":       random.choice(CAMPAIGN_CHANNELS),
            "target_product_id": random.choice(targets),
            "target_segment_id": random.choice([s[0] for s in SEGMENTS]),
            "start_date":    start.date().isoformat(),
            "end_date":      end.date().isoformat(),
            "budget_thb":    round(random.uniform(100_000, 5_000_000), 2),
            "status":        random.choices(["Planned", "Running", "Completed"], weights=[0.1, 0.3, 0.6])[0],
        })
    return pd.DataFrame(rows)

def gen_campaign_responses(customers: pd.DataFrame, campaigns: pd.DataFrame) -> pd.DataFrame:
    cust_ids = customers["customer_id"].tolist()
    cmp_ids = campaigns["campaign_id"].tolist()
    rows = []
    for i in range(1, N_CAMPAIGN_RESP + 1):
        outcome = random.choices(RESPONSE_OUTCOMES, weights=[0.25, 0.20, 0.40, 0.10, 0.05])[0]
        rows.append({
            "response_id":    f"CRS{i:08d}",
            "campaign_id":    random.choice(cmp_ids),
            "customer_id":    random.choice(cust_ids),
            "response_date":  random_date(datetime(2024, 1, 1), TODAY).date().isoformat(),
            "channel":        random.choice(CAMPAIGN_CHANNELS),
            "outcome":        outcome,
            "converted":      outcome == "Converted",
            "conversion_value_thb": round(random.uniform(1_000, 200_000), 2) if outcome == "Converted" else 0.0,
        })
    return pd.DataFrame(rows)

def gen_support_tickets(customers: pd.DataFrame, employees: pd.DataFrame) -> pd.DataFrame:
    cust_ids = customers["customer_id"].tolist()
    emp_ids = employees["employee_id"].tolist()
    rows = []
    for i in range(1, N_TICKETS + 1):
        opened = random_date(datetime(2024, 1, 1), TODAY)
        status = random.choices(TICKET_STATUSES, weights=[0.1, 0.15, 0.4, 0.3, 0.05])[0]
        closed = (opened + timedelta(hours=random.randint(1, 240))) if status in ("Resolved", "Closed") else None
        rows.append({
            "ticket_id":            f"TCK{i:07d}",
            "customer_id":          random.choice(cust_ids),
            "assigned_employee_id": random.choice(emp_ids),
            "category":             random.choice(TICKET_CATEGORIES),
            "channel":               random.choice(TICKET_CHANNELS),
            "priority":              random.choice(TICKET_PRIORITIES),
            "status":                status,
            "opened_at":             opened.isoformat(timespec="seconds"),
            "closed_at":             closed.isoformat(timespec="seconds") if closed else None,
            "subject":               f"[{random.choice(TICKET_CATEGORIES)}] {fake_th.sentence(nb_words=6)}",
            "csat_score":            random.choice([None, 1, 2, 3, 4, 5]) if status in ("Resolved", "Closed") else None,
        })
    return pd.DataFrame(rows)

def gen_service_interactions(customers: pd.DataFrame, employees: pd.DataFrame, branches: pd.DataFrame) -> pd.DataFrame:
    cust_ids = customers["customer_id"].tolist()
    emp_ids = employees["employee_id"].tolist()
    br_ids = branches["branch_id"].tolist()
    rows = []
    for i in range(1, N_INTERACTIONS + 1):
        ch = random.choice(INTERACTION_CHANNELS)
        rows.append({
            "interaction_id":  f"INT{i:08d}",
            "customer_id":     random.choice(cust_ids),
            "employee_id":     random.choice(emp_ids) if ch in ("Branch", "Call Center") else None,
            "branch_id":       random.choice(br_ids) if ch == "Branch" else None,
            "channel":         ch,
            "interaction_type": random.choice(INTERACTION_TYPES),
            "interaction_at":  random_date(datetime(2025, 1, 1), TODAY).isoformat(timespec="seconds"),
            "duration_seconds": random.randint(30, 1800),
            "notes":           fake_th.sentence(nb_words=8),
        })
    return pd.DataFrame(rows)

def gen_leads(customers: pd.DataFrame, employees: pd.DataFrame) -> pd.DataFrame:
    rows = []
    cust_ids = customers["customer_id"].tolist()
    emp_ids = employees["employee_id"].tolist()
    products = [p[0] for p in PRODUCTS]
    for i in range(1, N_LEADS + 1):
        is_existing = random.random() < 0.6
        rows.append({
            "lead_id":          f"LED{i:06d}",
            "lead_source":      random.choice(LEAD_SOURCES),
            "customer_id":      random.choice(cust_ids) if is_existing else None,
            "lead_full_name":   fake_th.name() if not is_existing else None,
            "phone":            thai_phone(),
            "email":            fake_en.email(),
            "interested_product_id": random.choice(products),
            "owner_employee_id": random.choice(emp_ids),
            "status":           random.choice(LEAD_STATUSES),
            "created_at":       random_date(datetime(2025, 1, 1), TODAY).isoformat(timespec="seconds"),
            "score":            random.randint(0, 100),
        })
    return pd.DataFrame(rows)

def gen_sales_opportunities(leads: pd.DataFrame) -> pd.DataFrame:
    lead_ids = leads["lead_id"].tolist()
    rows = []
    for i in range(1, N_OPPORTUNITIES + 1):
        amt = round(random.uniform(20_000, 5_000_000), 2)
        stage = random.choice(OPP_STAGES)
        rows.append({
            "opportunity_id":  f"OPP{i:06d}",
            "lead_id":         random.choice(lead_ids),
            "stage":           stage,
            "expected_value_thb": amt,
            "probability_pct": {
                "Prospecting": 10, "Qualification": 25, "Proposal": 50,
                "Negotiation": 75, "Closed Won": 100, "Closed Lost": 0,
            }[stage],
            "expected_close_date": random_date(TODAY, TODAY + timedelta(days=180)).date().isoformat(),
            "created_at":      random_date(datetime(2025, 1, 1), TODAY).isoformat(timespec="seconds"),
        })
    return pd.DataFrame(rows)


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main() -> None:
    print(f"Output directory: {OUTPUT_DIR}\n")

    print("Domain A — Customer")
    segments = gen_customer_segments();           to_csv(segments, "customer_segments")
    customers = gen_customers();                  to_csv(customers, "customers")
    addresses = gen_customer_addresses(customers); to_csv(addresses, "customer_addresses")
    seg_hist = gen_customer_segment_history(customers); to_csv(seg_hist, "customer_segment_history")
    kyc = gen_kyc_records(customers);             to_csv(kyc, "kyc_records")
    contacts = gen_customer_contacts(customers);  to_csv(contacts, "customer_contacts")

    print("\nDomain C — reference (Branches & Employees)")
    branches = gen_branches();                    to_csv(branches, "branches")
    employees = gen_employees(branches);          to_csv(employees, "employees")

    print("\nDomain B — Products")
    pcat = gen_product_categories();              to_csv(pcat, "product_categories")
    products = gen_products();                    to_csv(products, "products")
    accounts = gen_accounts(customers, branches); to_csv(accounts, "accounts")
    cards = gen_cards(customers, accounts);       to_csv(cards, "cards")
    loans = gen_loans(customers, branches);       to_csv(loans, "loans")
    schedule = gen_loan_repayment_schedule(loans); to_csv(schedule, "loan_repayment_schedule")
    fds = gen_fixed_deposits(customers, branches); to_csv(fds, "fixed_deposits")
    inv = gen_investment_holdings(customers);     to_csv(inv, "investment_holdings")

    print("\nDomain C — Sales & Engagement")
    campaigns = gen_marketing_campaigns();        to_csv(campaigns, "marketing_campaigns")
    responses = gen_campaign_responses(customers, campaigns); to_csv(responses, "campaign_responses")
    tickets = gen_support_tickets(customers, employees); to_csv(tickets, "support_tickets")
    interactions = gen_service_interactions(customers, employees, branches); to_csv(interactions, "service_interactions")
    leads = gen_leads(customers, employees);      to_csv(leads, "leads")
    opps = gen_sales_opportunities(leads);        to_csv(opps, "sales_opportunities")

    print("\n✅ All datasets generated.")


if __name__ == "__main__":
    main()
