# IDXExchange Project

## Objectives:
Upon downloading datasets on real estate properties sourced from CRMLS (California Regional Multiple Listing Service), the goal is to build and train a machine learning model to predict ClosePrice, the price of any single residential property in California.

## Weekly Milestones & Progress

### Week 1:
*Goals*
- Download atleast 6 months of raw CSV data from CRMLS
- Review MetaData to understand important data features and key columns

---

### Week 2:
*Goals*
- Load 6 months of dataset into jupyter notebook using pandas
- Explore the distributions of key columns: ClosePrice, LivingArea, Bedrooms, Bathrooms, LotSize
- Restrict to PropertyType = Residential and PropertySubType = SingleFamilyResidence

*Results*
- Close Price: most houses are sold between $750k to $900k, with outliers existing above $3M
- Living Area: most houses have around 1,500 to 2,000 square footage of living area
- Bedrooms: most houses have 3-4 bedrooms
- Bathrooms: most houses have 2-3 bathrooms
- Lot Size: most houses have a lot size of around 10k to 15k square footage

---

### Week 3:
*Goals*
- Handle missing values (decide whether to drop, impute, or flag).
- Convert categorical fields to numeric (encoding).
- Normalize numerical features if needed.
- Create train/test split

*Results*
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
         
- #### Observed that PostalCode and City had strong influence on ClosePrice:
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

### Week 4:
*Goals*
- Train a Linear Regression as the first model. 
- Evaluate using R² on the test set. 
- Record baseline results. 

*Results*
- Linear Regression Results: 
    - Training R²: 0.7778
    - Test R²: 0.7611
 
- The model had an R² score of 0.7611 on the test set, indicating that it explains approximately 76% of the variation in home sale prices. Both R² results are similar to each other with a difference of 0.0167 representing that the model is generalizing well without overfitting.

---

### Week 5:
*Goals*
- Try Decision Tree and Random Forest regressors. 
- Compare their test R² against baseline.
- Document model behavior (strengths/weaknesses). 

*Results*
- *Best Performing Model* - Random Forest Model
    - Builds multiple trees on various data subsets and features rather than memorizing patterns

- *Most Stable Model* - Linear Regression Model

- *Weaker Generalization Model* - Decision Tree Model:
    - Memorizes patterns on training data which doesn't generalize well to the test data

| Model | Train R² | Test R² | R² Difference | Strengths | Weaknesses |
| -------- | -------- | -------- | -------- | -------- | -------- |
| Random Forest Regressor | 0.978122  | 0.836335  | 0.141787  | Highest accuracy, captures complex relationships  | Slower training, harder to interpret  |
| Linear Regression  | 0.777826  | 0.761132  | 0.016694  | Stable, simple and fast  | Struggles to capture nonlinear patterns  |
| Decision Tree Regressor  | 0.998748  | 0.710998  | 0.28775  | Captures nonlinear patterns  | Overfits easily, unstable  |

---

### Week 6:
*Goals*
- Add more sample features you can engineer: bed/bath ratio, age of property in years 
- Add more detailed geographic layer using school districts
- Re-train models with the updated feature set. 

*Results*

| Model | Old Test R² | New Test R² | Improvement |
| -------- | -------- | -------- | -------- |
| Random Forest Regressor | 0.836335  | 0.865858  | 0.029523  |
| Linear Regression  | 0.761132  | 0.799203  | 0.038071  |
| Decision Tree Regressor  | 0.710998  | 0.744029  | 0.033031  |

##### Old Features
- `LivingArea`, `BedroomsTotal`, `BathroomsTotalInteger`, `LotSizeSquareFeet`, `zip_median_price`, `city_median_price`

##### New Features
- `property_age`: years since property was built (2026 - YearBuilt)
- `bed_bath_ratio`: bedrooms divided by bathrooms
- `district_median_price`: median ClosePrice per Unified School District

##### Conclusion

- All the models had improvement with the new feature set
    - Most Improvement: Linear Regression had the largest improvement of 0.038
    - Top Performing Model: Random Forest had the best Test R² score of 0.865858
- Creating the school district spatial layer (`district_median_price`) provided a tighter price baseline than ZIP codes and city medians alone, improving test accuracy across the models.
- Adding features like `bed_bath_ratio` and `property_age` helped models account for property condition and layout efficiency increasing model accuracy.
  
