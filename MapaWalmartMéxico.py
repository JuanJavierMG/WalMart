import pandas as pd
import geopandas as gpd
import matplotlib.pyplot as plt

store_locations = pd.read_csv('C:/Users/JJMARTINEZ/WalMart/WalStores.csv')

print("Missing coordinates:", store_locations[store_locations.isnull().any(axis=1)].shape[0])
store_locations = store_locations.dropna(subset=['latitude', 'longitude'])

mexico = gpd.read_file(gpd.datasets.get_path('naturalearth_lowres'))
mexico = mexico[mexico['iso_a3'] == 'MEX'].dissolve(by='iso_a3').reset_index()

gdf_stores = gpd.GeoDataFrame(store_locations, geometry=gpd.points_from_xy(store_locations.longitude, store_locations.latitude))
gdf_stores.crs = mexico.crs

state_store_count = store_locations.groupby('Estado').size().reset_index(name='store_count')
mexico_with_store_count = mexico.merge(state_store_count, left_on='name', right_on='Estado')

fig, ax = plt.subplots(figsize=(15, 15))
mexico.boundary.plot(ax=ax, linewidth=1, edgecolor='black')
mexico_with_store_count.plot(column='store_count', cmap='coolwarm', legend=True, linewidth=0.5, edgecolor='black', ax=ax)

gdf_stores.plot(ax=ax, color='red', markersize=30, legend=True, zorder=2)

ax.set_title('Brand X Stores in Mexico')
ax.set_aspect('auto')
ax.set_xticks([])
ax.set_yticks([])
plt.tight_layout()
plt.show()
