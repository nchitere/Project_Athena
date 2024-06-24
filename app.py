#Import dependencies 
import pandas as pd 
import numpy as np 
import matplotlib.pyplot as plt 
import seaborn as sns 
import streamlit as st


# Load the datasets
kiva_loans = pd.read_csv('C:/Users/HerbertChitere/Downloads/Athena/kiva_loans.csv')


# Analytics

# Create a funding rate column 
kiva_loans['funding_rate'] = kiva_loans['funded_amount' ]/kiva_loans['loan_amount'] 
# Generate summary statistics for the funding rate column 
kiva_loans[['funding_rate']].describe() 



kiva_loans.columns

# Kiva reach and impact data processing
funding_rate = kiva_loans.groupby(['region','country','sector','borrower_genders', 'funded_time'])['funding_rate'].mean().reset_index()
funding_rate.head()

funding_rate.dtypes

kiva_loans['funded_time'] = pd.to_datetime(funding_rate['funded_time'])



# Kiva reach and impact data processing
funding_rate = kiva_loans.groupby(['region','country','sector','borrower_genders', 'funded_time'])['funding_rate'].mean().reset_index()
funding_rate.head()

# Sidebar for filtering
st.sidebar.title("Filter Data")
selected_country = st.sidebar.multiselect("Select Country", funding_rate['country'].unique())
selected_region = st.sidebar.multiselect("Select Region", funding_rate['region'].unique())
selected_sector = st.sidebar.multiselect("Select Sector", funding_rate['sector'].unique())
selected_gender = st.sidebar.multiselect("Select Gender", funding_rate['borrower_genders'].unique())
start_date = st.sidebar.date_input("Start Date", value=funding_rate['funded_time'].min())
end_date = st.sidebar.date_input("End Date", value=funding_rate['funded_time'].max())

# Sidebar for filtering
st.sidebar.title("Filter Data")

# Region filter
all_regions = funding_rate['region'].unique()
selected_region = st.sidebar.multiselect("Select Region", all_regions, default=all_regions)

# Country filter
all_countries = funding_rate['country'].unique()
selected_country = st.sidebar.multiselect("Select Country", all_countries, default=all_countries)

# Sector filter
all_sectors = funding_rate['sector'].unique()
selected_sector = st.sidebar.multiselect("Select Sector", all_sectors, default=all_sectors)

# Gender filter
all_genders = funding_rate['borrower_genders'].unique()
selected_gender = st.sidebar.multiselect("Select Gender", all_genders, default=all_genders)

# Date filter
start_date = st.sidebar.date_input("Start Date", value=funding_rate['funded_time'].min())
end_date = st.sidebar.date_input("End Date", value=funding_rate['funded_time'].max())

# Filter the data based on selections
filtered_data = funding_rate[(funding_rate['region'].isin(selected_region)) |
                           (funding_rate['country'].isin(selected_country)) |
                           (funding_rate['sector'].isin(selected_sector)) |
                           (funding_rate['borrower_genders'].isin(selected_gender)) |
                           (funding_rate['funded_time'].dt.date >= start_date) |
                           (funding_rate['funded_time'].dt.date <= end_date)]


# Calculate KPIs
total_loans = len(filtered_data)
total_funding = filtered_data['funding_rate'].sum()
avg_funding_rate = filtered_data['funding_rate'].mean()

# Display KPIs
st.title("Kiva Impact and Reach")
st.metric("Total Loans", total_loans)
st.metric("Total Funding", total_funding)
st.metric("Average Funding Rate", f"{avg_funding_rate:.2%}")



# Visualizations
st.subheader("Funding Rate by Time")
fig, ax = plt.subplots(figsize=(8, 4))
sns.lineplot(x='funded_time', y='funding_rate', data=filtered_data, ax=ax)
ax.set_xlabel("Time")
ax.set_ylabel("Funding Rate")
st.pyplot(fig)

st.subheader("Funding Rate by Sector")
fig, ax = plt.subplots(figsize=(8, 4))
sns.barplot(x='sector', y='funding_rate', data=filtered_data, ax=ax)
ax.set_xlabel("Sector")
ax.set_ylabel("Funding Rate")
ax.tick_params(axis='x', rotation=90)
st.pyplot(fig)

st.subheader("Funding Rate by Region and Country")
fig, ax = plt.subplots(figsize=(8, 4))
sns.barplot(x='region', y='funding_rate', data=filtered_data, ax=ax)
ax.set_xlabel("Region")
ax.set_ylabel("Funding Rate")
ax.tick_params(axis='x', rotation=90)
st.pyplot(fig)

st.subheader("Funding Rate by Gender")
fig, ax = plt.subplots(figsize=(8, 4))
sns.barplot(x='borrower_genders', y='funding_rate', data=filtered_data, ax=ax)
ax.set_xlabel("Gender")
ax.set_ylabel("Funding Rate")
st.pyplot(fig)