import numpy as np
import pandas as pd

np.random.seed(42)

# --------------------------------------------------
# Configuration
# --------------------------------------------------

START_DATE = "2025-01-01"
END_DATE = "2025-12-31"
OUTPUT_FILE = "Owned_Retail_Performance_Dataset_Chanel_Simulated_v3.xlsx"

# Completed category names
categories = [
    "Handbags",
    "Small Leather Goods",
    "Costume Jewelry",
    "Other Accessories",
    "Eyewear",
    "Fragrance & Beauty",
    "Ready-to-Wear",
    "Footwear",
    "Watches",
    "Fine Jewelry",
]

accessory_categories = [
    "Handbags",
    "Small Leather Goods",
    "Costume Jewelry",
    "Other Accessories",
    "Eyewear",
]

wfj_categories = ["Watches", "Fine Jewelry"]

# Average monthly boutique target is designed to be close to $6.4M
locations = [
    {
        "boutique": "Madison Avenue",
        "market": "New York",
        "region": "Americas",
        "location_type": "Fashion Flagship",
        "primary_division": "Fashion",
        "base_monthly_target": 9_800_000,
    },
    {
        "boutique": "Beverly Hills",
        "market": "West Coast",
        "region": "Americas",
        "location_type": "Fashion Flagship",
        "primary_division": "Fashion",
        "base_monthly_target": 8_600_000,
    },
    {
        "boutique": "Miami Design District",
        "market": "Southeast",
        "region": "Americas",
        "location_type": "Fashion Boutique",
        "primary_division": "Fashion",
        "base_monthly_target": 7_100_000,
    },
    {
        "boutique": "SoHo",
        "market": "New York",
        "region": "Americas",
        "location_type": "Fashion Boutique",
        "primary_division": "Fashion",
        "base_monthly_target": 6_600_000,
    },
    {
        "boutique": "South Coast Plaza",
        "market": "West Coast",
        "region": "Americas",
        "location_type": "Fashion + Beauty Boutique",
        "primary_division": "Fashion",
        "base_monthly_target": 6_700_000,
    },
    {
        "boutique": "San Francisco",
        "market": "West Coast",
        "region": "Americas",
        "location_type": "Fashion Boutique",
        "primary_division": "Fashion",
        "base_monthly_target": 6_000_000,
    },
    {
        "boutique": "Chicago",
        "market": "Midwest",
        "region": "Americas",
        "location_type": "Fashion Boutique",
        "primary_division": "Fashion",
        "base_monthly_target": 5_800_000,
    },
    {
        "boutique": "Dallas",
        "market": "South",
        "region": "Americas",
        "location_type": "Fashion Boutique",
        "primary_division": "Fashion",
        "base_monthly_target": 5_600_000,
    },
    {
        "boutique": "Fifth Avenue Beauty",
        "market": "New York",
        "region": "Americas",
        "location_type": "Fragrance & Beauty Boutique",
        "primary_division": "Fragrance & Beauty",
        "base_monthly_target": 4_200_000,
    },
    {
        "boutique": "Boston Beauty",
        "market": "Northeast",
        "region": "Americas",
        "location_type": "Fragrance & Beauty Boutique",
        "primary_division": "Fragrance & Beauty",
        "base_monthly_target": 3_600_000,
    },
]

location_master = pd.DataFrame(locations)

location_master["supports_fashion"] = np.where(
    location_master["location_type"].str.contains("Fashion"), "Yes", "No"
)

location_master["supports_fnb"] = np.where(
    location_master["location_type"].str.contains("Beauty"), "Yes", "No"
)

location_master["supports_wfj"] = np.where(
    location_master["location_type"].isin(
        ["Fashion Flagship", "Fashion Boutique", "Fashion + Beauty Boutique"]
    ),
    "Yes",
    "No",
)

location_master["open_status"] = "Open"

# Monthly seasonality
seasonality = {
    1: 0.88,
    2: 0.90,
    3: 0.96,
    4: 1.00,
    5: 1.03,
    6: 1.00,
    7: 0.94,
    8: 0.82,
    9: 1.05,
    10: 1.10,
    11: 1.22,
    12: 1.42,
}

