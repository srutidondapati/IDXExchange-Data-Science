from pathlib import Path
import streamlit as st
import joblib
import pandas as pd
import base64
import plotly.express as px

st.set_page_config(page_title="California Housing Price Intelligence", page_icon="🏡", layout="wide")

BASE_DIR = Path(__file__).resolve().parent


def get_base64_image(path):
    with open(path, "rb") as f:
        return base64.b64encode(f.read()).decode()

hero_img_b64 = get_base64_image("hero.jpg")


# ==============================================================================
# STYLE
# ==============================================================================
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=Source+Serif+4:wght@600;700&display=swap');

:root {
    --primary: #17324D;
    --primary-dark: #10263A;
    --accent: #668B72;
    --accent-light: #E8EFE9;
    --gold: #B18A45;
    --gold-light: #F3EEDF;
    --background: #F6F7F6;
    --surface: #FFFFFF;
    --border: #D8DFDB;
    --text: #26313B;
    --muted: #647079;
    --rule: #E1E6E3;
}

html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
}

body {
    background: var(--background);
}

h1, h2, h3, h4, h5 {
    font-family: 'Source Serif 4', serif !important;
    color: var(--primary) !important;
}

h1 { margin-bottom: 0.25rem !important; }
h2, h3 { margin-top: 0.4rem !important; font-size: 1.5rem !important; }
h4 { font-size: 1.15rem !important; }

/* body text sizing */
.stMarkdown p, .stMarkdown li { font-size: 0.93rem !important; }

[data-testid="stCaptionContainer"] p {
    color: var(--muted) !important;
}

.block-container {
    padding-top: 1.1rem;
    padding-bottom: 3rem;
    max-width: 1180px;
}

.page-header {
    margin-top: 0;
}

.page-header h1 {
    margin-top: 0 !important;
}

.section-label {
    color: var(--accent);
    font-weight: 700;
    letter-spacing: 0.09em;
    font-size: 0.7rem;
    text-transform: uppercase;
    margin-bottom: 0.55rem;
}

div[data-testid="stVerticalBlockBorderWrapper"] {
    background: var(--surface) !important;
    border-radius: 2px !important;
    border: 1px solid var(--border) !important;
    box-shadow: 0 1px 2px rgba(23, 50, 77, 0.04);
    padding: 1rem 1.1rem;
}

div[data-testid="stHorizontalBlock"] div[data-testid="stVerticalBlockBorderWrapper"] {
    padding: 1.35rem 1.25rem !important;
}

div[data-baseweb="tab-list"],
div[role="tablist"] {
    display: flex !important;
    justify-content: flex-start !important;
    align-items: flex-end !important;
    column-gap: 2.5rem !important;
    gap: 2.5rem !important;
    width: 100% !important;
}

.callout {
    background-color: var(--accent-light);
    border-left: 3px solid var(--accent);
    border-radius: 2px;
    padding: 0.9rem 1.1rem;
    margin: 0.8rem 0;
    color: var(--text);
    font-size: 0.93rem;
}

.info-card-header {
    display: flex;
    align-items: center;
    gap: 0.6rem;
    margin-bottom: 0.7rem;
}

.info-card-header .icon { font-size: 1.4rem; }

.capability-title {
    font-weight: 700;
    color: var(--primary);
    margin-bottom: 0.5rem;
    font-size: 1rem;
}

.capability-desc {
    font-size: 0.87rem;
    color: var(--muted);
    line-height: 1.55;
    min-height: 3.6rem;
}

.capability-desc code {
    background: var(--accent-light);
    color: var(--primary);
    padding: 0.1rem 0.35rem;
    border-radius: 2px;
    font-size: 0.85em;
}

/* ---------- PAGE HEADER ---------- */

.page-header h1 {
    font-size: 1.9rem !important;
    margin-bottom: 0.2rem !important;
}

.page-header p {
    color: var(--muted);
    font-size: 0.92rem;
    margin: 0;
}

.page-divider {
    height: 1px;
    background: var(--rule);
    margin: 1rem 0 1.4rem 0;
}

/* ---------- HERO ---------- */

.hero {
    background:
        linear-gradient(105deg, rgba(16,38,58,0.95) 0%, rgba(23,50,77,0.90) 56%, rgba(86,143,102,0.82) 100%),
        var(--hero-bg-image);
    background-size: cover;
    background-position: center;
    border-radius: 2px 2px 0 0;
    padding: 2.1rem 2.6rem 1.9rem 2.6rem;
    color: white;
    min-height: 250px;
    border-top: 4px solid var(--accent);
}

.hero h1 {
    color: white !important;
    font-size: 2.35rem;
    line-height: 1.12;
    margin: 0 0 0.7rem 0 !important;
}

