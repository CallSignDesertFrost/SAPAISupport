import requests
from bs4 import BeautifulSoup
import pandas as pd
from sklearn.linear_model import LinearRegression
from sqlalchemy import create_engine

# Replace 'YOUR_SAP_API_KEY' and 'SAP_API_ENDPOINT' with your actual SAP API key and endpoint
headers = {
    'Authorization': 'Bearer YOUR_SAP_API_KEY',
    'Content-Type': 'application/json'
}

# Example: Fetch procurement data from SAP API
procurement_api_endpoint = 'SAP_API_ENDPOINT/procurement_data'
response_procurement = requests.get(procurement_api_endpoint, headers=headers)

# Check if the request was successful (status code 200)
if response_procurement.status_code == 200:
    procurement_data = response_procurement.json()
else:
    print(f"Error - Procurement Data: {response_procurement.status_code}")
    procurement_data = None

# Example: Web scraping for retailer prices (replace 'RETAILER_URL' with the actual retailer URL)
retailer_url = 'RETAILER_URL'
retailer_page = requests.get(retailer_url)
soup = BeautifulSoup(retailer_page.content, 'html.parser')

# Extracting prices (replace 'price_selector' with the actual HTML selector for prices)
prices = soup.select('price_selector')

# Assume we have a list of procurement prices and retailer prices
procurement_prices = [10, 15, 20, 25, 30]
retailer_prices = [8, 14, 18, 24, 28]

# Create a DataFrame for comparison
comparison_df = pd.DataFrame({
    'ProcurementPrice': procurement_prices,
    'RetailerPrice': retailer_prices
})

# Calculate price differences
comparison_df['PriceDifference'] = comparison_df['ProcurementPrice'] - comparison_df['RetailerPrice']

# Save data to an SQLite database
engine = create_engine('sqlite:///procurement_and_comparison_data.db')
comparison_df.to_sql('procurement_and_comparison_data', con=engine, index=False, if_exists='replace')

# Linear Regression for Profit Margin Estimation
X = comparison_df[['ProcurementPrice']]
y = comparison_df['RetailerPrice']

model = LinearRegression().fit(X, y)

# Predicting profit margin for a new procurement price
new_procurement_price = 22
predicted_retailer_price = model.predict([[new_procurement_price]])

profit_margin = (predicted_retailer_price - new_procurement_price) / new_procurement_price * 100

print(f"Predicted Retailer Price: {predicted_retailer_price[0]}")
print(f"Estimated Profit Margin: {profit_margin:.2f}%")
