import pandas as pd
import geopandas as gpd

# Read the store data
store_locations = pd.read_csv('C:/Users/JJMARTINEZ/WalMart/WalStores.csv')

# Read the shapefile
mexico = gpd.read_file('C:/Users/JJMARTINEZ/WalMart/ne_10m_admin_1_states_provinces/ne_10m_admin_1_states_provinces.shp')
mexico = mexico[mexico['admin'] == 'Mexico']

# Print the unique state names in the store data
unique_store_states = store_locations['Estado'].unique()
print("Unique state names in store data:")
print(unique_store_states)

# Print the unique state names in the shapefile
unique_shapefile_states = mexico['name'].unique()
print("\nUnique state names in shapefile:")
print(unique_shapefile_states)