.hero p {
    color: #E8EEEA;
    font-size: 0.95rem;
    max-width: 680px;
    margin-bottom: 0;
    line-height: 1.55;
}

.hero .eyebrow {
    color: #C5D0D8;
    font-weight: 700;
    letter-spacing: 0.1em;
    font-size: 0.68rem;
    text-transform: uppercase;
    margin-bottom: 0.6rem;
}

.stat-bar {
    display: flex;
    background: var(--primary-dark);
    border-radius: 0 0 2px 2px;
    border-top: 1px solid rgba(255,255,255,0.10);
}

.stat-item {
    flex: 1;
    padding: 0.9rem 1.5rem;
    color: white;
    border-right: 1px solid rgba(255,255,255,0.13);
}

.stat-item:last-child { border-right: none; }

.stat-item .stat-value {
    font-family: 'Inter', sans-serif;
    font-size: 1.25rem;
    font-weight: 700;
}

.stat-item .stat-label {
    font-size: 0.68rem;
    color: #C8D3DC;
    margin-top: 3px;
}

.decision-item {
    margin-bottom: 0.9rem;
    line-height: 1.5;
    color: var(--text);
    font-size: 0.9rem;
}

.decision-item b { color: var(--primary); }

.price-result {
    text-align: center;
    padding: 1.45rem 1.2rem;
    background: var(--primary);
    border-radius: 2px;
    margin: 1rem 0;
    border-top: 3px solid var(--accent);
}

.price-result .price-label {
    font-size: 0.68rem;
    text-transform: uppercase;
    letter-spacing: 0.1em;
    color: #C8D3DC;
    margin-bottom: 0.25rem;
}

.price-result .price-value {
    font-family: 'Source Serif 4', serif;
    font-size: 2.55rem;
    font-weight: 700;
    color: white;
    line-height: 1.1;
}

.stat-card {
    text-align: left;
    padding: 0.15rem 0.1rem;
    border-left: 3px solid var(--accent);
    padding-left: 1rem;
}

.stat-card .stat-card-value {
    font-family: 'Inter', sans-serif;
    font-size: 1.65rem;
    font-weight: 700;
    color: var(--primary);
    line-height: 1.15;
}

.stat-card .stat-card-label {
    font-size: 0.7rem;
    color: var(--muted);
    margin-top: 0.35rem;
    line-height: 1.35;
}

div[data-baseweb="tab-list"] {
    display: flex !important;
    justify-content: flex-start !important;
    gap: 0 !important;
    width: max-content !important;
    border-bottom: 1px solid var(--border);
}

button[data-baseweb="tab"],
button[role="tab"] {
    font-family: 'Inter', sans-serif !important;
    font-weight: 600 !important;
    font-size: 0.87rem !important;
    color: var(--muted) !important;
    padding: 0.72rem 0 !important;
    margin: 0 2.5rem 0 0 !important;
    flex: 0 0 auto !important;
    min-width: max-content !important;
    width: auto !important;
}

button[data-baseweb="tab"]:last-child,
button[role="tab"]:last-child {
    margin-right: 0 !important;
}

button[data-baseweb="tab"][aria-selected="true"] {
    color: var(--primary) !important;
    font-weight: 700 !important;
}

button[kind="primary"] {
    background-color: var(--primary) !important;
    border-radius: 2px !important;
    border: 1px solid var(--primary) !important;
    font-weight: 700 !important;
}

button[kind="primary"]:hover {
    background-color: var(--primary-dark) !important;
    border-color: var(--primary-dark) !important;
}

div[data-testid="stNumberInput"] button {
    background-color: #F0F3F1 !important;
    border: 1px solid var(--border) !important;
    border-radius: 0 !important;
}

div[data-testid="stNumberInput"] button svg {
    fill: var(--primary) !important;
}

div[data-baseweb="input"] > div,
div[data-baseweb="select"] > div {
    border-radius: 2px !important;
}

[data-testid="stDataFrame"] {
    border-radius: 2px;
    overflow: hidden;
}

hr {
    border-color: var(--rule) !important;
    margin: 1.2rem 0 !important;
}

[data-testid="stExpander"] {
    border: 1px solid var(--border) !important;
    border-radius: 2px !important;
    background: var(--surface) !important;
}

[data-testid="stPlotlyChart"] { margin-top: 0.25rem; }

@media (max-width: 768px) {
    .hero {
        padding: 1.6rem 1.4rem;
        min-height: 220px;
    }
    .hero h1 { font-size: 1.9rem; }
    .stat-bar { flex-direction: column; }
    .stat-item {
        border-right: none;
        border-bottom: 1px solid rgba(255,255,255,0.13);
    }
    .stat-item:last-child { border-bottom: none; }
}
</style>
""", unsafe_allow_html=True)

# ==============================================================================
# PAGE SETUP
# ==============================================================================
st.markdown("""
<div class="page-header">
    <h1>California Housing Price Intelligence</h1>
    <p>Data-driven price estimates and market insights.</p>