# Chanel-style category mix by location type
category_mix_by_type = {
    "Fashion Flagship": {
        "Handbags": 0.30,
        "Small Leather Goods": 0.08,
        "Costume Jewelry": 0.07,
        "Other Accessories": 0.05,
        "Eyewear": 0.03,
        "Fragrance & Beauty": 0.08,
        "Ready-to-Wear": 0.20,
        "Footwear": 0.07,
        "Watches": 0.04,
        "Fine Jewelry": 0.08,
    },
    "Fashion Boutique": {
        "Handbags": 0.34,
        "Small Leather Goods": 0.09,
        "Costume Jewelry": 0.08,
        "Other Accessories": 0.06,
        "Eyewear": 0.03,
        "Fragrance & Beauty": 0.06,
        "Ready-to-Wear": 0.20,
        "Footwear": 0.08,
        "Watches": 0.025,
        "Fine Jewelry": 0.035,
    },
    "Fashion + Beauty Boutique": {
        "Handbags": 0.28,
        "Small Leather Goods": 0.08,
        "Costume Jewelry": 0.06,
        "Other Accessories": 0.05,
        "Eyewear": 0.03,
        "Fragrance & Beauty": 0.22,
        "Ready-to-Wear": 0.15,
        "Footwear": 0.07,
        "Watches": 0.025,
        "Fine Jewelry": 0.035,
    },
    "Fragrance & Beauty Boutique": {
        "Handbags": 0.00,
        "Small Leather Goods": 0.00,
        "Costume Jewelry": 0.00,
        "Other Accessories": 0.02,
        "Eyewear": 0.00,
        "Fragrance & Beauty": 0.90,
        "Ready-to-Wear": 0.00,
        "Footwear": 0.00,
        "Watches": 0.00,
        "Fine Jewelry": 0.08,
    },
}

avg_ticket = {
    "Handbags": 7200,
    "Small Leather Goods": 1250,
    "Costume Jewelry": 1650,
    "Other Accessories": 900,
    "Eyewear": 650,
    "Fragrance & Beauty": 220,
    "Ready-to-Wear": 4800,
    "Footwear": 1350,
    "Watches": 9500,
    "Fine Jewelry": 13500,
}

sales_advisor_count = {
    "Fashion Flagship": 18,
    "Fashion Boutique": 12,
    "Fashion + Beauty Boutique": 14,
    "Fragrance & Beauty Boutique": 10,
}

client_segments = ["New", "Repeat", "VIP", "Reactivated"]
channels = ["Boutique Walk-In", "Private Appointment", "Clienteling Outreach", "Event"]

# --------------------------------------------------
# Calendar
# --------------------------------------------------

calendar = pd.DataFrame({"date": pd.date_range(START_DATE, END_DATE, freq="D")})
calendar["year"] = calendar["date"].dt.year
calendar["month"] = calendar["date"].dt.to_period("M").astype(str)
calendar["month_num"] = calendar["date"].dt.month
calendar["quarter"] = "Q" + calendar["date"].dt.quarter.astype(str)
calendar["week"] = calendar["date"].dt.isocalendar().week.astype(int)
calendar["day_of_week"] = calendar["date"].dt.day_name()

calendar["retail_season"] = np.select(
    [
        calendar["month_num"].isin([3, 4, 5]),
        calendar["month_num"].isin([6, 7, 8]),
        calendar["month_num"].isin([9, 10]),
        calendar["month_num"].isin([11, 12]),
    ],
    ["Spring", "Summer", "Fall", "Holiday"],
    default="Winter",
)

months = sorted(calendar["month"].unique())

# --------------------------------------------------
# Monthly Boutique Performance + Boutique Targets
# --------------------------------------------------

monthly_rows = []
target_rows = []

