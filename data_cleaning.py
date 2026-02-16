#!/usr/bin/env python
# coding: utf-8

# In[1]:


# Data source: https://ffiec.cfpb.gov/data-browser/data/2024?category=states
# Data fields: https://ffiec.cfpb.gov/documentation/publications/loan-level-datasets/lar-data-fields


# In[2]:


import pandas as pd
import numpy as np
df = pd.read_csv('state_NY.csv', dtype=str)


# In[3]:


print(df.shape)


# In[4]:


df = df.drop(['activity_year', 'lei', 'derived_msa-md', 'state_code', 'census_tract', 'total_loan_costs', 
              'total_points_and_fees','origination_charges', 'discount_points', 'lender_credits', 
              'prepayment_penalty_term', 'intro_rate_period', 'multifamily_affordable_units', 
              'applicant_credit_score_type', 'co-applicant_credit_score_type', 'submission_of_application',
              'initially_payable_to_institution', 'hoepa_status', 'manufactured_home_secured_property_type', 
              'manufactured_home_land_property_interest'], axis=1)


# In[5]:


print(df.shape)


# In[6]:


df = df[~df['derived_ethnicity'].isin(['Ethnicity Not Available'])]
print("After cleaning derived_ethnicity")
print(df.shape)

df = df[~df['derived_race'].isin(['Race Not Available'])]
print("After cleaning derived_race")
print(df.shape)

df = df[~df['derived_sex'].isin(['Sex Not Available'])]
print("After cleaning derived_sex")
print(df.shape)

df = df[~df['loan_purpose'].astype(str).isin(['5'])]
print("After cleaning loan_purpose")
print(df.shape)

df = df[~df['applicant_age'].astype(str).isin(['8888'])]
print("After cleaning applicant_age")
print(df.shape)

df = df[~df['co-applicant_age'].astype(str).isin(['8888'])]
print("After cleaning co-applicant_age")
print(df.shape)


# In[7]:


columns_require_1111_cleaning = ['reverse_mortgage', 'open-end_line_of_credit', 'business_or_commercial_purpose']
columns_require_1111_cleaning.extend([f'aus-{i}' for i in range(1, 6)])
columns_require_1111_cleaning.extend([f'denial_reason-{i}' for i in range(1, 5)])
for col in columns_require_1111_cleaning:
    df = df[~df[col].astype(str).isin(['1111'])]
print(df.shape)


# In[8]:


columns_require_exempt_cleaning = ['loan_to_value_ratio', 'interest_rate', 'rate_spread', 'loan_term', 
                                   'property_value', 'debt_to_income_ratio']
for col in columns_require_exempt_cleaning:
    df = df[~df[col].astype(str).isin(['Exempt'])]
print(df.shape)


# In[9]:


# source: https://en.wikipedia.org/wiki/List_of_counties_in_New_York

df['county_code'] = df['county_code'].astype(str).map({
    "36001": "Albany",
    "36003": "Allegany",
    "36005": "Bronx",
    "36007": "Broome",
    "36009": "Cattaraugus",
    "36011": "Cayuga",
    "36013": "Chautauqua",
    "36015": "Chemung",
    "36017": "Chenango",
    "36019": "Clinton",
    "36021": "Columbia",
    "36023": "Cortland",
    "36025": "Delaware",
    "36027": "Dutchess",
    "36029": "Erie",
    "36031": "Essex",
    "36033": "Franklin",
    "36035": "Fulton",
    "36037": "Genesee",
    "36039": "Greene",
    "36041": "Hamilton",
    "36043": "Herkimer",
    "36045": "Jefferson",
    "36047": "Kings",
    "36049": "Lewis",
    "36051": "Livingston",
    "36053": "Madison",
    "36055": "Monroe",
    "36057": "Montgomery",
    "36059": "Nassau",
    "36061": "New_York",
    "36063": "Niagara",
    "36065": "Oneida",
    "36067": "Onondaga",
    "36069": "Ontario",
    "36071": "Orange",
    "36073": "Orleans",
    "36075": "Oswego",
    "36077": "Otsego",
    "36079": "Putnam",
    "36081": "Queens",
    "36083": "Rensselaer",
    "36085": "Richmond",
    "36087": "Rockland",
    "36089": "St_Lawrence",
    "36091": "Saratoga",
    "36093": "Schenectady",
    "36095": "Schoharie",
    "36097": "Schuyler",
    "36099": "Seneca",
    "36101": "Steuben",
    "36103": "Suffolk",
    "36105": "Sullivan",
    "36107": "Tioga",
    "36109": "Tompkins",
    "36111": "Ulster",
    "36113": "Warren",
    "36115": "Washington",
    "36117": "Wayne",
    "36119": "Westchester",
    "36121": "Wyoming",
    "36123": "Yates"
})


# In[10]:


df['conforming_loan_limit'] = df['conforming_loan_limit'].map({
    "C": "Conforming",
    "NC": "Nonconforming",
    "U": "Undetermined"
})


# In[11]:


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


# In[12]:


df['purchaser_type'] = df['purchaser_type'].astype(str).map({
    "0": "Not_applicable",
    "1": "Fannie_Mae",
    "2": "Ginnie_Mae",
    "3": "Freddie_Mac",
    "4": "Farmer_Mac",
    "5": "Private_securitizer",
    "6": "Commercial_bank_or_savings_bank_or_savings_association",
    "71": "Credit_union_or_mortgage_company_or_finance_company",
    "72": "Life_insurance_company",
    "8": "Affiliate_institution",
    "9": "Other_type_of_purchaser"
})


# In[13]:


df['loan_type'] = df['loan_type'].astype(str).map({
    "1": "Conventional",
    "2": "FHA_insured",
    "3": "VA_guaranteed",
    "4": "RHS_or_FSA_guaranteed"
})


# In[14]:


df['occupancy_type'] = df['occupancy_type'].astype(str).map({
    "1": "Principal_residence",
    "2": "Second_residence",
    "3": "Investment_property"
})


# In[15]:


df['applicant_sex'] = df['applicant_sex'].astype(str).map({
    "1": "Male",
    "2": "Female",
    "3": "Not_provided",
    "4": "Not_applicable",
    "6": "Both_selected"
})

df['co-applicant_sex'] = df['co-applicant_sex'].astype(str).map({
    "1": "Male",
    "2": "Female",
    "3": "Not_provided",
    "4": "Not_applicable",
    "5": "No_co-applicant",
    "6": "Both_selected"
})


# In[16]:


df['applicant_ethnicity_observed'] = df['applicant_ethnicity_observed'].astype(str).map({
    "1": True,
    "2": False,
    "3": np.nan
})

df['co-applicant_ethnicity_observed'] = df['co-applicant_ethnicity_observed'].astype(str).map({
    "1": True,
    "2": False,
    "3": np.nan,
    "4": "no_co-applicant"
})

df['applicant_race_observed'] = df['applicant_race_observed'].astype(str).map({
    "1": True,
    "2": False,
    "3": np.nan
})

df['co-applicant_race_observed'] = df['co-applicant_race_observed'].astype(str).map({
    "1": True,
    "2": False,
    "3": np.nan,
    "4": "no_co-applicant"
})

df['applicant_sex_observed'] = df['applicant_sex_observed'].astype(str).map({
    "1": True,
    "2": False,
    "3": np.nan
})

df['co-applicant_sex_observed'] = df['co-applicant_sex_observed'].astype(str).map({
    "1": True,
    "2": False,
    "3": np.nan,
    "4": "no_co-applicant"
})


# In[17]:


def convert_to_boolean_and_drop(df, conversions_list):
    for new_col, original_col, value_for_true in conversions_list:
        df[new_col] = (df[original_col].astype(str) == value_for_true)
        df = df.drop(original_col, axis=1)
    return df

boolean_conversions = [
    ('preapproval_requested', 'preapproval', '1'),
    ('secured_by_a_first_lien', 'lien_status', '1'),
    ('is_reverse_mortgage', 'reverse_mortgage', '1'),
    ('is_open-end_line_of_credit', 'open-end_line_of_credit', '1'),
    ('primarily_for_a_business_or_commercial_purpose', 'business_or_commercial_purpose', '1'),
    ('includes_negative_amortization', 'negative_amortization', '1'),
    ('includes_interest_only_payment', 'interest_only_payment', '1'),
    ('includes_balloon_payment', 'balloon_payment', '1'),
    ('includes_other_nonamortizing_features', 'other_nonamortizing_features', '1'),
    ('is_site_built', 'construction_method', '1')
]
df = convert_to_boolean_and_drop(df, boolean_conversions)
print(df.shape)


# In[18]:


columns_require_regex_cleaning = ['derived_loan_product_type', 'derived_dwelling_category', 'derived_ethnicity', 
                                  'derived_race', 'derived_sex']
for col in columns_require_regex_cleaning:
    df[col] = df[col].str.replace(r'[^a-zA-Z0-9\-_]', '_', regex=True)


# In[19]:


df['total_units'] = df['total_units'].replace({">149": "over_149"})


# In[20]:


df['debt_to_income_ratio'] = df['debt_to_income_ratio'].replace({'>60%': 'over_60_percent', '<20%': "below_20_percent"})
df['debt_to_income_ratio'] = df['debt_to_income_ratio'].replace(r'%', '_percent', regex=True)


# In[21]:


df['applicant_age'] = df['applicant_age'].replace({'<25': 'below_25', '>74': "above_74"})
df['co-applicant_age'] = df['co-applicant_age'].replace({'<25': 'below_25', '>74': "above_74"})


