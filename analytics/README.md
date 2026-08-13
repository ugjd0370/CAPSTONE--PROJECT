# Titanic Analytics and Predictive Modeling

## Overview

This module implements an end-to-end Titanic analytics and machine-learning workflow. The dataset was loaded once using Seaborn's built-in Titanic loader and immediately saved as `titanic.csv` as the offline fallback. All subsequent analysis and modeling use this saved dataset and the same cleaning decisions.

## Dataset Loading

The raw dataset was loaded using:

```python
sns.load_dataset("titanic")
df.to_csv("titanic.csv", index=False)

Missing-Value Handling

Missing-value percentages were calculated for every affected column.

Column	Missing %	Strategy	Reason
age	19.87%	Median imputation	Between 5% and 30%
embarked	0.22%	Drop rows	Below 5%
deck	77.22%	Drop column	Very high missingness
embark_town	0.22%	Remove redundant column	Duplicates embarked information

The missing-value strategy follows the assignment's threshold rule. Columns with less than 5% missing values had their affected rows removed. Columns with 5%–30% missing values were imputed. deck had very high missingness, so it was dropped because reliable imputation would introduce substantial uncertainty.

UNIVARIETE ANALYSIS 

Histograms and box plots were produced for age and fare.

IQR analysis was performed using:

[Q1 - 1.5 × IQR, Q3 + 1.5 × IQR]
{'Q1': np.float64(22.0), 'Q3': np.float64(35.0), 'IQR': np.float64(13.0), 'lower_bound': np.float64(2.5), 'upper_bound': np.float64(54.5), 'outlier_count': 65}

FARE
{'Q1': np.float64(7.8958), 'Q3': np.float64(31.0), 'IQR': np.float64(23.1042), 'lower_bound': np.float64(-26.7605), 'upper_bound': np.float64(65.6563), 'outlier_count': 114


BIVARIATE ANALYSIS
Survival rates were calculated by:

1.sex
2.passenger class
3.sex and passenger class together

Boolean masking using & and | was also demonstrated.

CORRELATION ANALYSIS
The correlation matrix contains exactly:

1.survived
2.pclass
3.age
4.sibsp
5.parch
6.fare

The derived boolean columns adult_male and alone were intentionally excluded.
1.pclass and fare (-0.548193) : This is a very strong negative correlation. That is, as the class (pclass) traveled by passengers increases.
2.sibsp and parch (0.414542) : This is a positive correlation. Accordingly, those who traveled with siblings or spouses (sibsp) were more likely to travel as a family with their parents or children.

MULTIVARIATE DATA STORY

Four or more charts were produced to explain survival patterns:

1.Survival rate by sex
2.Survival rate by passenger class
3.Survival rate by sex and passenger class
4.Age distribution by survival

Each chart has an accompanying written interpretation.

Overall, the analysis shows that sex and passenger class were important factors associated with survival, while age provided additional predictive information.

STANDARDIZATION CHECK 

age and fare were standardized during EDA using the z-score transformation. The resulting variables had approximately zero mean and unit standard deviation.

This transformation was used only as an exploratory sanity check and was not used in the modeling pipeline.

TRAIN/TEST SPLIT 

The data was split into training and test sets using a stratified split. Stratification was used to preserve the survived/not-survived class proportions because the target classes were not perfectly balanced.

MODELLING PREPROCESSING

Preprocessing was implemented using ColumnTransformer and Pipeline.

Numerical features were processed using median imputation followed by StandardScaler.

Categorical features were processed using most-frequent imputation followed by OneHotEncoder.

All preprocessing was fitted only on the training data. The test data was transformed using the already-fitted preprocessing steps.

CLASSIFICATION MODELS
  
Three classifiers were trained on the same train/test split:

1.Logistic Regression
2.Decision Tree
3.Random Forest

Each model was evaluated using:

1.Accuracy
2.Precision
3.Recall
4.F1
5.ROC/AUC
6.Confusion matrix

The Decision Tree was also visualized using plot_tree.

IMBALANCE HANDLING

Three approaches were compared:

1.Baseline
2.class_weight="balanced"
3.SMOTE applied only to the training data

The strategies were compared using precision, recall and F1 score.
1.High Precision : If the model predicts someone will "survive", they should actually survive (fewer false positives).
2.High Recall : The model should detect all surviving passengers without missing a beat (low false negatives).

RANDOM FOREST HYPERPARAMETER TUNING 

GridSearchCV was used to tune:

1.n_estimators
2.max_depth
3.max_features

The Random Forest estimator was constructed with:
oob_score=True
Best parameters:
'classifier__max_depth': None, 
'classifier__max_features': 'sqrt',
 'classifier__n_estimators': 100

Best CV F1:
0.7481602702078536


REGRESSION SIDE TASK

A multivariate Linear Regression model was trained to predict fare using the other available features.

The reported metrics are:

1.MAE
2.RMSE
3.R²
4.Adjusted R²

A residual plot was produced to assess whether the residual variance appeared approximately constant or showed evidence of heteroscedasticity.

FINAL RECOMMENDATION

The final classifier recommendation is based primarily on the classification metrics, especially F1 and AUC, while considering the precision-recall trade-off.

The selected model achieved the strongest overall performance according to the reported evaluation metrics. The exact metric values are reported in the final comparison table in the notebook.

Classification metrics and regression metrics are presented as separate metric groups because they measure different prediction tasks and are not directly comparable.