for _, loc in location_master.iterrows():
    boutique = loc["boutique"]
    market = loc["market"]
    region = loc["region"]
    location_type = loc["location_type"]
    base_target = loc["base_monthly_target"]

    category_mix = category_mix_by_type[location_type]

    for month in months:
        month_number = int(month[-2:])
        seasonal_factor = seasonality[month_number]

        boutique_sales_target = base_target * seasonal_factor

        # Current-year boutique attainment
        if month_number in [11, 12]:
            attainment = np.random.normal(loc=0.99, scale=0.07)
        elif month_number == 8:
            attainment = np.random.normal(loc=0.96, scale=0.06)
        else:
            attainment = np.random.normal(loc=1.01, scale=0.07)

        attainment = np.clip(attainment, 0.84, 1.16)

        category_actuals = {}
        category_targets = {}
        category_ly = {}

        for cat in categories:
            base_share = category_mix[cat]
            category_share = max(base_share * np.random.normal(loc=1.0, scale=0.08), 0)

            cat_target = boutique_sales_target * category_share
            cat_actual = cat_target * attainment * np.random.normal(loc=1.0, scale=0.06)

            ly_growth = np.random.normal(loc=1.035, scale=0.08)
            ly_growth = np.clip(ly_growth, 0.88, 1.22)

            cat_ly = cat_actual / ly_growth if ly_growth else cat_actual

            category_targets[cat] = round(cat_target, 2)
            category_actuals[cat] = round(max(cat_actual, 0), 2)
            category_ly[cat] = round(max(cat_ly, 0), 2)

            if cat == "Fragrance & Beauty":
                division = "Fragrance & Beauty"
            elif cat in ["Watches", "Fine Jewelry"]:
                division = "Watches & Fine Jewelry"
            else:
                division = "Fashion"

            target_rows.append(
                {
                    "month": month,
                    "boutique": boutique,
                    "market": market,
                    "region": region,
                    "location_type": location_type,
                    "division": division,
                    "category": cat,
                    "monthly_sales_target": round(cat_target, 2),
                    "traffic_target": int(np.random.randint(1200, 5200) * seasonal_factor),
                    "conversion_target": round(np.random.uniform(0.18, 0.35), 3),
                    "clienteling_target": int(np.random.randint(150, 650) * seasonal_factor),
                }
            )

        total_accessories = sum(category_actuals[c] for c in accessory_categories)
        total_watches_fine_jewelry = sum(category_actuals[c] for c in wfj_categories)
        total_sales = sum(category_actuals.values())

        total_accessories_ly = sum(category_ly[c] for c in accessory_categories)
        total_watches_fine_jewelry_ly = sum(category_ly[c] for c in wfj_categories)
        ly_figures = sum(category_ly.values())

        monthly_rows.append(
            {
                "month": month,
                "boutique": boutique,
                "market": market,
                "region": region,
                "location_type": location_type,
                "boutique_sales_target": round(boutique_sales_target, 2),
                "ly_figures": round(ly_figures, 2),
                "handbags": category_actuals["Handbags"],
                "small_leather_goods": category_actuals["Small Leather Goods"],
                "costume_jewelry": category_actuals["Costume Jewelry"],
                "other_accessories": category_actuals["Other Accessories"],
                "eyewear": category_actuals["Eyewear"],
                "total_accessories": round(total_accessories, 2),
                "fragrance_beauty": category_actuals["Fragrance & Beauty"],
                "ready_to_wear": category_actuals["Ready-to-Wear"],
                "footwear": category_actuals["Footwear"],
                "watches": category_actuals["Watches"],
                "fine_jewelry": category_actuals["Fine Jewelry"],
                "total_watches_fine_jewelry": round(total_watches_fine_jewelry, 2),
                "total_sales": round(total_sales, 2),
                "sales_vs_target_pct": round(total_sales / boutique_sales_target, 4),
                "sales_vs_ly_pct": round(total_sales / ly_figures - 1, 4) if ly_figures else 0,
                "gap_to_target": round(total_sales - boutique_sales_target, 2),
                "total_accessories_ly": round(total_accessories_ly, 2),
                "total_watches_fine_jewelry_ly": round(total_watches_fine_jewelry_ly, 2),
            }
        )

monthly_boutique_performance = pd.DataFrame(monthly_rows)
boutique_targets = pd.DataFrame(target_rows)

# --------------------------------------------------
# Sales Transactions
# --------------------------------------------------

advisor_lookup = {}

for _, loc in location_master.iterrows():
    boutique = loc["boutique"]
    count = sales_advisor_count[loc["location_type"]]
    advisor_lookup[boutique] = [
        f"{boutique.split()[0]} Advisor {i}" for i in range(1, count + 1)
    ]

transaction_rows = []
transaction_id = 1