# In[22]:


ethnicity_map = {
    '1': 'Hispanic_or_Latino',
    '11': 'Mexican',
    '12': 'Puerto_Rican',
    '13': 'Cuban',
    '14': 'Other_Hispanic_or_Latino',
    '2': 'Not_Hispanic_or_Latino',
    '3': 'Not_provided',
    '4': 'Not_applicable',
    '5': "No_co-applicant"
}

applicant_ethnicity_cols = [f'applicant_ethnicity-{i}' for i in range(1, 6)]

df[applicant_ethnicity_cols] = df[applicant_ethnicity_cols].astype(str)

for code, category in ethnicity_map.items():
    col_name = f'applicant_ethnicity_is_{category}'
    df[col_name] = df[applicant_ethnicity_cols].isin([code]).any(axis=1)

df = df.drop(applicant_ethnicity_cols, axis=1)

co_applicant_ethnicity_cols = [f'co-applicant_ethnicity-{i}' for i in range(1, 6)]

df[co_applicant_ethnicity_cols] = df[co_applicant_ethnicity_cols].astype(str)

for code, category in ethnicity_map.items():
    col_name = f'co-applicant_ethnicity_is_{category}'
    df[col_name] = df[co_applicant_ethnicity_cols].isin([code]).any(axis=1)

df = df.drop(co_applicant_ethnicity_cols, axis=1)
print(df.shape)


# In[23]:


race_map = {
    '1': 'American_Indian_or_Alaska_Native',
    '2': 'Asian',
    '21': 'Asian_Indian',
    '22': 'Chinese',
    '23': 'Filipino',
    '24': 'Japanese',
    '25': 'Korean',
    '26': 'Vietnamese',
    '27': 'Other_Asian',
    '3': 'Black_or_African_American',
    '4': 'Native_Hawaiian_or_Other_Pacific_Islander',
    '41': 'Native_Hawaiian',
    '42': 'Guamanian_or_Chamorro',
    '43': 'Samoan',
    '44': 'Other_Pacific_Islander',
    '5': 'White',
    '6': 'Not_provided',
    '7': 'Not_applicable',
    '8': 'No_co-applicant'
}

applicant_race_cols = [f'applicant_race-{i}' for i in range(1, 6)]

df[applicant_race_cols] = df[applicant_race_cols].astype(str)

for code, category in race_map.items():
    col_name = f'applicant_race_is_{category}'
    df[col_name] = df[applicant_race_cols].isin([code]).any(axis=1)

df = df.drop(applicant_race_cols, axis=1)

co_applicant_race_cols = [f'co-applicant_race-{i}' for i in range(1, 6)]

df[co_applicant_race_cols] = df[co_applicant_race_cols].astype(str)

for code, category in race_map.items():
    col_name = f'co-applicant_race_is_{category}'
    df[col_name] = df[co_applicant_race_cols].isin([code]).any(axis=1)

df = df.drop(co_applicant_race_cols, axis=1)

print(df.shape)


# In[24]:


aus_map = {
    '1': 'DU',
    '2': 'LP_or_Loan_Product_Advisor',
    '3': 'TOTAL_scorecard',
    '4': 'GUS',
    '5': 'Other',
    '6': 'Not_applicable',
    '7': 'Internal Proprietary System'
}

aus_rows = [f'aus-{i}' for i in range(1, 6)]

df[aus_rows] = df[aus_rows].astype(str)

for code, category in aus_map.items():
    col_name = f'aus_is_{category}'
    df[col_name] = df[aus_rows].isin([code]).any(axis=1)

df = df.drop(aus_rows, axis=1)

print(df.shape)


# In[25]:


denial_reason_map = {
    '1': 'Debt-to-income_ratio',
    '2': 'Employment_history',
    '3': 'Credit_history',
    '4': 'Collateral',
    '5': 'Insufficient_cash',
    '6': 'Unverifiable_information',
    '7': 'Credit_application_incomplete',
    '8': 'Mortgage_insurance_denied',
    '9': 'Other',
    '10': 'Not_applicable'
}

denial_reason_rows = [f'denial_reason-{i}' for i in range(1, 5)]

df[denial_reason_rows] = df[denial_reason_rows].astype(str)

for code, category in denial_reason_map.items():
    col_name = f'denial_reason_is_{category}'
    df[col_name] = df[denial_reason_rows].isin([code]).any(axis=1)

df = df.drop(denial_reason_rows, axis=1)

print(df.shape)


# In[26]:


print(df.head())


# In[27]:


df = df.dropna(subset=['county_code', 'conforming_loan_limit', 'income', 'debt_to_income_ratio', 'applicant_age', 
                       'co-applicant_age'])


# In[28]:


print(df.shape)


# In[29]:


print(df.head())


# In[30]:


df.to_csv('hmda_ny_2024_cleaned_data.csv', index=False)