</div>
<div class="page-divider"></div>
""", unsafe_allow_html=True)

# Navigation Tabs
tab_home, tab_predict, tab_market, tab_methodology = st.tabs([
    "Home",
    "Price Estimate",
    "Market",
    "Methodology",
])

# ==============================================================================
# TAB 1: HOME
# ==============================================================================
with tab_home:
    st.markdown(f"""
    <div class="hero" style="--hero-bg-image: url('data:image/jpeg;base64,{hero_img_b64}');">
        <div class="eyebrow">CALIFORNIA HOUSING PRICE INTELLIGENCE</div>
        <h1>Estimate the price. Make the right choice.</h1>
        <p>Real-time sale price estimates for single-family homes across California,
        combining property characteristics with hyper-local market data.</p>
    </div>
    <div class="stat-bar">
        <div class="stat-item">
            <div class="stat-value">$500K–$1M</div>
            <div class="stat-label">Best-performing price range</div>
        </div>
        <div class="stat-item">
            <div class="stat-value">XGBoost</div>
            <div class="stat-label">Prediction model</div>
        </div>
        <div class="stat-item">
            <div class="stat-value">100K+</div>
            <div class="stat-label">Training properties</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.write("")

    with st.container(border=True):
        st.markdown("""
        <div class="info-card-header">
            <div class="section-label" style="margin-bottom:0;">WHAT THIS APP DOES</div>
        </div>
        """, unsafe_allow_html=True)
        st.write("""
Estimate home values using property characteristics and hyper-local market data. The model
combines features such as square footage, bedrooms, and property age with ZIP, city, and
school-district price benchmarks.
        """)

    st.write("")
    st.markdown('<div class="section-label">KEY CAPABILITIES</div>', unsafe_allow_html=True)

    cap1, cap2, cap3 = st.columns(3)

    with cap1:
        with st.container(border=True):
            st.markdown("""
            <div class="capability-title">ZIP Code Lookup</div>
            <div class="capability-desc">Automatically maps ZIP codes to city and school-district price benchmarks.</div>
            """, unsafe_allow_html=True)

    with cap2:
        with st.container(border=True):
            st.markdown("""
            <div class="capability-title">Feature Engineering</div>
            <div class="capability-desc">Creates <code>property_age</code> and <code>bed_bath_ratio</code> from user inputs.</div>
            """, unsafe_allow_html=True)

    with cap3:
        with st.container(border=True):
            st.markdown("""
            <div class="capability-title">XGBoost Model</div>
            <div class="capability-desc">Predicts sale prices using property and hyper-local market features.</div>
            """, unsafe_allow_html=True)