for _, row in monthly_boutique_performance.iterrows():
    boutique = row["boutique"]
    market = row["market"]
    region = row["region"]
    location_type = row["location_type"]
    month = row["month"]

    month_dates = calendar[calendar["month"] == month]["date"].values

    category_sales_map = {
        "Handbags": row["handbags"],
        "Small Leather Goods": row["small_leather_goods"],
        "Costume Jewelry": row["costume_jewelry"],
        "Other Accessories": row["other_accessories"],
        "Eyewear": row["eyewear"],
        "Fragrance & Beauty": row["fragrance_beauty"],
        "Ready-to-Wear": row["ready_to_wear"],
        "Footwear": row["footwear"],
        "Watches": row["watches"],
        "Fine Jewelry": row["fine_jewelry"],
    }

    for cat, cat_sales in category_sales_map.items():
        if cat_sales <= 0:
            continue

        estimated_tx = int(cat_sales / avg_ticket[cat])
        n_tx = int(np.clip(estimated_tx, 6, 90))

        weights = np.random.dirichlet(np.ones(n_tx))
        amounts = weights * cat_sales

        for amount in amounts:
            transaction_date = pd.Timestamp(np.random.choice(month_dates))
            advisor = np.random.choice(advisor_lookup[boutique])

            if cat == "Fragrance & Beauty":
                division = "Fragrance & Beauty"
            elif cat in ["Watches", "Fine Jewelry"]:
                division = "Watches & Fine Jewelry"
            else:
                division = "Fashion"

            client_type = np.random.choice(client_segments, p=[0.36, 0.34, 0.20, 0.10])
            channel = np.random.choice(channels, p=[0.46, 0.20, 0.26, 0.08])

            units = np.random.choice(
                [1, 1, 1, 2, 2, 3],
                p=[0.48, 0.20, 0.12, 0.12, 0.05, 0.03],
            )

            return_flag = np.random.choice(["Yes", "No"], p=[0.055, 0.945])
            discount_flag = np.random.choice(["Yes", "No"], p=[0.035, 0.965])

            transaction_rows.append(
                {
                    "transaction_id": f"T{transaction_id:07d}",
                    "transaction_date": transaction_date.date(),
                    "month": month,
                    "quarter": f"Q{transaction_date.quarter}",
                    "boutique": boutique,
                    "market": market,
                    "region": region,
                    "location_type": location_type,
                    "division": division,
                    "category": cat,
                    "subcategory": cat,
                    "sales_advisor": advisor,
                    "client_id": f"C{np.random.randint(10000, 99999)}",
                    "client_type": client_type,
                    "transaction_amount": round(amount, 2),
                    "units": units,
                    "return_flag": return_flag,
                    "discount_flag": discount_flag,
                    "channel": channel,
                }
            )

            transaction_id += 1

sales_transactions = pd.DataFrame(transaction_rows)

# --------------------------------------------------
# Clienteling Activity
# --------------------------------------------------

clienteling_rows = []
activity_id = 1

outreach_types = [
    "Text",
    "Email",
    "Phone",
    "Private Appointment",
    "Event Invitation",
    "Product Follow-Up",
]

for _, loc in location_master.iterrows():
    boutique = loc["boutique"]
    market = loc["market"]
    region = loc["region"]
    location_type = loc["location_type"]

    for month in months:
        month_dates = calendar[calendar["month"] == month]["date"].values

        monthly_target = boutique_targets[
            (boutique_targets["boutique"] == boutique)
            & (boutique_targets["month"] == month)
        ]["clienteling_target"].sum()

        n_activities = int(np.clip(monthly_target * np.random.uniform(0.55, 0.95), 80, 600))

        for _ in range(n_activities):
            activity_date = pd.Timestamp(np.random.choice(month_dates))
            advisor = np.random.choice(advisor_lookup[boutique])
            client_segment = np.random.choice(client_segments, p=[0.24, 0.39, 0.25, 0.12])
            outreach_type = np.random.choice(
                outreach_types,
                p=[0.31, 0.24, 0.14, 0.11, 0.10, 0.10],
            )

            base_book_rate = {
                "Text": 0.18,
                "Email": 0.12,
                "Phone": 0.20,
                "Private Appointment": 0.65,
                "Event Invitation": 0.28,
                "Product Follow-Up": 0.36,
            }[outreach_type]

            if client_segment == "VIP":
                base_book_rate += 0.14
            elif client_segment == "New":
                base_book_rate -= 0.04

            appointment_booked = np.random.rand() < base_book_rate
            appointment_completed = appointment_booked and (np.random.rand() < 0.78)

            purchase_prob = 0.17
            if appointment_completed:
                purchase_prob += 0.34
            if client_segment == "VIP":
                purchase_prob += 0.18
            if outreach_type == "Product Follow-Up":
                purchase_prob += 0.09

            purchase_made = np.random.rand() < purchase_prob

            purchase_amount = 0
            if purchase_made:
                purchase_amount = np.random.lognormal(mean=np.log(4200), sigma=0.85)
                if client_segment == "VIP":
                    purchase_amount *= 1.85
                purchase_amount = round(np.clip(purchase_amount, 180, 60_000), 2)

            clienteling_rows.append(
                {
                    "activity_id": f"A{activity_id:07d}",
                    "activity_date": activity_date.date(),
                    "month": month,
                    "boutique": boutique,
                    "market": market,
                    "region": region,
                    "location_type": location_type,
                    "sales_advisor": advisor,
                    "client_id": f"C{np.random.randint(10000, 99999)}",
                    "client_segment": client_segment,
                    "outreach_type": outreach_type,
                    "appointment_booked": "Yes" if appointment_booked else "No",
                    "appointment_completed": "Yes" if appointment_completed else "No",
                    "purchase_made": "Yes" if purchase_made else "No",
                    "purchase_amount": purchase_amount,
                    "days_since_last_purchase": int(np.random.gamma(shape=3, scale=45)),
                }
            )

            activity_id += 1

