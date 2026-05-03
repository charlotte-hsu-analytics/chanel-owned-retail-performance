import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

# --------------------------------------------------
# Page setup
# --------------------------------------------------
st.set_page_config(
    page_title="Owned Retail Portfolio Performance Excellence Dashboard",
    layout="wide"
)

# --------------------------------------------------
# Color palette
# --------------------------------------------------
BLACK = "#111111"
CHARCOAL = "#333333"
CREAM = "#FAF7F2"
SOFT_GRAY = "#E6E0DA"
GOLD = "#C9A46C"
BEIGE = "#D8C3A5"
ROSE = "#B76E79"
GREEN = "#4F7D5A"
RED = "#B85C5C"
BLUE_GRAY = "#657A8A"

STATUS_COLORS = {
    "Above Target": GREEN,
    "Near Target": GOLD,
    "Below Target": RED,
}

CATEGORY_COLORS = {
    "Handbags": BLACK,
    "Small Leather Goods": "#6E6259",
    "Costume Jewelry": GOLD,
    "Other Accessories": BEIGE,
    "Eyewear": BLUE_GRAY,
    "Fragrance & Beauty": ROSE,
    "Ready-to-Wear": "#8C7B75",
    "Footwear": "#A3896B",
    "Watches": "#4A4A4A",
    "Fine Jewelry": "#C9A46C",
}

