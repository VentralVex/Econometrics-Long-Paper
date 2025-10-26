import pandas as pd

# -------------------------
# 1. Load the three CSVs
# -------------------------
trained = pd.read_csv("/Users/aditpakala/Downloads/Econometrics/Econometrics Long Paper Data - Trained Teachers.csv")
secondary = pd.read_csv("/Users/aditpakala/Downloads/Econometrics/Econometrics Long Paper Data - Secondary Education Completion.csv")
gdp = pd.read_csv("/Users/aditpakala/Downloads/Econometrics/Econometrics Long Paper Data - GDP Per Capita.csv")

# -------------------------
# 2. Select only the needed columns
# -------------------------
trained = trained[['Entity', 'Year', 'se_sec_tcaq_up_zs']]
secondary = secondary[['Entity', 'Year', 'completion_rate__upper_secondary_education__both_sexes__pct__modelled_data__cr_mod_3']]
gdp = gdp[['Entity', 'Year', 'ny_gdp_pcap_pp_kd']]

# -------------------------
# 3. Merge datasets on Entity and Year
# -------------------------
merged = pd.merge(trained, secondary, on=['Entity', 'Year'], how='outer')
merged = pd.merge(merged, gdp, on=['Entity', 'Year'], how='outer')

# -------------------------
# 4. Keep only rows where all three target columns have data
# -------------------------
merged = merged.dropna(subset=[
    'se_sec_tcaq_up_zs', 
    'completion_rate__upper_secondary_education__both_sexes__pct__modelled_data__cr_mod_3', 
    'ny_gdp_pcap_pp_kd'
])

# -------------------------
# 5. Sort by Entity and Year
# -------------------------
merged = merged.sort_values(['Entity', 'Year']).reset_index(drop=True)

# -------------------------
# 6. Define OECD accession years
# -------------------------
oecd_years = {
    'Australia': 1961,
    'Austria': 1961,
    'Belgium': 1961,
    'Canada': 1961,
    'Chile': 2010,
    'Colombia': 2020,
    'Czech Republic': 1995,
    'Denmark': 1961,
    'Estonia': 2010,
    'Finland': 1969,
    'France': 1961,
    'Germany': 1961,
    'Greece': 1961,
    'Hungary': 1996,
    'Iceland': 1961,
    'Ireland': 1961,
    'Israel': 2010,
    'Italy': 1961,
    'Japan': 1964,
    'Korea': 1996,
    'Latvia': 2016,
    'Lithuania': 2018,
    'Luxembourg': 1961,
    'Mexico': 1994,
    'Netherlands': 1961,
    'New Zealand': 1973,
    'Norway': 1961,
    'Poland': 1996,
    'Portugal': 1961,
    'Slovakia': 2000,
    'Slovenia': 2010,
    'Spain': 1961,
    'Sweden': 1961,
    'Switzerland': 1961,
    'Turkey': 1961,
    'United Kingdom': 1961,
    'United States': 1961
}

# -------------------------
# 7. Create OECD dummy column
# -------------------------
def assign_oecd(row):
    join_year = oecd_years.get(row['Entity'], None)
    if join_year is not None and row['Year'] >= join_year:
        return 1
    else:
        return 0

merged['OECD'] = merged.apply(assign_oecd, axis=1)

# -------------------------
# 8. Inspect the data (optional)
# -------------------------
print(merged[['Entity', 'Year', 'OECD']].head(20))

# -------------------------
# 9. Save the cleaned merged dataset
# -------------------------
merged.to_csv("/Users/aditpakala/Downloads/Econometrics/Merged_Dataset_With_OECD.csv", index=False)