clienteling_activity = pd.DataFrame(clienteling_rows)

# --------------------------------------------------
# Commission / Bonus
# --------------------------------------------------

sales_by_advisor = (
    sales_transactions
    .groupby(
        ["month", "boutique", "market", "region", "location_type", "sales_advisor"],
        as_index=False,
    )
    .agg(
        sales_amount=("transaction_amount", "sum"),
        units_sold=("units", "sum"),
        return_count=("return_flag", lambda x: (x == "Yes").sum()),
        transaction_count=("transaction_id", "nunique"),
    )
)

commission_rows = []

for _, row in sales_by_advisor.iterrows():
    month = row["month"]
    boutique = row["boutique"]
    advisor = row["sales_advisor"]

    advisor_sales = max(row["sales_amount"], 25_000)

    simulated_attainment = np.random.normal(loc=1.00, scale=0.16)
    simulated_attainment = np.clip(simulated_attainment, 0.60, 1.40)

    target_amount = advisor_sales / simulated_attainment
    attainment_pct = row["sales_amount"] / target_amount if target_amount else 0

    clienteling_subset = clienteling_activity[
        (clienteling_activity["month"] == month)
        & (clienteling_activity["boutique"] == boutique)
        & (clienteling_activity["sales_advisor"] == advisor)
    ]

    outreach_count = len(clienteling_subset)
    purchase_count = (clienteling_subset["purchase_made"] == "Yes").sum()
    clienteling_score = purchase_count / outreach_count if outreach_count else 0

    return_adjustment = abs(row["sales_amount"]) * 0.015 if row["return_count"] > 3 else 0

    bonus_eligible = (
        attainment_pct >= 0.95
        and clienteling_score >= 0.12
        and row["sales_amount"] > 0
        and row["return_count"] <= 5
    )

    estimated_payout = 0

    if bonus_eligible:
        estimated_payout = row["sales_amount"] * 0.012
        if attainment_pct >= 1.10:
            estimated_payout *= 1.25
        estimated_payout -= return_adjustment
        estimated_payout = max(estimated_payout, 0)

    random_data_issue = np.random.rand()

    if random_data_issue < 0.015:
        exception_flag = "Yes"
        exception_reason = "Target validation needed"
    elif row["return_count"] > 5:
        exception_flag = "Yes"
        exception_reason = "Return adjustment review"
    elif attainment_pct < 0.85:
        exception_flag = "Yes"
        exception_reason = "Below payout threshold"
    elif attainment_pct >= 0.95 and clienteling_score < 0.12:
        exception_flag = "Yes"
        exception_reason = "Clienteling score below threshold"
    elif 0.85 <= attainment_pct < 0.95:
        exception_flag = "Yes"
        exception_reason = "Near threshold review"
    else:
        exception_flag = "No"
        exception_reason = "Payout ready"

    commission_rows.append(
        {
            "month": month,
            "boutique": boutique,
            "market": row["market"],
            "region": row["region"],
            "location_type": row["location_type"],
            "sales_advisor": advisor,
            "sales_amount": round(row["sales_amount"], 2),
            "target_amount": round(target_amount, 2),
            "attainment_pct": round(attainment_pct, 4),
            "clienteling_score": round(clienteling_score, 4),
            "return_adjustment": round(return_adjustment, 2),
            "bonus_eligible": "Yes" if bonus_eligible else "No",
            "estimated_payout": round(estimated_payout, 2),
            "payout_status": "Ready"
            if bonus_eligible and exception_reason == "Payout ready"
            else "Review",
            "exception_flag": exception_flag,
            "exception_reason": exception_reason,
        }
    )