# ==============================================================================
# TAB 2: PRICE ESTIMATE
# ==============================================================================
with tab_predict:
    st.markdown('<div class="section-label">PRICE ESTIMATE</div>', unsafe_allow_html=True)
    st.header("Get a price estimate")
    st.caption("Enter the relevant property details below to estimate the sale price of a single-family residential property in California.")

    @st.cache_resource
    def load_artifacts():
        model = joblib.load(BASE_DIR / "xgb_model.pkl")
        zip_median_lookup = joblib.load(BASE_DIR / "zip_median_lookup.pkl")
        city_median_lookup = joblib.load(BASE_DIR / "city_median_lookup.pkl")
        district_median_lookup = joblib.load(BASE_DIR / "district_median_lookup.pkl")
        zip_to_city = joblib.load(BASE_DIR / "zip_to_city.pkl")
        zip_to_district = joblib.load(BASE_DIR / "zip_to_district.pkl")
        global_median = joblib.load(BASE_DIR / "global_median.pkl")
        return model, zip_median_lookup, city_median_lookup, district_median_lookup, zip_to_city, zip_to_district, global_median

    @st.cache_data
    def load_market_data():
        zip_stats = joblib.load(BASE_DIR / "zip_stats.pkl")
        city_stats = joblib.load(BASE_DIR / "city_stats.pkl")
        market_summary = joblib.load(BASE_DIR / "market_summary.pkl")
        price_distribution = joblib.load(BASE_DIR / "price_distribution.pkl")
        monthly_trend = joblib.load(BASE_DIR / "monthly_trend.pkl")

        zip_to_city = {}
        zip_city_file = BASE_DIR / "zip_to_city.pkl"
        if zip_city_file.exists():
            zip_to_city = joblib.load(zip_city_file)

        zip_stats = zip_stats.copy()
        if "City" not in zip_stats.columns:
            zip_stats["City"] = (
                zip_stats["PostalCode5"]
                .astype(str)
                .map(zip_to_city)
                .fillna("ZIP " + zip_stats["PostalCode5"].astype(str))
            )

        return zip_stats, city_stats, market_summary, price_distribution, monthly_trend

    try:
        model, zip_median_lookup, city_median_lookup, district_median_lookup, zip_to_city, zip_to_district, global_median = load_artifacts()
    except Exception as e:
        st.error("Error loading model artifacts.")
        st.stop()

    form_col, guide_col = st.columns([1, 1])

    with form_col:
        with st.container(border=True):
            st.markdown('<div class="section-label">PROPERTY DETAILS</div>', unsafe_allow_html=True)

            c1, c2 = st.columns(2)
            with c1:
                living_area = st.number_input('Living Area (sq ft)', min_value=300, max_value=15000, value=1800, step=100)
                bedrooms = st.number_input('Bedrooms', min_value=1, max_value=10, value=3, step=1)
                year_built = st.number_input('Year Built', min_value=1900, max_value=2026, value=1990, step=1)

            with c2:
                lot_size = st.number_input('Lot Size (sq ft)', min_value=0, max_value=100000, value=6500, step=500)
                bathrooms = st.number_input('Bathrooms', min_value=1, max_value=10, value=2, step=1)

            st.markdown('<div class="section-label" style="margin-top:0.5rem;">LOCATION</div>', unsafe_allow_html=True)
            zip_code = st.text_input('ZIP Code', value='90210')

            predict_clicked = st.button('Get Estimate', type='primary')

    with guide_col:
        with st.container(border=True):
            st.markdown('<div class="section-label">UNDERSTANDING THE ESTIMATE</div>', unsafe_allow_html=True)
            st.markdown("""
            <div class="decision-item"><b>Best-performing range.</b><br>Accuracy is highest between $500K–$1M.</div>
            <div class="decision-item"><b>Edge cases.</b><br>Very low or high ZIP-level prices carry more uncertainty.</div>
            <div class="decision-item"><b>Use as a starting point.</b><br>Pair the estimate with comparable local sales.</div>
            """, unsafe_allow_html=True)

        with st.container(border=True):
            st.markdown('<div class="section-label">SCENARIO COMPARISON</div>', unsafe_allow_html=True)
            st.caption("These scenarios show how the model responds when one property feature is changed at a time.")

            def predict_with(living_area_value, bedrooms_value, bathrooms_value, lot_size_value, year_built_value, zip_value):
                zip_input_value = str(zip_value).strip()[:5]
                city_value = zip_to_city.get(zip_input_value, "Unknown")
                district_value = zip_to_district.get(zip_input_value, "Unknown")
                zip_median_value = zip_median_lookup.get(zip_input_value, global_median)
                city_median_value = city_median_lookup.get(city_value, global_median)
                district_median_value = district_median_lookup.get(district_value, global_median)
                property_age_value = 2026 - year_built_value
                bed_bath_ratio_value = bedrooms_value / max(bathrooms_value, 1)

                scenario_features = pd.DataFrame([{
                    'LivingArea': living_area_value,
                    'BedroomsTotal': bedrooms_value,
                    'BathroomsTotalInteger': bathrooms_value,
                    'LotSizeSquareFeet': lot_size_value,
                    'zip_median_price': zip_median_value,
                    'city_median_price': city_median_value,
                    'bed_bath_ratio': bed_bath_ratio_value,
                    'property_age': property_age_value,
                    'district_median_price': district_median_value,
                }])
                return model.predict(scenario_features)[0]

            base_price_preview = predict_with(living_area, bedrooms, bathrooms, lot_size, year_built, zip_code)
            bigger_home_price = predict_with(min(living_area + 250, 15000), bedrooms, bathrooms, lot_size, year_built, zip_code)
            newer_home_price = predict_with(living_area, bedrooms, bathrooms, lot_size, min(year_built + 10, 2026), zip_code)

            benchmark_delta = ((base_price_preview / max(global_median, 1)) - 1) * 100

            s1, s2 = st.columns(2)
            with s1:
                st.markdown(f"""
                <div class="stat-card" style="margin-bottom:0.2rem;">
                    <div class="stat-card-value">${base_price_preview:,.0f}</div>
                    <div class="stat-card-label">Current input set</div>
                </div>
                """, unsafe_allow_html=True)
            with s2:
                st.markdown(f"""
                <div class="stat-card" style="margin-bottom:0.2rem;">
                    <div class="stat-card-value">{benchmark_delta:+.1f}%</div>
                    <div class="stat-card-label">Vs. statewide median benchmark</div>
                </div>
                """, unsafe_allow_html=True)

            st.markdown(f"""
            <div class="decision-item"><b>+250 sq ft.</b> Estimated price: ${bigger_home_price:,.0f}</div>
            <div class="decision-item"><b>10 years newer.</b> Estimated price: ${newer_home_price:,.0f}</div>
            """, unsafe_allow_html=True)

    if predict_clicked:
        zip_input = str(zip_code).strip()[:5]

        city = zip_to_city.get(zip_input, "Unknown")
        district = zip_to_district.get(zip_input, "Unknown")

        zip_median = zip_median_lookup.get(zip_input, global_median)
        city_median = city_median_lookup.get(city, global_median)
        district_median = district_median_lookup.get(district, global_median)

        property_age = 2026 - year_built
        bed_bath_ratio = bedrooms / max(bathrooms, 1)

        features = pd.DataFrame([{
            'LivingArea': living_area,
            'BedroomsTotal': bedrooms,
            'BathroomsTotalInteger': bathrooms,
            'LotSizeSquareFeet': lot_size,
            'zip_median_price': zip_median,
            'city_median_price': city_median,
            'bed_bath_ratio': bed_bath_ratio,
            'property_age': property_age,
            'district_median_price': district_median,
        }])

        predicted_price = model.predict(features)[0]

        st.markdown(f"""
        <div class="price-result">
            <div class="price-label">Estimated Sale Price</div>
            <div class="price-value">${predicted_price:,.0f}</div>
        </div>
        """, unsafe_allow_html=True)

        with st.container(border=True):
            st.markdown('<div class="section-label">INPUT SUMMARY</div>', unsafe_allow_html=True)
            summary = {
                'Living Area': f'{living_area:,} sq ft',
                'Bedrooms': bedrooms,
                'Bathrooms': bathrooms,
                'Lot Size': f'{lot_size:,} sq ft',
                'Year Built': year_built,
                'Property Age': f'{property_age} years',
                'ZIP Code': zip_code,
                'City (matched)': city,
                'ZIP Median Price Benchmark': f'${zip_median:,.0f}',
            }
            st.dataframe(pd.DataFrame(summary.items(), columns=['Field', 'Value']), use_container_width=True, hide_index=True)

