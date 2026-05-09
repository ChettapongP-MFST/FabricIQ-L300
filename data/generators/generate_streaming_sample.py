"""
generate_streaming_sample.py
============================
Generate a small JSONL sample of streaming events for the FabricIQ-L300 labs.

Outputs:
  ../streaming/card_transactions.sample.jsonl
  ../streaming/deposit_transactions.sample.jsonl

These samples are committed to git (see .gitignore exception). For producing
many events at scale, use the Fabric Spark notebook in
notebooks/streaming_to_eventhouse.ipynb.
"""

from __future__ import annotations

import json
import random
import uuid
from datetime import datetime, timedelta, timezone
from pathlib import Path

OUTPUT_DIR = Path(__file__).resolve().parent.parent / "streaming"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

random.seed(2026)

THAI_MERCHANTS = [
    "7-Eleven Sukhumvit",  "Tops Daily Asok",   "Big C Rajdamri",
    "CP All HQ",           "Lotus's Phra Ram 4","Central Embassy",
    "Siam Paragon",        "ICONSIAM",          "Terminal 21 Asok",
    "MBK Center",          "Lazada TH",         "Shopee TH",
    "Grab Food",           "LINE MAN",          "AIS Online",
    "True Online",         "BTS SkyTrain",      "MRT Bangkok",
    "PTT Station",         "Bangchak Petrol",   "Starbucks Silom",
    "Café Amazon",         "After You Siam",    "Krispy Kreme",
]

MCC_CODES = [
    ("5411", "Grocery"),
    ("5812", "Restaurant"),
    ("5541", "Fuel"),
    ("4111", "Transport"),
    ("5732", "Electronics"),
    ("5651", "Apparel"),
    ("5999", "Misc Retail"),
    ("4814", "Telecom"),
]

CARD_TYPES = ["Credit", "Debit"]
CHANNELS = ["POS", "Ecommerce", "Contactless", "ATM", "QR"]
DEPOSIT_TYPES = ["DEPOSIT", "WITHDRAW", "TRANSFER_IN", "TRANSFER_OUT", "PROMPTPAY_IN", "PROMPTPAY_OUT", "FEE"]


def now_minus(minutes: int) -> str:
    return (datetime.now(timezone.utc) - timedelta(minutes=minutes)).isoformat(timespec="seconds")


def card_event(i: int) -> dict:
    mcc = random.choice(MCC_CODES)
    amount = round(random.choice([
        random.uniform(50, 800),
        random.uniform(800, 5_000),
        random.uniform(5_000, 50_000),
    ]), 2)
    return {
        "event_id":      str(uuid.uuid4()),
        "event_time":    now_minus(random.randint(0, 240)),
        "card_id":       f"CRD{random.randint(1, 7500):07d}",
        "customer_id":   f"CUS{random.randint(1, 10000):07d}",
        "card_type":     random.choice(CARD_TYPES),
        "channel":       random.choice(CHANNELS),
        "merchant_name": random.choice(THAI_MERCHANTS),
        "mcc_code":      mcc[0],
        "mcc_category":  mcc[1],
        "amount_thb":    amount,
        "currency":      "THB",
        "auth_status":   random.choices(["APPROVED", "DECLINED"], weights=[0.95, 0.05])[0],
        "country":       "TH",
        "is_fraud_suspect": random.random() < 0.01,
    }


def deposit_event(i: int) -> dict:
    txn_type = random.choice(DEPOSIT_TYPES)
    amount = round(random.uniform(100, 200_000), 2)
    return {
        "event_id":     str(uuid.uuid4()),
        "event_time":   now_minus(random.randint(0, 240)),
        "account_id":   f"ACC{random.randint(1, 18000):08d}",
        "customer_id":  f"CUS{random.randint(1, 10000):07d}",
        "txn_type":     txn_type,
        "channel":      random.choice(["Mobile App", "ATM", "Branch", "Internet Banking", "PromptPay"]),
        "amount_thb":   amount,
        "currency":     "THB",
        "balance_after_thb": round(random.uniform(0, 5_000_000), 2),
        "counter_account": f"{random.randint(100,999)}-{random.randint(0,9)}-{random.randint(10000,99999)}-{random.randint(0,9)}"
                           if "TRANSFER" in txn_type or "PROMPTPAY" in txn_type else None,
        "branch_id":    f"BR{random.randint(1, 50):04d}" if random.random() < 0.3 else None,
    }


def write_jsonl(name: str, events: list[dict]) -> None:
    path = OUTPUT_DIR / name
    with path.open("w", encoding="utf-8") as f:
        for e in events:
            f.write(json.dumps(e, ensure_ascii=False) + "\n")
    print(f"  ✓ {name:42s} {len(events):>4} events")


def main() -> None:
    print(f"Output directory: {OUTPUT_DIR}\n")
    write_jsonl("card_transactions.sample.jsonl",    [card_event(i)    for i in range(50)])
    write_jsonl("deposit_transactions.sample.jsonl", [deposit_event(i) for i in range(50)])
    print("\n✅ Streaming samples generated.")


if __name__ == "__main__":
    main()