commission_bonus = pd.DataFrame(commission_rows)

# --------------------------------------------------
# Simulation assumptions
# --------------------------------------------------

assumptions = pd.DataFrame(
    [
        {
            "assumption_area": "Project scope",
            "assumption": "Simulated selected owned retail portfolio across Fashion Boutiques, Fragrance & Beauty retail, and Watches & Fine Jewelry.",
        },
        {
            "assumption_area": "Monthly target",
            "assumption": "Average monthly target across selected boutiques is anchored around $6.4M, with higher targets for flagship locations and lower targets for beauty-focused doors.",
        },
        {
            "assumption_area": "Category structure",
            "assumption": "Categories use completed names: Handbags, Small Leather Goods, Costume Jewelry, Other Accessories, Eyewear, Fragrance & Beauty, Ready-to-Wear, Footwear, Watches, Fine Jewelry, Total Accessories, and Total Watches & Fine Jewelry.",
        },
        {
            "assumption_area": "Target planning",
            "assumption": "Targets are generated by boutique, month, and category with seasonality and category-mix assumptions.",
        },
        {
            "assumption_area": "LY figures",
            "assumption": "LY figures are simulated from current sales and category-level growth assumptions.",
        },
        {
            "assumption_area": "Commission logic",
            "assumption": "Advisor payout eligibility is based on sales attainment, clienteling score, and return/data-quality exception checks.",
        },
        {
            "assumption_area": "Data disclaimer",
            "assumption": "This dataset is simulated for analytics portfolio demonstration and does not represent Chanel internal data.",
        },
    ]
)

# --------------------------------------------------
# Export
# --------------------------------------------------

with pd.ExcelWriter(OUTPUT_FILE, engine="openpyxl") as writer:
    location_master.to_excel(writer, sheet_name="Location_Master", index=False)
    monthly_boutique_performance.to_excel(
        writer, sheet_name="Monthly_Boutique_Performance", index=False
    )
    boutique_targets.to_excel(writer, sheet_name="Boutique_Targets", index=False)
    sales_transactions.to_excel(writer, sheet_name="Sales_Transactions", index=False)
    clienteling_activity.to_excel(writer, sheet_name="Clienteling_Activity", index=False)
    commission_bonus.to_excel(writer, sheet_name="Commission_Bonus", index=False)
    calendar.to_excel(writer, sheet_name="Calendar", index=False)
    assumptions.to_excel(writer, sheet_name="Simulation_Assumptions", index=False)

# --------------------------------------------------
# Validation summary
# --------------------------------------------------

annual_target = monthly_boutique_performance["boutique_sales_target"].sum()
annual_sales = monthly_boutique_performance["total_sales"].sum()
annual_ly = monthly_boutique_performance["ly_figures"].sum()

monthly_summary = (
    monthly_boutique_performance.groupby("month", as_index=False)
    .agg(
        total_sales=("total_sales", "sum"),
        boutique_sales_target=("boutique_sales_target", "sum"),
        ly_figures=("ly_figures", "sum"),
    )
)

monthly_summary["sales_vs_target_pct"] = (
    monthly_summary["total_sales"] / monthly_summary["boutique_sales_target"] * 100
)
monthly_summary["sales_vs_ly_pct"] = (
    monthly_summary["total_sales"] / monthly_summary["ly_figures"] - 1
) * 100

print("Created:", OUTPUT_FILE)
print("\nAnnual selected portfolio target:", f"${annual_target:,.0f}")
print("Annual selected portfolio sales:", f"${annual_sales:,.0f}")
print("Annual LY figures:", f"${annual_ly:,.0f}")
print("Average monthly target per boutique:", f"${annual_target / 12 / len(location_master):,.0f}")

print("\nMonthly summary:")
print(monthly_summary)

print("\nSheet shapes:")
print("Location_Master:", location_master.shape)
print("Monthly_Boutique_Performance:", monthly_boutique_performance.shape)
print("Boutique_Targets:", boutique_targets.shape)
print("Sales_Transactions:", sales_transactions.shape)
print("Clienteling_Activity:", clienteling_activity.shape)
print("Commission_Bonus:", commission_bonus.shape)
print("Calendar:", calendar.shape)
print("Simulation_Assumptions:", assumptions.shape)

print("\nBonus exception mix:")
print(commission_bonus["exception_reason"].value_counts())
