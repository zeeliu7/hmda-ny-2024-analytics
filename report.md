# Analytics of Home Mortgage Disclosure Act (HMDA) Mortgage Dataset (New York State, 2024)

## Introduction and dataset description

The Home Mortgage Disclosure Act (HMDA) is a U.S. official dataset that provides comprehensive information regarding the U.S. housing mortgage market, disclosed by many financial institutions [(Source)](https://www.consumerfinance.gov/data-research/hmda/). In this project, we have analyzed the many characteristics that could affect loan application results, using the data for New York State over the year of 2024.

## Data acquisition methodology

The dataset was downloaded from the [HMDA data browser](https://ffiec.cfpb.gov/data-browser/data/2024?category=states) with New York State and year 2024 selected. The original dataset included 383,577 rows and 99 columns.

## Cleaning and preprocessing steps

We referred to the explanation of data for each field according to [Public HMDA - LAR Data Fields](https://ffiec.cfpb.gov/documentation/publications/loan-level-datasets/lar-data-fields).

For how we have treated each of the 99 columns, including the selected data dropping and remapping, please refer to [Placeholder](www.example.com).

### Dropping features

20 features were dropped initially due to the following reasons:

| Reason | Number of Affected Features | Example |
|:------:|:---------------------------:|:-------:|
| Identification number or shared feature | 5 | `activity_year` |
| Minimal contribution to analysis | 4 | `applicant_credit_score_type` |
| Too many missing values | 11 | `total_points_and_fees` |

### Exempt data removal

For the remaining features, many data included exempt categories that would not benefit our analysis. As a result, we removed rows that includes exempt data.

Example:

```
loan_purpose
Values:
1 - Home purchase
2 - Home improvement
31 - Refinancing
32 - Cash-out refinancing
4 - Other purpose
5 - Not applicable
```

Code:
```python
df = df[~df['loan_purpose'].astype(str).isin(['5'])]
```

### Relabelling

For categorical features, the original data usually included a numerical code, and we converted them to readable format and better for further one-hot encoding column naming. For data initially as text, we have refined the text by replacing non-alphanumerical characters to underline for a more machine-friendly format.

Example:

```python
df['action_taken'] = df['action_taken'].astype(str).map({
    "1": "Loan_originated",
    "2": "Application_approved_but_not_accepted",
    "3": "Application_denied",
    "4": "Application_withdrawn_by_applicant",
    "5": "File_closed_for_incompleteness",
    "6": "Purchased_loan",
    "7": "Preapproval_request_denied",
    "8": "Preapproval_request_approved_but_not_accepted"
})
```

### Boolean conversion

Certain categories were categorical but only with two categories each. We have converted the data into boolean. This was helpful for filtering since boolean checking is faster than string matching.

Example:

```
Before:
preapproval
1 - Preapproval requested
2 - Preapproval not requested

After:
preapproval_requested (True/False)
```

### From combined feature to one-hot encoding

A couple features were initially in a combined format. The following is an example, and the original dataset included `applicant_ethnicity-1` through `applicant_ethnicity-5`:

```
applicant_ethnicity-1
1 - Hispanic or Latino
11 - Mexican
12 - Puerto Rican
13 - Cuban
14 - Other Hispanic or Latino
2 - Not Hispanic or Latino
3 - Information not provided by applicant in mail, internet, or telephone application
4 - Not applicable
```

We collected the appearance of any category listed and converted them to a boolean feature, such as `applicant_ethnicity_is_Mexican` (True/False). For example, if an applicant has selected 1, 11, and 12, the row of data will set the related three columns to True. This one-hot encoding of ethnicity ensures high machine performance over combined data.

### End result

The final dataset included 216,635 rows and 123 columns.

## Exploratory Data Analysis (EDA)

The Exploratory Data Analysis begins with an examination of the core financial variables to understand their statistical properties, distributional shapes, and potential implications for downstream modeling. The dataset contains 216,635 observations and 123 variables, providing a sufficiently large sample to derive reliable statistical insights while also increading the likelihood of extreme values and structural irregularities. 

### 1) Core Financial Variables Distribution
[Loan Amount Distribution(raw)](figures/loan_amount_distribution_raw.png)


## Feature engineering process and justification

We divided feature engineering into two parts. The first part focuses on basic feature transformations and binary normalization. The second part involves creating additional columns that may be useful for later analysis. 

### 1) Basic feature transformations 
After reviewing the cleaned dataset, We found that many variables were stored as boolean values (True/False), similar to “denial_reason_is_Debt-to-income_ratio.” Therefore, these boolean indicators were first converted into a standardized binary format (0/1). A large number of missing values (NaN) was also observed in categorical variables related to co-applicants. By cross-checking with other co-applicant fields (e.g cases where co_applicant_age = 9999 indicates no co-applicant), it was validated that blanks in these co-applicant category fields are more consistent with the presence of a co-applicant whose demographic information is missing, rather than the absence of a co-applicant. Therefore, a new binary indicator variable was constructed to identify whether an application includes a co-applicant.

Secondly, we created a binary approval indicator  to distinguish applications that resulted in an originated loan from those that did not. Applications that were approved but not accepted were treated as not approved, since no loan was ultimately issued. This definition helps ensure consistency in downstream analysis. Moreover, we encoded Several variables with predefined categories. For example, loan_type contains only four categories, the race/ethnicity fields for the applicant and co-applicant use fixed category codes, and applicant age is already provided in grouped ranges. Encoding these categorical features (one-hot encoding) makes it easier to examine whether demographic and product-related attributes are associated with application outcomes.

### 2) Create additional useful columns
First, we applied KNN imputation to fill missing values in variables such as loan_to_value_ratio, interest_rate, rate_spread, and property_value to support subsequent calculations. In contrast, loan_term typically takes discrete integer values (e.g., 360 or 180), with 360 dominating the distribution. Because KNN imputation could produce unrealistic intermediate values for this discrete feature, it is not appropriate for filling missing loan terms. Instead, mode imputation is a more suitable choice.

example for loan type:
```
loan_type
Conventional             195259
FHA_insured               16469
VA_guaranteed              4608
RHS_or_FSA_guaranteed       299
Name: count, dtype: int64
```
Then, we construct important financial indicators such as loan to income (Loan Amount/Income), equity (Property Value − Loan Amount), and equity_ratio (Equity/Property Value) for subsequent analysis.
formulat:
```
P * r * (1 + r)**n / ((1 + r)**n - 1)
```
Since an individual’s deviation from local market conditions may also be informative, we created three county-relative features: interest_rate_minus_county_median (whether the interest rate is above the county median), property_value_minus_county_median (whether the property value is above the county median), and income_minus_county_median (whether income is above the county median). These variables capture how each application compares to the typical level in its local market and support scenario-based analysis.Finally, we calculate the z-score for all values to facilitate computation.

## Summary of key findings

## Challenges faced and future recommendations

### Data pre-processing

While it may be storage-efficient to store categorical data as numbers, it would be highly inefficient for using the last number as "Exempt". For example, if a feature had 5 categories labelled 1 through 5, the exempt category was labelled as "5". This means that in order to remove exempt data, the data cleaner need to read over the documentation in order to find the code representing exempt. It was nice to notice how certain features used universal code to represent exempt (e.g. 1111, 8888) but those were not universal even within the same dataset. It would be recommended as universal practice to use an unified code (e.g. 0) to represent exempt so data cleaners would directly drop exempt data. 

## Link to your GitHub repository

[Placeholder](www.example.com)

## Each member’s contribution to the project
* **Jason Zhao** Zhao was primarily responsible for data transformation and aggregation in the feature engineering section. Zhao normalized key variables, encoded categorical features, and extracted important indicators for subsequent analysis. For example, Zhao constructed columns to identify whether an application had co-applicants and whether the loan was ultimately approved. Finally, Zhao was also responsible for performing KNN imputation on data used for calculations, such as Interest_rate.
* **Zhonghao Liu** proposed and downloaded the HMDA dataset. Furthermore, Liu analyzed the data distribution and appearance of NaN/Exempt data for each feature, which was outlined in `HMDA_NY_2024_data_overview.pdf`. Furthermore, Liu has coded the "Data Cleaning and Handling Inconsistencies" of the project, including removing irrelevant features, selectively dropping NA/exempt data, relabelling categorical data for one-hot encoding, and doing preparation work for the rest of the team (e.g. filling in empty entries using KNN).