---

### Week 7:
*Goals*
- Try Gradient Boosting (e.g., XGBoost or LightGBM).
- Perform light hyperparameter tuning (depth, learning rate, n_estimators). 

*Results*

| Model | Test R² |
| -------- | -------- |
| Linear Regression | 0.799203  |
| Decision Tree  | 0.744029  |
| Random Forest  | 0.865858  |
| Baseline XGBoost  | 0.868322  |
| Tuned XGBoost  | 0.872436  |

- Baseline XGBoost Test R² : 0.868322
- Tuned XGBoost Test R² : 0.872436
    - Best hyperparameters: `n_estimators=300`, `learning_rate=0.10`, and `max_depth=9`
        - Larger max_depth allows the model to capture complex relationships
    - Increase of 0.004114 over baseline XGBoost
  
---

### Week 8:
*Goals*
- Compute metrics beyond R²: MAPE and MdAPE.
- Summarize insights (e.g., which price bands perform better). 

*Results*

| Price Band | Count | RF MAPE% | DT MAPE% | LR MAPE% | XGB MAPE% | RF MdAPE% | DT MdAPE% | LR MdAPE% | XGB MdAPE% |
| -------- | -------- | -------- | -------- | -------- | -------- | -------- | -------- | -------- | -------- |
| Under $500k | 1809 | 20.62 | 24.95 | 44.91 | 20.62 | 9.22 | 12.63 | 35.40 | 9.64 |
| $500k-$1M | 5327 | 11.05 | 14.73 | 23.82 | 10.64 | 6.85 | 9.15 | 18.68 | 6.98 |
| $1M-$2M | 3946 | 13.55 | 19.52 | 18.19 | 12.92 | 9.94 | 13.98 | 13.48 | 9.52 |
| Over $2M | 1702 | 17.77 | 24.71 | 19.88 | 17.27 | 14.46 | 20.00 | 16.69 | 13.76 |


- **$500K–$1M** had the lowest prediction errors across all models
- Error increases at both extremes — under $500K due to fewer 
  training examples, over $2M due to unique luxury features 
  not captured in MLS data
- XGBoost consistently had the lowest MAPE across all price bands;
  Random Forest had a slightly lower MdAPE in the under $500K band

1. **XGBoost** — Best overall
    - Lowest MAPE (10.64%) and MdAPE (6.98%) in the $500K–$1M band
    - Most consistent performance across all price tiers

2. **Random Forest** — Close second
    - Slightly better MdAPE in the under $500K band 
      (9.22% vs XGBoost 9.64%)

3. **Decision Tree** — High variance
    - Most unstable across price bands 
      (MAPE ranges from 14.73% to 24.95%)

4. **Linear Regression** — Weakest overall
    - Struggles most under $500K (MAPE: 44.91%, MdAPE: 35.40%)
    - Becomes more competitive above $1M
  
---

### Week 9:
*Goals*
- Build a Streamlit app: user inputs LivingArea, Beds, Baths, LotSize → output predicted price. 
- Load trained model with joblib/pickle.

*Results*
Built a Streamlit prediction app (`app.py`) using the tuned XGBoost model loaded in with joblib. The app takes user inputs and engineers features automatically (PropertyAge, BedBathRatio) before running the model.

- To run app use command `streamlit run app.py` in terminal

#### Test Cases from April 2026 Test Dataset:

| | Test Case 1 | Test Case 2 | Test Case 3 |
|---|---|---|---|
| **Tier** | Under $500K | $500K–$1M | Over $1M |
| **Address** | 24860 4th, San Bernardino | 2089 Palm Beach Way, San Jose | 35 Malibu, Laguna Niguel |
| **Living Area** | 456 sq ft | 1,020 sq ft | 2,629 sq ft |
| **Beds / Baths** | 1 / 1 | 3 / 2 | 4 / 3 |
| **Lot Size** | 11,000 sq ft | 5,200 sq ft | 9,100 sq ft |
| **Year Built** | 1930 | 1960 | 1987 |
| **ZIP Code** | 92410 | 95122 | 92677 |
| **Actual Price** | $245,000 | $851,000 | $2,250,000 |
| **Predicted Price** | $276,695 | $$851,047 | $2,144,243 |
