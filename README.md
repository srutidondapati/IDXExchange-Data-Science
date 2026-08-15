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
    - Training set contains data from September 2025 - March 2026
    - Test set contains data from April 2026
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
| Under $500k | 1809 | 20.62 | 25.51 | 44.91 | 20.62 | 9.22 | 12.68 | 35.40 | 9.64 |
| $500k-$1M | 5327 | 11.05 | 14.79 | 23.82 | 10.64 | 6.85 | 8.97 | 18.68 | 6.98 |
| Over $1M | 5648 | 14.83 | 21.14 | 18.70 | 14.23 | 11.16 | 15.43 | 14.42 | 10.57 |


- $500k-$1M price band had the lowest prediction errors
- Homes under $500k and $1M had higher errors, meaning these properties were more difficult for the models to predict
- XGBoost had the lowest MAPE for the $500k–$1M and over-$1M bands; while Random Forest had a slightly lower MdAPE for the under-$500k band

1. XGBoost:
    - Best performance with 10.64% MAPE and 6.98% MdAPE for the $500k - $1M band
2. Random Forest:
    - Slightly better in the lowest price band with MdAPE of 9.22% compared to XGBoost 9.64%
3. Decision Tree:
    - High variance and instability across the price bands (25.51% in under $500k vs 21.14% in over $1M)
4. Linear Regression:
    - Poor performance across price bands with high MAPE (44.91%) and MdAPE (35.40%) scores
