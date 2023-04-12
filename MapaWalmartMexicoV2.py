import pandas as pd
import geopandas as gpd
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors

# Read store data
store_locations = pd.read_csv('C:/Users/JJMARTINEZ/WalMart/WalStores.csv')

# Read Mexico shapefile
mexico = gpd.read_file('C:/Users/JJMARTINEZ/WalMart/ne_10m_admin_1_states_provinces/ne_10m_admin_1_states_provinces.shp')
mexico = mexico[mexico['iso_a2'] == 'MX']

# Create GeoDataFrame for store locations
gdf_stores = gpd.GeoDataFrame(store_locations, geometry=gpd.points_from_xy(store_locations.longitude, store_locations.latitude))

# Dictionary to map state names in store data to state names in shapefile
state_name_map = {
    'Baja California Norte': 'Baja California',
    'Estado De México': 'México',
    # Add any other mappings if required
}

# Update the state names in the store data
store_locations['Estado'] = store_locations['Estado'].replace(state_name_map)

# Calculate store count per state
state_store_count = store_locations.groupby('Estado').size().reset_index(name='store_count')

# Merge store count data with Mexican states
mexico_with_store_count = mexico.merge(state_store_count, left_on='name', right_on='Estado')

# Create custom colormap
cmap = mcolors.LinearSegmentedColormap.from_list("", ["white", "darkred"])

# Plot the map
fig, ax = plt.subplots(figsize=(15, 15))
mexico.boundary.plot(ax=ax, linewidth=1, edgecolor='black')
mexico_with_store_count.plot(column='store_count', cmap=cmap, ax=ax, legend=True, zorder=1, vmin=0, vmax=50)
gdf_stores.plot(ax=ax, color='red', markersize=30, zorder=2)
plt.title('Ubicación Walmarts Nivel Nacional')
plt.show()