# --------------------------------------------------
# CSS
# --------------------------------------------------
st.markdown(
    """
    <style>
    .stApp {
        background-color: #FAF7F2;
        color: #333333;
    }

    h1, h2, h3, h4, h5, h6 {
        color: #111111 !important;
        font-weight: 700 !important;
    }

    p, div, span, label {
        color: #333333;
    }

    [data-testid="stSidebar"] {
        background-color: #F3ECE4;
    }

    [data-testid="stSidebar"] * {
        color: #333333 !important;
    }

    [data-baseweb="select"] > div {
        background-color: #FFFFFF;
        border: 1px solid #D8CFC6;
        border-radius: 10px;
    }

    [data-baseweb="tag"] {
        background-color: #111111 !important;
        color: white !important;
        border-radius: 999px !important;
        font-weight: 600 !important;
    }

    [data-baseweb="tag"] span {
        color: white !important;
    }

    [data-baseweb="tag"] svg {
        fill: white !important;
    }

    [data-testid="stMetric"] {
        background-color: #FFFFFF;
        border: 1px solid #D8CFC6;
        padding: 18px;
        border-radius: 14px;
        box-shadow: 0px 2px 8px rgba(17, 17, 17, 0.06);
    }

    [data-testid="stMetricLabel"] p {
        color: #5B514A !important;
        font-weight: 600 !important;
    }

    [data-testid="stMetricValue"] div {
        color: #111111 !important;
        font-weight: 700 !important;
    }

    .insight-box {
        background-color: #FFFFFF;
        color: #333333 !important;
        border: 1px solid #D8CFC6;
        border-left: 6px solid #C9A46C;
        padding: 18px;
        border-radius: 14px;
        margin-bottom: 18px;
        box-shadow: 0px 2px 8px rgba(17, 17, 17, 0.05);
    }

    .insight-box * {
        color: #333333 !important;
    }

    .stDownloadButton button {
        background-color: #111111;
        color: white;
        border-radius: 999px;
        border: none;
        font-weight: 600;
    }

    .stDownloadButton button:hover {
        background-color: #333333;
        color: white;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# --------------------------------------------------
# Helper functions
# --------------------------------------------------
def style_fig(fig):
    fig.update_layout(
        plot_bgcolor="white",
        paper_bgcolor="white",
        font=dict(color=CHARCOAL, size=13),
        title_font=dict(size=18, color=BLACK),
        legend_title_font=dict(color=CHARCOAL),
        legend_font=dict(color=CHARCOAL),
        margin=dict(l=35, r=35, t=70, b=60),
    )
    fig.update_xaxes(
        showgrid=False,
        tickfont=dict(color=CHARCOAL, size=12),
        title_font=dict(color=CHARCOAL, size=13)
    )
    fig.update_yaxes(
        gridcolor=SOFT_GRAY,
        tickfont=dict(color=CHARCOAL, size=12),
        title_font=dict(color=CHARCOAL, size=13)
    )
    return fig


def money(x):
    if pd.isna(x):
        return "$0"
    return f"${x:,.0f}"


def pct(x):
    if pd.isna(x):
        return "0.0%"
    return f"{x:.1f}%"


def safe_divide(a, b):
    return a / b if b else 0


# --------------------------------------------------
# Fast data loading
# --------------------------------------------------
@st.cache_data(show_spinner="Loading dashboard summary data...")
def load_summary_data():
    location_master = pd.read_csv("location_master.csv")
    monthly_perf = pd.read_csv("monthly_boutique_performance.csv")
    targets = pd.read_csv("boutique_targets.csv")
    bonus = pd.read_csv("commission_bonus.csv")
    assumptions = pd.read_csv("simulation_assumptions.csv")
    return location_master, monthly_perf, targets, bonus, assumptions


@st.cache_data(show_spinner="Loading sales transaction detail...")
def load_sales_data():
    sales = pd.read_csv("sales_transactions.csv")
    sales["transaction_date"] = pd.to_datetime(sales["transaction_date"])
    return sales


@st.cache_data(show_spinner="Loading clienteling detail...")
def load_clienteling_data():
    clienteling = pd.read_csv("clienteling_activity.csv")
    clienteling["activity_date"] = pd.to_datetime(clienteling["activity_date"])
    return clienteling


try:
    location_master, monthly_perf, targets, bonus, assumptions = load_summary_data()
except FileNotFoundError as e:
    st.error(f"Missing required CSV file: {e}")
    st.stop()

# --------------------------------------------------
# Header
# --------------------------------------------------
st.title("Owned Retail Portfolio Performance Excellence Dashboard")
st.caption("Sales Planning | Boutique Performance | Category Recap | Clienteling Insights | Incentive Accuracy")
st.caption("Created by Charlotte Hsu")

st.markdown(
    """
    <div class="insight-box">
    This dashboard uses a <b>simulated selected owned retail dataset</b> designed to mirror boutique-level performance reporting,
    sales planning, category recap, clienteling insights, and commission/bonus exception monitoring.
    The data is for portfolio demonstration only and does not represent Chanel internal data.
    </div>
    """,
    unsafe_allow_html=True
)

# --------------------------------------------------
# Sidebar filters
# --------------------------------------------------
st.sidebar.header("Filters")

month_filter = st.sidebar.multiselect(
    "Select Month",
    options=sorted(monthly_perf["month"].unique()),
    default=sorted(monthly_perf["month"].unique())
)

market_filter = st.sidebar.multiselect(
    "Select Market",
    options=sorted(monthly_perf["market"].unique()),
    default=sorted(monthly_perf["market"].unique())
)

location_type_filter = st.sidebar.multiselect(
    "Select Location Type",
    options=sorted(monthly_perf["location_type"].unique()),
    default=sorted(monthly_perf["location_type"].unique())
)

boutique_filter = st.sidebar.multiselect(
    "Select Boutique",
    options=sorted(monthly_perf["boutique"].unique()),
    default=sorted(monthly_perf["boutique"].unique())
)

st.sidebar.markdown("---")
st.sidebar.subheader("About")
st.sidebar.write(
    """
    Role-specific portfolio project aligned to Owned Retail Analytics & Insights.
    Focus areas: performance recaps, sales planning, category performance,
    clienteling productivity, and incentive payout exception monitoring.
    """
)

# --------------------------------------------------
# Apply filters to summary tables
# --------------------------------------------------
monthly_f = monthly_perf[
    monthly_perf["month"].isin(month_filter) &
    monthly_perf["market"].isin(market_filter) &
    monthly_perf["location_type"].isin(location_type_filter) &
    monthly_perf["boutique"].isin(boutique_filter)
].copy()

targets_f = targets[
    targets["month"].isin(month_filter) &
    targets["market"].isin(market_filter) &
    targets["location_type"].isin(location_type_filter) &
    targets["boutique"].isin(boutique_filter)
].copy()

bonus_f = bonus[
    bonus["month"].isin(month_filter) &
    bonus["market"].isin(market_filter) &
    bonus["location_type"].isin(location_type_filter) &
    bonus["boutique"].isin(boutique_filter)
].copy()

if monthly_f.empty:
    st.warning("No records match the selected filters.")
    st.stop()

# --------------------------------------------------
# Core metrics from summary data
# --------------------------------------------------
total_sales = monthly_f["total_sales"].sum()
total_target = monthly_f["boutique_sales_target"].sum()
total_ly = monthly_f["ly_figures"].sum()

attainment = safe_divide(total_sales, total_target) * 100
growth_vs_ly = (safe_divide(total_sales, total_ly) - 1) * 100
gap_to_target = total_sales - total_target

boutique_count = monthly_f["boutique"].nunique()
month_count = monthly_f["month"].nunique()
avg_monthly_target_per_boutique = safe_divide(total_target, boutique_count * month_count)

# Fast executive-level estimates to avoid loading raw transactions on app start
estimated_transactions = max(int(total_sales / 3200), 1)
estimated_units = estimated_transactions * 1.35
atv = safe_divide(total_sales, estimated_transactions)
upt = safe_divide(estimated_units, estimated_transactions)
return_rate = 5.5

# Fast clienteling estimates to avoid loading raw clienteling data on app start
clienteling_revenue_est = total_sales * 0.18
clienteling_conversion_est = 28.0
appointment_completion_est = 78.0

estimated_payout = bonus_f["estimated_payout"].sum()
payout_exceptions = (bonus_f["exception_flag"] == "Yes").sum()
bonus_eligible_count = (bonus_f["bonus_eligible"] == "Yes").sum()

# --------------------------------------------------
# Executive KPI Summary
# --------------------------------------------------
st.header("Executive Performance Recap")

st.markdown(
    """
    This section provides an executive-level recap of owned retail performance, including sales versus target,
    sales versus LY figures, boutique coverage, transaction productivity, clienteling revenue, and payout exception risk.
    It is designed to help leaders quickly understand whether the business is on track and where deeper review is needed.
    """
)

col1, col2, col3, col4 = st.columns(4)
col1.metric("Total Sales", money(total_sales))
col2.metric("Boutique Sales Target", money(total_target))
col3.metric("Sales vs Target", pct(attainment))
col4.metric("Gap to Target", money(gap_to_target))

col5, col6, col7, col8 = st.columns(4)
col5.metric("LY Figures", money(total_ly))
col6.metric("Sales vs LY", pct(growth_vs_ly))
col7.metric("Avg Monthly Target / Boutique", money(avg_monthly_target_per_boutique))
col8.metric("Boutiques in View", f"{boutique_count:,}")

col9, col10, col11, col12 = st.columns(4)
col9.metric("Estimated ATV", money(atv))
col10.metric("Estimated UPT", f"{upt:.2f}")
col11.metric("Estimated Return Rate", pct(return_rate))
col12.metric("Estimated Clienteling Revenue", money(clienteling_revenue_est))

col13, col14, col15, col16 = st.columns(4)
col13.metric("Estimated Clienteling Conversion", pct(clienteling_conversion_est))
col14.metric("Estimated Appointment Completion", pct(appointment_completion_est))
col15.metric("Bonus Eligible Advisors", f"{bonus_eligible_count:,}")
col16.metric("Payout Exceptions", f"{payout_exceptions:,}")

st.divider()

# --------------------------------------------------
# Executive Summary
# --------------------------------------------------
st.header("Executive Summary")

boutique_perf = (
    monthly_f.groupby(["boutique", "market", "location_type"], as_index=False)
    .agg(
        total_sales=("total_sales", "sum"),
        boutique_sales_target=("boutique_sales_target", "sum"),
        ly_figures=("ly_figures", "sum")
    )
)

boutique_perf["sales_vs_target_pct"] = boutique_perf["total_sales"] / boutique_perf["boutique_sales_target"] * 100
boutique_perf["sales_vs_ly_pct"] = (boutique_perf["total_sales"] / boutique_perf["ly_figures"] - 1) * 100

top_boutique = boutique_perf.sort_values("sales_vs_target_pct", ascending=False).iloc[0]["boutique"]
low_boutique = boutique_perf.sort_values("sales_vs_target_pct", ascending=True).iloc[0]["boutique"]

category_cols = {
    "Handbags": "handbags",
    "Small Leather Goods": "small_leather_goods",
    "Costume Jewelry": "costume_jewelry",
    "Other Accessories": "other_accessories",
    "Eyewear": "eyewear",
    "Fragrance & Beauty": "fragrance_beauty",
    "Ready-to-Wear": "ready_to_wear",
    "Footwear": "footwear",
    "Watches": "watches",
    "Fine Jewelry": "fine_jewelry",
}

category_totals = {
    label: monthly_f[col].sum()
    for label, col in category_cols.items()
}

top_category = max(category_totals, key=category_totals.get)

st.markdown(
    f"""
    <div class="insight-box">
    <b>Key Takeaways from Current Selection</b><br><br>
    1. Total sales are <b>{money(total_sales)}</b> against a boutique sales target of <b>{money(total_target)}</b>, for <b>{attainment:.1f}%</b> target attainment.<br>
    2. Sales are <b>{growth_vs_ly:.1f}%</b> versus LY figures, indicating current-period performance momentum.<br>
    3. <b>{top_boutique}</b> is the strongest boutique by target attainment, while <b>{low_boutique}</b> requires closer review.<br>
    4. <b>{top_category}</b> is the largest category contributor in the selected view.<br>
    5. There are <b>{payout_exceptions}</b> incentive payout exceptions requiring validation before payout finalization.
    </div>
    """,
    unsafe_allow_html=True
)

# --------------------------------------------------
# 1. Sales Planning & LY Performance
# --------------------------------------------------
st.header("1. Sales Planning & LY Performance")

st.markdown(
    """
    This section compares current sales performance against boutique sales targets and LY figures.
    The analysis supports commercial sales planning by showing whether the portfolio is pacing ahead or behind plan,
    and whether current performance is improving versus the prior year.
    """
)

monthly_summary = (
    monthly_f.groupby("month", as_index=False)
    .agg(
        total_sales=("total_sales", "sum"),
        boutique_sales_target=("boutique_sales_target", "sum"),
        ly_figures=("ly_figures", "sum")
    )
)

monthly_summary["sales_vs_target_pct"] = monthly_summary["total_sales"] / monthly_summary["boutique_sales_target"] * 100
monthly_summary["sales_vs_ly_pct"] = (monthly_summary["total_sales"] / monthly_summary["ly_figures"] - 1) * 100
monthly_summary["gap_to_target"] = monthly_summary["total_sales"] - monthly_summary["boutique_sales_target"]

col1, col2 = st.columns(2)

with col1:
    fig = go.Figure()
    fig.add_trace(go.Bar(
        x=monthly_summary["month"],
        y=monthly_summary["boutique_sales_target"],
        name="Boutique Sales Target",
        marker_color=BEIGE,
        hovertemplate="Month: %{x}<br>Target: $%{y:,.0f}<extra></extra>"
    ))
    fig.add_trace(go.Scatter(
        x=monthly_summary["month"],
        y=monthly_summary["total_sales"],
        name="Total Sales",
        mode="lines+markers",
        line=dict(color=BLACK, width=3),
        marker=dict(size=8),
        hovertemplate="Month: %{x}<br>Total Sales: $%{y:,.0f}<extra></extra>"
    ))
    fig.add_trace(go.Scatter(
        x=monthly_summary["month"],
        y=monthly_summary["ly_figures"],
        name="LY Figures",
        mode="lines+markers",
        line=dict(color=GOLD, width=3, dash="dash"),
        marker=dict(size=8),
        hovertemplate="Month: %{x}<br>LY Figures: $%{y:,.0f}<extra></extra>"
    ))
    fig.update_layout(
        title="Monthly Sales vs Target and LY Figures",
        yaxis_title="Sales",
        xaxis_title="Month",
        legend=dict(orientation="h", y=1.05)
    )
    fig.update_yaxes(tickprefix="$")
    st.plotly_chart(style_fig(fig), use_container_width=True)

with col2:
    fig = px.bar(
        monthly_summary,
        x="month",
        y="sales_vs_target_pct",
        title="Monthly Sales vs Target %",
        text="sales_vs_target_pct",
        color_discrete_sequence=[GOLD],
        labels={"month": "Month", "sales_vs_target_pct": "Sales vs Target %"}
    )
    fig.update_traces(texttemplate="%{text:.1f}%", textposition="outside")
    fig.update_yaxes(ticksuffix="%")
    st.plotly_chart(style_fig(fig), use_container_width=True)

# --------------------------------------------------
# 2. Boutique Performance Excellence
# --------------------------------------------------
st.header("2. Boutique Performance Excellence")

st.markdown(
    """
    This section evaluates boutique-level performance across target attainment and LY growth.
    It helps identify overperforming boutiques, underperforming boutiques, and locations that may require deeper review
    based on sales momentum, target gap, and location type.
    """
)

boutique_perf["status"] = pd.cut(
    boutique_perf["sales_vs_target_pct"],
    bins=[-999, 95, 100, 999],
    labels=["Below Target", "Near Target", "Above Target"]
).astype(str)

col1, col2 = st.columns(2)

with col1:
    fig = px.bar(
        boutique_perf.sort_values("sales_vs_target_pct", ascending=True),
        x="sales_vs_target_pct",
        y="boutique",
        orientation="h",
        color="status",
        color_discrete_map=STATUS_COLORS,
        title="Boutique Sales vs Target",
        text="sales_vs_target_pct",
        labels={"sales_vs_target_pct": "Sales vs Target %", "boutique": "Boutique"}
    )
    fig.update_traces(texttemplate="%{text:.1f}%", textposition="outside")
    fig.update_xaxes(ticksuffix="%")
    st.plotly_chart(style_fig(fig), use_container_width=True)

with col2:
    fig = px.scatter(
        boutique_perf,
        x="sales_vs_ly_pct",
        y="sales_vs_target_pct",
        size="total_sales",
        color="location_type",
        hover_name="boutique",
        title="Boutique Performance Matrix: Target Attainment vs LY Growth",
        labels={
            "sales_vs_ly_pct": "Sales vs LY %",
            "sales_vs_target_pct": "Sales vs Target %",
            "location_type": "Location Type"
        }
    )
    fig.add_hline(y=100, line_dash="dash", line_color=GOLD)
    fig.add_vline(x=0, line_dash="dash", line_color=BLUE_GRAY)
    fig.update_xaxes(ticksuffix="%")
    fig.update_yaxes(ticksuffix="%")
    st.plotly_chart(style_fig(fig), use_container_width=True)

# --------------------------------------------------
# 3. Category Performance Recap
# --------------------------------------------------
st.header("3. Category Performance Recap")

st.markdown(
    """
    This section summarizes sales performance by key retail categories and executive rollups.
    It helps identify which categories are driving total sales, how the business mix is distributed,
    and whether Accessories or Watches & Fine Jewelry are meaningful contributors to portfolio performance.
    """
)

category_sales = pd.DataFrame({
    "category": list(category_totals.keys()),
    "sales": list(category_totals.values())
}).sort_values("sales", ascending=False)

rollup_sales = pd.DataFrame({
    "rollup": ["Total Accessories", "Total Watches & Fine Jewelry"],
    "sales": [
        monthly_f["total_accessories"].sum(),
        monthly_f["total_watches_fine_jewelry"].sum()
    ]
})

col1, col2 = st.columns(2)

with col1:
    fig = px.bar(
        category_sales.sort_values("sales", ascending=True),
        x="sales",
        y="category",
        orientation="h",
        title="Sales by Category",
        text="sales",
        color="category",
        color_discrete_map=CATEGORY_COLORS,
        labels={"sales": "Sales", "category": "Category"}
    )
    fig.update_traces(texttemplate="$%{text:,.0f}", textposition="outside")
    fig.update_xaxes(tickprefix="$")
    st.plotly_chart(style_fig(fig), use_container_width=True)

with col2:
    fig = px.pie(
        category_sales,
        names="category",
        values="sales",
        title="Category Mix",
        color="category",
        color_discrete_map=CATEGORY_COLORS
    )
    st.plotly_chart(style_fig(fig), use_container_width=True)

fig = px.bar(
    rollup_sales,
    x="rollup",
    y="sales",
    title="Key Rollups: Total Accessories and Total Watches & Fine Jewelry",
    text="sales",
    color="rollup",
    color_discrete_sequence=[BLACK, GOLD],
    labels={"rollup": "Rollup", "sales": "Sales"}
)
fig.update_traces(texttemplate="$%{text:,.0f}", textposition="outside")
fig.update_yaxes(tickprefix="$")
st.plotly_chart(style_fig(fig), use_container_width=True)

# --------------------------------------------------
# 4. Clienteling Insights
# --------------------------------------------------
st.header("4. Clienteling Insights")

st.markdown(
    """
    This section evaluates clienteling productivity by outreach type and client segment.
    To keep the dashboard fast, detailed clienteling records are loaded only when this section is expanded.
    """
)

load_clienteling = st.checkbox("Load detailed clienteling charts", value=False)

if load_clienteling:
    clienteling = load_clienteling_data()

    clienteling_f = clienteling[
        clienteling["month"].isin(month_filter) &
        clienteling["market"].isin(market_filter) &
        clienteling["location_type"].isin(location_type_filter) &
        clienteling["boutique"].isin(boutique_filter)
    ].copy()

    clienteling_summary = (
        clienteling_f.groupby("outreach_type", as_index=False)
        .agg(
            outreach_count=("activity_id", "count"),
            appointments=("appointment_booked", lambda x: (x == "Yes").sum()),
            completed=("appointment_completed", lambda x: (x == "Yes").sum()),
            purchases=("purchase_made", lambda x: (x == "Yes").sum()),
            revenue=("purchase_amount", "sum")
        )
    )

    if not clienteling_summary.empty:
        clienteling_summary["booking_rate"] = clienteling_summary["appointments"] / clienteling_summary["outreach_count"] * 100
        clienteling_summary["purchase_conversion"] = clienteling_summary["purchases"] / clienteling_summary["outreach_count"] * 100

        col1, col2 = st.columns(2)

        with col1:
            fig = px.bar(
                clienteling_summary.sort_values("purchase_conversion", ascending=True),
                x="purchase_conversion",
                y="outreach_type",
                orientation="h",
                title="Clienteling Purchase Conversion by Outreach Type",
                text="purchase_conversion",
                color_discrete_sequence=[ROSE],
                labels={"purchase_conversion": "Purchase Conversion %", "outreach_type": "Outreach Type"}
            )
            fig.update_traces(texttemplate="%{text:.1f}%", textposition="outside")
            fig.update_xaxes(ticksuffix="%")
            st.plotly_chart(style_fig(fig), use_container_width=True)

        with col2:
            fig = px.bar(
                clienteling_summary.sort_values("revenue", ascending=True),
                x="revenue",
                y="outreach_type",
                orientation="h",
                title="Clienteling Revenue by Outreach Type",
                text="revenue",
                color_discrete_sequence=[GOLD],
                labels={"revenue": "Revenue", "outreach_type": "Outreach Type"}
            )
            fig.update_traces(texttemplate="$%{text:,.0f}", textposition="outside")
            fig.update_xaxes(tickprefix="$")
            st.plotly_chart(style_fig(fig), use_container_width=True)

    client_segment_summary = (
        clienteling_f.groupby("client_segment", as_index=False)
        .agg(
            outreach_count=("activity_id", "count"),
            purchases=("purchase_made", lambda x: (x == "Yes").sum()),
            revenue=("purchase_amount", "sum")
        )
    )

    if not client_segment_summary.empty:
        client_segment_summary["conversion"] = client_segment_summary["purchases"] / client_segment_summary["outreach_count"] * 100

        fig = px.bar(
            client_segment_summary.sort_values("revenue", ascending=True),
            x="revenue",
            y="client_segment",
            orientation="h",
            title="Clienteling Revenue by Client Segment",
            text="revenue",
            color_discrete_sequence=[BLUE_GRAY],
            labels={"revenue": "Revenue", "client_segment": "Client Segment"}
        )
        fig.update_traces(texttemplate="$%{text:,.0f}", textposition="outside")
        fig.update_xaxes(tickprefix="$")
        st.plotly_chart(style_fig(fig), use_container_width=True)
else:
    st.info("Detailed clienteling charts are available on demand to keep the dashboard fast for interview/demo use.")

# --------------------------------------------------
# 5. Commission & Bonus Accuracy Monitor
# --------------------------------------------------
st.header("5. Commission & Bonus Accuracy Monitor")

st.markdown(
    """
    This section monitors advisor-level incentive eligibility and payout exception risk.
    It supports payout accuracy by flagging records that may require review, including sales below threshold,
    clienteling score gaps, return adjustment issues, and target validation needs.
    """
)

exception_summary = (
    bonus_f[bonus_f["exception_flag"] == "Yes"]
    .groupby("exception_reason", as_index=False)
    .agg(exception_count=("sales_advisor", "count"))
    .sort_values("exception_count", ascending=True)
)

advisor_bonus = bonus_f.copy()
advisor_bonus["attainment_pct_display"] = advisor_bonus["attainment_pct"] * 100
advisor_bonus["clienteling_score_display"] = advisor_bonus["clienteling_score"] * 100
advisor_bonus["bubble_size"] = advisor_bonus["sales_amount"].abs().clip(lower=1000)

col1, col2 = st.columns(2)

with col1:
    if not exception_summary.empty:
        fig = px.bar(
            exception_summary,
            x="exception_count",
            y="exception_reason",
            orientation="h",
            title="Payout Exceptions by Reason",
            text="exception_count",
            color_discrete_sequence=[RED],
            labels={"exception_count": "Exception Count", "exception_reason": "Exception Reason"}
        )
        fig.update_traces(textposition="outside")
        st.plotly_chart(style_fig(fig), use_container_width=True)
    else:
        st.success("No payout exceptions in current selection.")

with col2:
    fig = px.scatter(
        advisor_bonus,
        x="attainment_pct_display",
        y="clienteling_score_display",
        size="bubble_size",
        color="bonus_eligible",
        hover_name="sales_advisor",
        hover_data={
            "boutique": True,
            "sales_amount": ":$,.0f",
            "target_amount": ":$,.0f",
            "attainment_pct_display": ":.1f",
            "clienteling_score_display": ":.1f",
            "estimated_payout": ":$,.0f",
            "bubble_size": False,
        },
        title="Advisor Attainment vs Clienteling Score",
        labels={
            "attainment_pct_display": "Sales Attainment %",
            "clienteling_score_display": "Clienteling Score %",
            "bonus_eligible": "Bonus Eligible"
        },
        color_discrete_map={"Yes": GREEN, "No": RED}
    )

    fig.add_vline(
        x=95,
        line_dash="dash",
        line_color=GOLD,
        annotation_text="95% Sales Threshold",
        annotation_position="top right"
    )

    fig.add_hline(
        y=12,
        line_dash="dash",
        line_color=BLUE_GRAY,
        annotation_text="12% Clienteling Threshold",
        annotation_position="bottom right"
    )

    fig.update_xaxes(ticksuffix="%")
    fig.update_yaxes(ticksuffix="%")
    st.plotly_chart(style_fig(fig), use_container_width=True)

st.subheader("Payout Exception Detail")

exception_detail = advisor_bonus[advisor_bonus["exception_flag"] == "Yes"][
    [
        "month",
        "boutique",
        "sales_advisor",
        "sales_amount",
        "target_amount",
        "attainment_pct",
        "clienteling_score",
        "estimated_payout",
        "exception_reason",
    ]
].copy()

if exception_detail.empty:
    st.success("No payout exceptions found for the selected filters.")
else:
    exception_detail["attainment_pct"] = exception_detail["attainment_pct"] * 100
    st.dataframe(
        exception_detail.style.format({
            "sales_amount": "${:,.0f}",
            "target_amount": "${:,.0f}",
            "attainment_pct": "{:.1f}%",
            "clienteling_score": "{:.1%}",
            "estimated_payout": "${:,.0f}",
        }),
        use_container_width=True
    )

# --------------------------------------------------
# 6. Data Explorer
# --------------------------------------------------
with st.expander("6. Data Explorer", expanded=False):
    st.markdown(
        """
        This section provides a self-service view of the underlying data tables used in the dashboard.
        Large detail files are loaded only when selected.
        """
    )

    explorer_option = st.selectbox(
        "Select table to view",
        [
            "Monthly Boutique Performance",
            "Boutique Targets",
            "Commission Bonus",
            "Location Master",
            "Simulation Assumptions",
            "Sales Transactions",
            "Clienteling Activity",
        ]
    )

    if explorer_option == "Monthly Boutique Performance":
        explorer_df = monthly_f
    elif explorer_option == "Boutique Targets":
        explorer_df = targets_f
    elif explorer_option == "Commission Bonus":
        explorer_df = bonus_f
    elif explorer_option == "Location Master":
        explorer_df = location_master
    elif explorer_option == "Simulation Assumptions":
        explorer_df = assumptions
    elif explorer_option == "Sales Transactions":
        sales_detail = load_sales_data()
        explorer_df = sales_detail[
            sales_detail["month"].isin(month_filter) &
            sales_detail["market"].isin(market_filter) &
            sales_detail["location_type"].isin(location_type_filter) &
            sales_detail["boutique"].isin(boutique_filter)
        ].copy()
    else:
        clienteling_detail = load_clienteling_data()
        explorer_df = clienteling_detail[
            clienteling_detail["month"].isin(month_filter) &
            clienteling_detail["market"].isin(market_filter) &
            clienteling_detail["location_type"].isin(location_type_filter) &
            clienteling_detail["boutique"].isin(boutique_filter)
        ].copy()

    row_limit = st.slider("Rows to display", min_value=50, max_value=500, value=100, step=50)

    st.dataframe(explorer_df.head(row_limit), use_container_width=True)

    csv = explorer_df.to_csv(index=False).encode("utf-8")
    st.download_button(
        label=f"Download {explorer_option} CSV",
        data=csv,
        file_name=f"{explorer_option.lower().replace(' ', '_')}.csv",
        mime="text/csv"
    )

# --------------------------------------------------
# Strategic Recommendations
# --------------------------------------------------
st.header("Strategic Recommendations")

st.markdown(
    """
    <div class="insight-box">
    <b>1. Focus performance recaps on sales-to-target and sales-to-LY variance.</b><br>
    The monthly recap should quickly show whether boutique performance is ahead or behind plan and whether current sales are improving versus LY figures.<br><br>

    <b>2. Use category rollups to guide commercial action.</b><br>
    Total Accessories and Total Watches & Fine Jewelry provide executive-level views, while category detail identifies the specific drivers behind growth or gap.<br><br>

    <b>3. Monitor boutique performance using more than sales volume.</b><br>
    Combining sales vs target, sales vs LY, clienteling revenue, ATV, and UPT gives a more complete view of boutique health.<br><br>

    <b>4. Use clienteling conversion to prioritize field coaching.</b><br>
    Outreach types and client segments with stronger conversion can inform advisor best practices and campaign follow-up strategy.<br><br>

    <b>5. Build payout exception monitoring into the reporting process.</b><br>
    Commission and bonus exception flags help support payout accuracy and reduce manual reconciliation risk.
    </div>
    """,
    unsafe_allow_html=True
)

# --------------------------------------------------
# Footer
# --------------------------------------------------
st.caption(
    "Created by Charlotte Hsu | Portfolio project using simulated selected owned retail data. "
    "This dashboard is designed to demonstrate performance reporting, sales planning, category recap, "
    "clienteling analytics, business intelligence infrastructure, and commission/bonus exception monitoring. "
    "The dataset is simulated for demonstration purposes and does not represent Chanel internal data."
)
