import pandas as pd
import geopandas as gpd
import matplotlib.pyplot as plt

mexico = gpd.read_file('C:/Users/JJMARTINEZ/WalMart/ne_10m_admin_1_states_provinces/ne_10m_admin_1_states_provinces.shp')  # Replace with the path to the ne_10m_admin_1_states_provinces.shp file
mexico = mexico[mexico['iso_a2'] == 'MX']

fig, ax = plt.subplots(figsize=(15, 15))
mexico.boundary.plot(ax=ax, linewidth=1, edgecolor='black')
plt.title('Mexico States')
plt.show()