# ==============================================================================
# TAB 3: MARKET
# ==============================================================================
with tab_market:
    try:
        zip_stats, city_stats, market_summary, price_distribution, monthly_trend = load_market_data()
    except Exception:
        st.error("Market data files not found. Run the export cell in 07_prediction_app.ipynb first.")
        st.stop()

    st.markdown('<div class="section-label">MARKET SNAPSHOT</div>', unsafe_allow_html=True)
    st.header("California Housing Market")
    st.caption("Market trends and dynamics to help inform real estate decisions.")

    # Compute once, filtered — used everywhere on this tab so every stat agrees
    MIN_SALES_FOR_RANKING = 20
    ranked_cities = city_stats[city_stats["sales_count"] >= MIN_SALES_FOR_RANKING].copy()
    priciest_city = ranked_cities.loc[ranked_cities["median_ppsf"].idxmax()]
    cheapest_city = ranked_cities.loc[ranked_cities["median_ppsf"].idxmin()]

    price_change_pct = (
        (monthly_trend["median_price"].iloc[-1] - monthly_trend["median_price"].iloc[0])
        / monthly_trend["median_price"].iloc[0] * 100
    )

    m1, m2, m3, m4 = st.columns(4)
    for col, val, label in zip(
        [m1, m2, m3, m4],
        [
            f"{market_summary['homes_sold']:,}",
            f"${market_summary['median_ppsf']:.0f}",
            priciest_city["City"],
            f"{price_change_pct:+.1f}%",
        ],
        ["Homes Analyzed", "Median $/Sq Ft", f"Priciest City (≥{MIN_SALES_FOR_RANKING} sales)", "7-Month Trend"]
    ):
        with col:
            with st.container(border=True):
                st.markdown(f"""
                <div class="stat-card">
                    <div class="stat-card-value">{val}</div>
                    <div class="stat-card-label">{label}</div>
                </div>
                """, unsafe_allow_html=True)

    st.write("")

    # ---------- MAP ----------
    with st.container(border=True):
        st.markdown('<div class="section-label">ZIP CODE PRICE MAP</div>', unsafe_allow_html=True)
        st.caption("Median price per sq ft across California ZIP codes. Circle size = sales volume.")

        fig_map = px.scatter_map(
            zip_stats,
            lat="latitude",
            lon="longitude",
            size="sales_count",
            color="median_ppsf",
            color_continuous_scale=["#E8EFE9", "#668B72", "#17324D"],
            size_max=22,
            zoom=5.1,
            center={"lat": 37.0, "lon": -119.6},
            hover_name="PostalCode5",
            hover_data={
                "median_price": ":$,.0f",
                "median_ppsf": ":$,.0f",
                "sales_count": True,
                "latitude": False,
                "longitude": False,
            },
            labels={"median_ppsf": "$/sq ft", "median_price": "Median price", "sales_count": "Sales"},
            map_style="carto-positron",
            opacity=0.75,
        )
        fig_map.update_layout(
            height=520,
            margin=dict(l=0, r=0, t=0, b=0),
            coloraxis_colorbar=dict(title="$ / sq ft"),
        )
        st.plotly_chart(fig_map, use_container_width=True, key="zip_map")

    st.write("")

    # ---------- CITY RANKINGS ----------
    with st.container(border=True):
        st.markdown('<div class="section-label">CITY PRICE COMPARISON</div>', unsafe_allow_html=True)
        st.caption("Price-per-square-foot comparison across cities.")

        priciest_city_name = str(priciest_city["City"])
        priciest_city_ppsf = float(priciest_city["median_ppsf"])
        cheapest_city_name = str(cheapest_city["City"])
        cheapest_city_ppsf = float(cheapest_city["median_ppsf"])
        price_gap = priciest_city_ppsf / max(cheapest_city_ppsf, 1)

        st.markdown(f"""
        <div class="callout">
            Among cities with at least {MIN_SALES_FOR_RANKING} sales, <b>{priciest_city_name}</b> commands
            the highest price per square foot at <b>${priciest_city_ppsf:,.0f}</b>, while
            <b>{cheapest_city_name}</b> is the most affordable at <b>${cheapest_city_ppsf:,.0f}</b>,
            a gap of roughly <b>{price_gap:.1f}x</b>.
        </div>
        """, unsafe_allow_html=True)

        rc1, rc2 = st.columns(2)

        with rc1:
            st.markdown("**Top 8 by price per sq ft**")
            top_priced = ranked_cities.nlargest(8, "median_ppsf")[["City", "median_ppsf", "sales_count"]]
            top_priced = top_priced.rename(columns={"median_ppsf": "$/sq ft", "sales_count": "Sales"})
            top_priced["$/sq ft"] = top_priced["$/sq ft"].map(lambda x: f"${x:.0f}")
            st.dataframe(top_priced, use_container_width=True, hide_index=True)

        with rc2:
            st.markdown("**Most affordable 8, by price per sq ft**")
            bottom_priced = ranked_cities.nsmallest(8, "median_ppsf")[["City", "median_ppsf", "sales_count"]]
            bottom_priced = bottom_priced.rename(columns={"median_ppsf": "$/sq ft", "sales_count": "Sales"})
            bottom_priced["$/sq ft"] = bottom_priced["$/sq ft"].map(lambda x: f"${x:.0f}")
            st.dataframe(bottom_priced, use_container_width=True, hide_index=True)

    st.write("")

    # ---------- PRICE TREND ----------
    with st.container(border=True):
        st.markdown('<div class="section-label">PRICE TREND</div>', unsafe_allow_html=True)
        st.caption("Statewide median close price, month by month.")

        fig_trend = px.line(
            monthly_trend,
            x="SaleMonth",
            y="median_price",
            markers=True,
            labels={"SaleMonth": "Month", "median_price": "Median close price"},
        )
        fig_trend.update_traces(line_color="#17324D", marker_color="#668B72", line_width=3)
        fig_trend.update_layout(
            height=280, margin=dict(l=10, r=10, t=10, b=10),
            plot_bgcolor="white",
        )
        st.plotly_chart(fig_trend, use_container_width=True)
        st.caption("Seven months of closed sales — a short window, so treat this as directional rather than seasonal.")

    st.write("")

    # ---------- DISTRIBUTION ----------
    with st.container(border=True):
        st.markdown('<div class="section-label">PRICE DISTRIBUTION</div>', unsafe_allow_html=True)
        st.caption("Distribution of sale prices and price per sq ft.")

        d1, d2 = st.columns(2)
        with d1:
            fig_price = px.histogram(
                x=price_distribution["close_price"],
                nbins=40,
                labels={"x": "Close Price"},
            )
            fig_price.update_traces(marker_color="#668B72")
            fig_price.update_layout(
                height=280, margin=dict(l=10, r=10, t=10, b=10),
                yaxis_title="Homes sold", xaxis_title="Close price",
                plot_bgcolor="white",
            )
            st.plotly_chart(fig_price, use_container_width=True)

        with d2:
            fig_ppsf = px.histogram(
                x=price_distribution["price_per_sqft"],
                nbins=40,
                labels={"x": "Price per Sq Ft"},
            )
            fig_ppsf.update_traces(marker_color="#17324D")
            fig_ppsf.update_layout(
                height=280, margin=dict(l=10, r=10, t=10, b=10),
                yaxis_title="Homes sold", xaxis_title="Price per sq ft",
                plot_bgcolor="white",
            )
            st.plotly_chart(fig_ppsf, use_container_width=True)
        st.caption("Top and bottom 1% of values trimmed from both charts so a handful of outliers don't flatten the shape.")

    st.write("")

    # ---------- VOLUME BY CITY ----------
    with st.container(border=True):
        st.markdown('<div class="section-label">TRANSACTION VOLUME</div>', unsafe_allow_html=True)
        st.caption("Top 15 cities by homes sold.")

        top_cities = city_stats.head(15).sort_values("sales_count", ascending=True)

        fig_city = px.bar(
            top_cities,
            x="sales_count",
            y="City",
            orientation="h",
            color="median_ppsf",
            color_continuous_scale=["#E8EFE9", "#668B72", "#17324D"],
            labels={"sales_count": "Homes sold", "median_ppsf": "Median $/sq ft"},
        )
        fig_city.update_layout(
            height=420, margin=dict(l=10, r=10, t=10, b=10),
            plot_bgcolor="white", yaxis_title="", xaxis_title="Homes sold",
        )
        st.plotly_chart(fig_city, use_container_width=True)
        st.caption("Bar color still tracks price per square foot — a busy market isn't necessarily an expensive one.")

