import pandas as pd
import time
from geopy.geocoders import Nominatim
from geopy.extra.rate_limiter import RateLimiter

# Set up the Nominatim geocoder
geolocator = Nominatim(user_agent="myGeocoder", timeout=10)
geocode = RateLimiter(geolocator.geocode, min_delay_seconds=2, max_retries=5)

# Load the store data from the provided Excel file with the first sheet and first row as the header
store_data = pd.read_excel('C:/Users/JJMARTINEZ/WalMart/TiendasWal.xlsx')

# Print the column names
print(store_data.columns)

def geocode_with_retry(address, retries=3):
    for i in range(retries):
        try:
            location = geocode(address)
            return location
        except Exception as e:
            if i < retries - 1:
                time.sleep(2**(i+1))
            else:
                print(f"Error geocoding address: {address} - {e}")
                return None

# Define a function to geocode addresses using the Nominatim geocoding service
def geocode_address(row):
    address = f"{row['Dirección']}, {row['Ciudad']}, {row['Estado']}, Mexico"
    location = geocode_with_retry(address)
    if location:
        return pd.Series((location.latitude, location.longitude), index=['latitude', 'longitude'])
    else:
        return pd.Series((None, None), index=['latitude', 'longitude'])

# Geocode store addresses
store_data[['latitude', 'longitude']] = store_data.apply(geocode_address, axis=1)

# Save the updated store data with coordinates to a new CSV file
store_data.to_csv('C:/Users/JJMARTINEZ/WalMart/brand_x_stores.csv', index=False)
