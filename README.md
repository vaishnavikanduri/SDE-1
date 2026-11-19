# Milk Delivery Checker

A small Python script that reads our family's milk delivery history and tells my mother when the milk usually arrives, which days it came late, which days we had no milk, and when the price changed.

- **Person:** Priya Kanduri, my mother, who manages our Country Delight milk order
- **Place:** our home, Swaminarayan City, Thane
- **Data collected:** Copied by hand from the Country Delight app's "My Orders" screen (12 screenshots)


## The problem

We get 2 packets of Buffalo Milk every morning from Country Delight. My mother's complaints were that it sometimes arrives late, and that the order isn't changed when we travel or have guests. She said anything after 7:30 AM is late.

## How to run

Needs Python 3. No extra packages.

    python milk_check.py            # reads data.csv
    python milk_check.py other.csv  # reads another file

To change what counts as late, edit the settings at the top of milk_check.py:

    LATE_AFTER = "07:30"
    WARN_MINUTES = 30

## data.csv

One row per day: date, day, delivery_time, product, packets, total_rs, status, notes

- 44 delivered days and 8 days with no milk, from 28 Sep to 18 Nov 2026.
- On 9 days the total was hidden behind the app's chat button in my screenshot, so I left it blank instead of guessing.
- Notes come from my mother (for example, the 12 to 18 Nov travel).

## Real output
 MILK DELIVERY REPORT
 28 Sep 2026 to 18 Nov 2026
==============================================

Deliveries checked: 44
Usual time (middle value): 06:22
Earliest: 05:36   Latest: 07:26

Late (after 07:30): 0
Nearly late (within 30 min of 07:30): 3
  Wed 21 Oct  07:07
  Sun 08 Nov  07:26
  Wed 11 Nov  07:04

Latest day on average: Mon (06:32)

Days with no milk: 8
  Mon 26 Oct  no entry in app history for this day
  Thu 12 Nov  family travelling (mother said)
  Fri 13 Nov  family travelling (mother said)
  Sat 14 Nov  family travelling (mother said)
  Sun 15 Nov  family travelling (mother said)
  Mon 16 Nov  family travelling (mother said)
  Tue 17 Nov  family travelling (mother said)
  Wed 18 Nov  family travelling (mother said)

Price changes:
  19 Oct: Rs 108 -> Rs 113
  20 Oct: Rs 113 -> Rs 109
Total spent (known days): Rs 3804  (9 day(s) with price not known)

----------------------------------------------
 MESSAGE FOR AMMA
----------------------------------------------
Milk usually comes around 06:22.
It never came after 07:30 in these days.
It came close to 07:30 on 3 day(s).
Mon is usually the latest day.

## Bad rows

Rows with an impossible date, a wrong time, a non-number price, or a "Delivered" row with no time are skipped and listed by line number. The rest of the report still runs.

## What this gets wrong

- The app's time may not be when the milk reached our door. It may be when the delivery was marked done. By my mother's own rule nothing was late, yet she remembers late days, so this gap is the biggest open question.
- Only 44 days. Days before 28 Sep are not included, and those may be the late ones she remembers.
- 9 prices are missing, so the total spent is too low.
- "Latest day on average" is weak. Each weekday has only about 6 deliveries, so one late morning changes the answer.
- It does not know about festivals or guests. Those are only in my mother's memory, not in the app.
- It should not be trusted to say whether the delivery service is good or bad overall. It only describes these 44 days from one app screen.