# ==============================================================================
# TAB 4: METHODOLOGY
# ==============================================================================
with tab_methodology:

    st.markdown(
        '<div class="section-label">MODEL OVERVIEW</div>',
        unsafe_allow_html=True
    )

    st.header("Methodology")
    st.caption(
        "How the model generates price estimates and how to interpret its results."
    )

    # --------------------------------------------------------------------------
    # QUICK SUMMARY
    # --------------------------------------------------------------------------

    s1, s2, s3 = st.columns(3)

    for col, val, label in zip(
        [s1, s2, s3],
        ["XGBoost", "8.75%", "4"],
        [
            "Selected model",
            "Overall MdAPE",
            "Models evaluated"
        ]
    ):
        with col:
            with st.container(border=True):
                st.markdown(
                    f"""
                    <div class="stat-card">
                        <div class="stat-card-value">{val}</div>
                        <div class="stat-card-label">{label}</div>
                    </div>
                    """,
                    unsafe_allow_html=True
                )

    st.write("")

    # --------------------------------------------------------------------------
    # HOW THE MODEL WORKS
    # --------------------------------------------------------------------------

    with st.container(border=True):

        st.markdown(
            '<div class="section-label">HOW IT WORKS</div>',
            unsafe_allow_html=True
        )

        st.markdown("#### Property → Location → Feature Engineering → XGBoost")

        w1, w2, w3, w4 = st.columns(4)

        with w1:
            st.markdown("""
            **01 · Property**

            Living area, bedrooms, bathrooms, lot size, and year built.
            """)

        with w2:
            st.markdown("""
            **02 · Location**

            ZIP, city, and school-district median price benchmarks are added.
            """)

        with w3:
            st.markdown("""
            **03 · Feature Engineering**

            Property age and bed-to-bath ratio are calculated from the inputs.
            """)

        with w4:
            st.markdown("""
            **04 · XGBoost**

            The model combines these features to estimate the property's sale price.
            """)

        st.markdown("""
        <div class="callout">
            <b>Model:</b> Extreme Gradient Boosting (<code>XGBRegressor</code>),
            trained on over 100,000 single-family residential properties in California
            and evaluated using an out-of-time test dataset.
        </div>
        """, unsafe_allow_html=True)

        st.markdown("""
        <div class="callout">
            <b>Time-based evaluation:</b> Training data covers <b>November 2025–May 2026</b>,
            while <b>June 2026</b> is held out as the test period. This chronological split
            helps evaluate how the model performs on a later month rather than randomly mixing
            future transactions into training data.
        </div>
        """, unsafe_allow_html=True)

        st.markdown("""
        <div class="callout">
            <b>Model selection:</b> Four regression models were evaluated: Linear Regression,
            Decision Tree, Random Forest, and XGBoost. XGBoost was selected based on its
            held-out test performance.
        </div>
        """, unsafe_allow_html=True)

    st.write("")

    # --------------------------------------------------------------------------
    # MODEL PERFORMANCE
    # --------------------------------------------------------------------------

    with st.container(border=True):

        st.markdown(
            '<div class="section-label">MODEL PERFORMANCE</div>',
            unsafe_allow_html=True
        )

        #st.markdown("#### R² 0.872  |  MAPE 13.64%  |  MdAPE 8.75%")

        r1, r2, r3 = st.columns(3)

        for col, val, label in zip(
            [r1, r2, r3],
            ["0.872", "13.64%", "8.75%"],
            [
                "R² Score",
                "MAPE",
                "MdAPE"
            ]
        ):
            with col:
                st.markdown(
                    f"""
                    <div class="stat-card">
                        <div class="stat-card-value">{val}</div>
                        <div class="stat-card-label">{label}</div>
                    </div>
                    """,
                    unsafe_allow_html=True
                )

        st.markdown("""
        <div class="callout">
            <b>What these mean:</b><br>
            R² measures how much of the variation in sale prices the model explains.<br>
            MAPE measures average percentage error, while MdAPE measures the median
            percentage error and is less affected by extreme prices.
        </div>
        """, unsafe_allow_html=True)

        st.markdown("##### Accuracy by price band")

        st.caption(
            "XGBoost MdAPE across four price tiers, held-out test data"
        )

        band_df = pd.DataFrame({
            'Price Band': [
                'Under $500K',
                '$500K–$1M',
                '$1M–$2M',
                'Over $2M'
            ],
            'XGB MdAPE %': [
                9.64,
                6.98,
                9.52,
                13.76
            ],
        })

        st.bar_chart(
            band_df.set_index('Price Band'),
            color='#668B72'
        )

        st.markdown("""
        <div class="callout">
            <b>Best performance: $500K–$1M.</b>
            This band has the lowest MdAPE at <b>6.98%</b> and contains
            5,327 of the test homes. Error increases at both price extremes,
            where the model has less representative data and fewer features
            describing unusual or luxury properties.
        </div>
        """, unsafe_allow_html=True)

    st.write("")

    # --------------------------------------------------------------------------
    # HOW TO INTERPRET THE ESTIMATE
    # --------------------------------------------------------------------------

    with st.container(border=True):

        st.markdown(
            '<div class="section-label">INTERPRETING THE ESTIMATE</div>',
            unsafe_allow_html=True
        )

        st.markdown("#### Use the estimate as a starting point")

        i1, i2, i3 = st.columns(3)

        with i1:
            st.markdown("""
            **$500K–$1M**

            This is where the model is most consistent. Use the estimate as a
            strong first check alongside standard review.
            """)

        with i2:
            st.markdown("""
            **Under $500K / $1M–$2M**

            Error is higher than in the $500K–$1M range. Cross-check the estimate
            against recent local comparable sales.
            """)

        with i3:
            st.markdown("""
            **Over $2M**

            This tier has the widest error margin. Consider additional specialist
            review because unique property features become more important.
            """)

    st.write("")

    # --------------------------------------------------------------------------
    # MODEL LIMITATIONS
    # --------------------------------------------------------------------------

    with st.container(border=True):

        st.markdown(
            '<div class="section-label">MODEL LIMITATIONS</div>',
            unsafe_allow_html=True
        )

        st.markdown("#### What the model can and cannot see")

        l1, l2 = st.columns(2)

        with l1:
            st.markdown("""
            **Built into the model**

            Living area, bedroom and bathroom counts, lot size, property age,
            and location benchmarks from ZIP, city, and school-district
            median prices.
            """)

        with l2:
            st.markdown("""
            **Outside its reach**

            Renovation quality, interior condition, views, noise exposure,
            and anything unique about a specific lot or floor plan.
            """)

    st.write("")

    # --------------------------------------------------------------------------
    # DETAILED METRICS
    # --------------------------------------------------------------------------

    with st.expander("View detailed metrics by price band for each model evaluated."):

        full_df = pd.DataFrame({
            'Price Band': [
                'Under $500K',
                '$500K–$1M',
                '$1M–$2M',
                'Over $2M'
            ],
            'Count': [
                1809,
                5327,
                3946,
                1702
            ],
            'RF MAPE %': [
                20.62,
                11.05,
                13.55,
                17.77
            ],
            'DT MAPE %': [
                25.81,
                14.77,
                19.84,
                25.12
            ],
            'LR MAPE %': [
                44.91,
                23.82,
                18.19,
                19.88
            ],
            'XGB MAPE %': [
                20.62,
                10.64,
                12.92,
                17.27
            ],
            'RF MdAPE %': [
                9.22,
                6.85,
                9.94,
                14.46
            ],
            'DT MdAPE %': [
                12.68,
                9.09,
                14.29,
                20.00
            ],
            'LR MdAPE %': [
                35.40,
                18.68,
                13.48,
                16.69
            ],
            'XGB MdAPE %': [
                9.64,
                6.98,
                9.52,
                13.76
            ],
        })

        st.dataframe(
            full_df,
            use_container_width=True,
            hide_index=True
        )

        st.caption("XGBoost — Best overall performance  " \
        "\nRandom Forest — Close second, but slightly less accurate  " \
        "\nDecision Tree — Higher variance and less stable performance  " \
        "\nLinear Regression — Weakest overall performance  " \
        "\n" \
        "\nThe $500K–$1M price band had the lowest prediction errors across all models and metrics.")