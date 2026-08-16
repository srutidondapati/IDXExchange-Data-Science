import streamlit as st
import joblib
import pandas as pd

# Page setup
st.set_page_config(page_title="California Housing App", page_icon="🏡", layout="wide")

# Main Title & Subtitle (matching screenshot)
st.title("🏡 California Housing App")
st.write("Explore the price of single-family residential properties in California using a data-driven approach.")

# Navigation Tabs
tab_home, tab_predict, tab_app_info = st.tabs([
    "Home",
    "House Price Predictor", 
    "App Info", 
])

# ==============================================================================
# TAB 1: HOME
# ==============================================================================
with tab_home:
    st.header("Welcome")
    st.write("""
        ### What This App Does
        This web application provides real-time sale price estimates for **Single Family Residences** across California. By creating a model that blends traditional property specs (square footage, bedrooms, age) with **hyper-local spatial economics**, the tool estimates valuation based on recent market trends.
    
        ### Key Capabilities
        * **ZIP Code Lookup:** Enter a 5-digit ZIP code to automatically map city and school district price benchmarks.
        * **Custom Feature Engineering:** Factors in structural properties like `property_age` and `bed_bath_ratio`.
        * **Gradient Boosting Machine Learning:** Powered by an **XGBoost Regressor** trained on extensive California MLS market data.
        """)

    st.info("""
        🎯 **Optimal Range**
        
        This model achieves peak performance on single-family properties valued between **$500,000 and $1,000,000**.
        
        *Properties outside this window may have higher variance due to luxury market differences or non-standard features.*
        """)

# ==============================================================================
# TAB 2: HOUSE PRICE PREDICTION
# ==============================================================================
with tab_predict:
    st.header("House Price Prediction")
    st.caption("Enter the relevant property details below to predict the sale price of a single-family residential property in California.")
    
    # Artifact loader
    @st.cache_resource
    def load_artifacts():
        model = joblib.load('xgb_model.pkl')
        zip_median_lookup = joblib.load('zip_median_lookup.pkl')
        city_median_lookup = joblib.load('city_median_lookup.pkl')
        district_median_lookup = joblib.load('district_median_lookup.pkl')
        zip_to_city = joblib.load('zip_to_city.pkl')
        zip_to_district = joblib.load('zip_to_district.pkl')
        global_median = joblib.load('global_median.pkl')
        return model, zip_median_lookup, city_median_lookup, district_median_lookup, zip_to_city, zip_to_district, global_median

    try:
        model, zip_median_lookup, city_median_lookup, district_median_lookup, zip_to_city, zip_to_district, global_median = load_artifacts()
    except Exception as e:
        st.error("Error loading model artifacts.")
        st.stop()

    st.info(
            'Note: This model performs best for properties priced between '
            '$500K and $1M. Predictions outside this range may exhibit higher variance.'
        )

    col1, col2 = st.columns(2)

    with col1:
        living_area = st.number_input('Living Area (sq ft)', min_value=300, max_value=15000, value=1800, step=100)
        bedrooms = st.number_input('Bedrooms', min_value=1, max_value=10, value=3, step=1)
        bathrooms = st.number_input('Bathrooms', min_value=1, max_value=10, value=2, step=1)

    with col2:
        lot_size = st.number_input('Lot Size (sq ft)', min_value=0, max_value=100000, value=6500, step=500)
        year_built = st.number_input('Year Built', min_value=1900, max_value=2026, value=1990, step=1)
        zip_code = st.text_input('ZIP Code', value='90210')

    if st.button('Predict Price', type='primary'):
        # Clean ZIP input to 5 digits
        zip_input = str(zip_code).strip()[:5]

        city = zip_to_city.get(zip_input, "Unknown")
        district = zip_to_district.get(zip_input, "Unknown")

        # Look up location medians from precomputed dictionaries
        # if zip_input is not found, use global median as fallback
        zip_median = zip_median_lookup.get(zip_input, global_median)
        city_median = city_median_lookup.get(city, global_median)
        district_median = district_median_lookup.get(district, global_median)

        # Feature engineering
        property_age = 2026 - year_built
        bed_bath_ratio = bedrooms / max(bathrooms, 1)

        # Build feature vector (9 features)
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

        st.success(f'##### Estimated Sale Price: ${predicted_price:,.0f}')

        st.subheader('Input Summary')
        summary = {
            'Living Area': f'{living_area:,} sq ft',
            'Bedrooms': bedrooms,
            'Bathrooms': bathrooms,
            'Lot Size': f'{lot_size:,} sq ft',
            'Year Built': year_built,
            'Property Age': f'{property_age} years',
            'ZIP Code': zip_code,
            'ZIP Median Price Benchmark': f'${zip_median:,.0f}',
        }
        st.dataframe(pd.DataFrame(summary.items(), columns=['Field', 'Value']), use_container_width=True)


# ==============================================================================
# TAB 3: APP INFO
# ==============================================================================
with tab_app_info:
    st.header("App Info")
    st.write("### Machine Learning Engine: XGBoost")
    st.info("Model compared and selected against other regression algorithms: Linear Regression, Random Forest, Decision Trees.")
    st.write("""
    * **Algorithm:** Extreme Gradient Boosting (`XGBRegressor`)
    * **Training Data:** The model was trained on a dataset of over 100,000 single-family residential properties in California.
    * **Out-of-Time Validation:** Evaluated against an out-of-time test dataset to verify generalization and guard against overfitting.
    """)
    st.write("### Evaluation Metrics:")
    st.write("""
    * **R² Score:** The coefficient of determination, indicating the proportion of the variance in the dependent variable that is predictable from the independent variables.
    * **MAPE:** The mean absolute percentage error, a measure of the differences between values predicted by a model and the values actually observed.
    * **MdAPE:** The mean absolute percentage error, a measure of the differences between values predicted by a model and the values actually observed.
    """)
    st.write("""
    **Model Accuracy Notes:**
    - Most accurate for homes priced **$500K–$1M** (MdAPE: 6.98%)
    - Model improved **+7.5% over baseline** Linear Regression 
    through feature engineering and XGBoost tuning
    """)