# Analytics of Home Mortgage Disclosure Act (HMDA) Mortgage Dataset (New York State, 2024)

## Instructions
### Step 1: Data Cleaning
1. Unzip `data.zip` and load `state_NY.zip` to local folder
2. Run `data_cleaning.py` or use `data_cleaning.ipynb` in Jupyter Notebook
    * For the reason of cleaning data this way, check out `HMDA_NY_2024_data_overview.pdf`
    * We removed all features with too many rows of missing data or not relevant to our study.
    * For the remaining features, we have removed empty data.
3. You will have cleaned data as `hmda_ny_2024_cleaned_data.csv`

## Data Sources
* [Official data download link](https://ffiec.cfpb.gov/data-browser/data/2024?category=states)
* [Official data fields explanation](https://ffiec.cfpb.gov/documentation/publications/loan-level-datasets/lar-data-fields)
* Original and cleaned dataset (CSV) under `hmda_ny_2024_data.zip`