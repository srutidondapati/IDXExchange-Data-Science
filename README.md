# IDXExchange Project

## Project Overview:
The IDXExchange project uses machine learning models to predict ClosePrice, the sale price of a single residential property in California.

The project uses real estate property data sourced from the California Regional Multiple Listing Service (CRMLS). The workflow includes data exploration, preprocessing, feature engineering, geographic price features, model comparison, advanced modeling, evaluation across different price ranges, and a Streamlit prediction application.

The final model is a tuned XGBoost regressor, which achieved a test R² of 0.872436.

---

## Dataset Source

The dataset consists of approximately six months of real estate property data sourced from CRMLS (California Regional Multiple Listing Service).

The project focuses on:
- PropertyType = Residential
- PropertySubType = SingleFamilyResidence

The target variable is:
- ClosePrice — the final sale price of the property

Important original features include:
- LivingArea
- BedroomsTotal
- BathroomsTotalInteger
- LotSizeSquareFeet
- YearBuilt
- PostalCode
- City
- UnifiedSchoolDistrict

---

## Data Preprocessing

The preprocessing workflow was performed before training the machine learning models.

- #### Handling Missing Values:
    - ClosePrice: 0 nulls, no handling necessary
    - LivingArea: 35 nulls, dropped rows (since it is required for model)
    - BedroomsTotal: 0 nulls, no handling necessary
    - BathroomsTotalInteger: 2 nulls, filled with median (under 50% threshold)
    - LotSizeSquareFeet: 1,210 nulls, filled with median (under 50% threshold)

 - #### Outlier Removal:
     - Removed large/unrealistic values using the findings from Week 2 data exploration
       - ClosePrice: kept between $50K and $10M
       - LivingArea: kept between 300 and 15,000 sq ft

- #### Geographic Features: (PostalCode and City)
    - ZIP code median prices range from $75K to $9M
    - City median prices range from $75K to $6.9M
    - encoded as median price features computed on training data: zip_median_price, city_median_price
 
- #### Train/Test Split:
    - Training: November 2025 – May 2026
    - Test: June 2026
    - Final Features (X): LivingArea, BedroomsTotal, BathroomsTotalInteger, 
      LotSizeSquareFeet, zip_median_price, city_median_price
    - Target (y): ClosePrice

---

## Models Tested

- ### Linear Regression
    - Linear Regression was used as the baseline model because it is simple, fast, and provides an initial benchmark.

- ### Decision Tree
    - Decision Tree regression was tested to capture nonlinear relationships between property features and sale price.

- ### Random Forest
    - Random Forest combines multiple decision trees to improve generalization and reduce the instability of a single decision tree.

- ### XGBoost
    - XGBoost was tested as an advanced gradient boosting model. A tuned version was created by adjusting:
        - n_estimators
        - learning_rate
        - max_depth

    - The best-performing hyperparameters were:
        - n_estimators = 300
        - learning_rate = 0.10
        - max_depth = 9

---

## Feature Engineering

#### Old Features
- `LivingArea`, `BedroomsTotal`, `BathroomsTotalInteger`, `LotSizeSquareFeet`, `zip_median_price`, `city_median_price`

#### New Features
- `property_age`: years since property was built (2026 - YearBuilt)
- `bed_bath_ratio`: bedrooms divided by bathrooms
- `district_median_price`: median ClosePrice per Unified School District

---

## Model Results

| Model | Test R² |
| -------- | -------- |
| Linear Regression | 0.799203  |
| Decision Tree  | 0.744029  |
| Random Forest  | 0.865858  |
| Baseline XGBoost  | 0.868322  |
| Tuned XGBoost  | 0.872436  |

*Best Model* : Tuned XGBoost
    - Test R² : 0.872436
    - Improvement over baseline XGBoost: 0.004114

---

## Evaluation by Price Band

In addition to R², the models were evaluated using:
    - MAPE (Mean Absolute Percentage Error)
    - MdAPE (Median Absolute Percentage Error)

| Price Band | Count | RF MAPE% | DT MAPE% | LR MAPE% | XGB MAPE% | RF MdAPE% | DT MdAPE% | LR MdAPE% | XGB MdAPE% |
| -------- | -------- | -------- | -------- | -------- | -------- | -------- | -------- | -------- | -------- |
| Under $500k | 1809 | 20.62 | 24.95 | 44.91 | 20.62 | 9.22 | 12.63 | 35.40 | 9.64 |
| $500k-$1M | 5327 | 11.05 | 14.73 | 23.82 | 10.64 | 6.85 | 9.15 | 18.68 | 6.98 |
| $1M-$2M | 3946 | 13.55 | 19.52 | 18.19 | 12.92 | 9.94 | 13.98 | 13.48 | 9.52 |
| Over $2M | 1702 | 17.77 | 24.71 | 19.88 | 17.27 | 14.46 | 20.00 | 16.69 | 13.76 |

*Overall Model Ranking*
1. XGBoost — Best overall performance
2. Random Forest — Close second
3. Decision Tree — Higher variance and less stable performance
4. Linear Regression — Weakest overall performance

The $500K–$1M price band had the lowest prediction errors across all models and metrics.

---

## Streamlit Prediction App

A Streamlit application was created to allow users to enter property information and receive a predicted sale price.

The application accepts property information such as:
- Living area
- Bedrooms
- Bathrooms
- Lot size
- Year built
- ZIP code

### Launch the Streamlit App

From the directory containing app.py, run:

`streamlit run app.py`

Streamlit will provide a local URL where the prediction application can be opened in a web browser.

---

## How to Run the Project

1. Clone the Repository
- Clone the project repository and navigate to the project directory.

2. Install Dependencies
- Install the Python libraries used by the project:

`pip install pandas numpy scikit-learn xgboost joblib streamlit jupyter`

3. Run the Notebooks

The notebooks should be completed in the following order:

01_exploration.ipynb
02_preprocessing.ipynb
03_baseline_model.ipynb
04_model_comparison.ipynb
05_advanced_models.ipynb
06_evaluation.ipynb

The notebooks progress from data exploration and preprocessing through model training, comparison, advanced modeling, and final evaluation.

