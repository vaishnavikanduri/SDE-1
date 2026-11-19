"""
milk_check.py

Reads data.csv (our Country Delight order history, copied by hand from the app)
and prints a short report for Amma:
  - when the milk usually comes
  - which days it came late
  - days with no milk, and why
  - price changes and money spent

Run:  python milk_check.py            (uses data.csv)
      python milk_check.py other.csv  (uses another file)
"""

import csv
import sys
from datetime import datetime
from statistics import median

# ---------- SETTINGS (change these) ----------
LATE_AFTER = "07:30"        # Amma said: after 7:30 AM is late
WARN_MINUTES = 30           # also warn if milk came within this many minutes of LATE_AFTER
DATA_FILE = "data.csv"
# ---------------------------------------------


def to_minutes(hhmm):
    """'06:35' -> 395 minutes after midnight. Raises ValueError if bad."""
    t = datetime.strptime(hhmm.strip(), "%H:%M")
    return t.hour * 60 + t.minute


def to_hhmm(minutes):
    minutes = int(round(minutes))
    return f"{minutes // 60:02d}:{minutes % 60:02d}"


def load_rows(path):
    """Read the CSV. Bad rows are skipped and reported, never crash the program."""
    good, bad = [], []
    with open(path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for line_no, row in enumerate(reader, start=2):  # line 1 is the header
            try:
                day = datetime.strptime((row.get("date") or "").strip(), "%Y-%m-%d").date()
                status = (row.get("status") or "").strip()

                time_text = (row.get("delivery_time") or "").strip()
                time_min = to_minutes(time_text) if time_text else None
                if status == "Delivered" and time_min is None:
                    raise ValueError("delivered but no delivery_time")

                price_text = (row.get("total_rs") or "").strip()
                price = float(price_text) if price_text else None
                if price is not None and price <= 0:
                    raise ValueError("total_rs must be more than 0")

                good.append({
                    "date": day,
                    "status": status,
                    "time": time_min,
                    "price": price,
                    "notes": (row.get("notes") or "").strip(),
                })
            except (ValueError, TypeError) as err:
                bad.append((line_no, str(err)))
    good.sort(key=lambda r: r["date"])
    return good, bad


def report(rows, bad):
    late_limit = to_minutes(LATE_AFTER)
    delivered = [r for r in rows if r["status"] == "Delivered"]
    missed = [r for r in rows if r["status"] != "Delivered"]

    print("=" * 46)
    print(" MILK DELIVERY REPORT")
    if rows:
        print(f" {rows[0]['date']:%d %b %Y} to {rows[-1]['date']:%d %b %Y}")
    print("=" * 46)

    if bad:
        print(f"\nSkipped {len(bad)} bad row(s):")
        for line_no, why in bad:
            print(f"  line {line_no}: {why}")

    if not delivered:
        print("\nNo delivered rows to check.")
        return

    # 1. Usual delivery time
    times = sorted(r["time"] for r in delivered)
    print(f"\nDeliveries checked: {len(delivered)}")
    print(f"Usual time (middle value): {to_hhmm(median(times))}")
    print(f"Earliest: {to_hhmm(times[0])}   Latest: {to_hhmm(times[-1])}")

    # 2. Late and nearly late
    late = [r for r in delivered if r["time"] > late_limit]
    near = [r for r in delivered
            if late_limit - WARN_MINUTES <= r["time"] <= late_limit]
    print(f"\nLate (after {LATE_AFTER}): {len(late)}")
    for r in late:
        print(f"  {r['date']:%a %d %b}  {to_hhmm(r['time'])}")
    print(f"Nearly late (within {WARN_MINUTES} min of {LATE_AFTER}): {len(near)}")
    for r in near:
        print(f"  {r['date']:%a %d %b}  {to_hhmm(r['time'])}")

    # 3. Latest day of the week, on average
    by_day = {}
    for r in delivered:
        by_day.setdefault(r["date"].strftime("%a"), []).append(r["time"])
    avg = {d: sum(v) / len(v) for d, v in by_day.items()}
    worst = max(avg, key=avg.get)
    print(f"\nLatest day on average: {worst} ({to_hhmm(avg[worst])})")

    # 4. Days with no milk
    print(f"\nDays with no milk: {len(missed)}")
    for r in missed:
        print(f"  {r['date']:%a %d %b}  {r['notes'] or 'reason not known'}")

    # 5. Price changes and spend
    priced = [r for r in delivered if r["price"] is not None]
    print(f"\nPrice changes:")
    last = None
    changes = 0
    for r in priced:
        if last is not None and r["price"] != last:
            print(f"  {r['date']:%d %b}: Rs {last:g} -> Rs {r['price']:g}")
            changes += 1
        last = r["price"]
    if changes == 0:
        print("  none")
    unknown = len(delivered) - len(priced)
    print(f"Total spent (known days): Rs {sum(r['price'] for r in priced):g}"
          f"  ({unknown} day(s) with price not known)")

    # 6. A short message Amma can read
    print("\n" + "-" * 46)
    print(" MESSAGE FOR AMMA")
    print("-" * 46)
    print(f"Milk usually comes around {to_hhmm(median(times))}.")
    if late:
        print(f"It came after {LATE_AFTER} on {len(late)} day(s).")
    else:
        print(f"It never came after {LATE_AFTER} in these days.")
    if near:
        print(f"It came close to {LATE_AFTER} on {len(near)} day(s).")
    print(f"{worst} is usually the latest day.")


def main():
    path = sys.argv[1] if len(sys.argv) > 1 else DATA_FILE
    try:
        rows, bad = load_rows(path)
    except FileNotFoundError:
        print(f"Could not find {path}")
        sys.exit(1)
    report(rows, bad)


if __name__ == "__main__":
    main()