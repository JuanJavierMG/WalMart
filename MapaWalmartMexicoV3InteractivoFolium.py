import pandas as pd
import geopandas as gpd
import folium
from folium.plugins import HeatMap
from folium.features import GeoJsonTooltip

# Read store data
store_locations = pd.read_csv('C:/Users/JJMARTINEZ/WalMart/WalStores.csv')

# Read Mexico shapefile
mexico = gpd.read_file('C:/Users/JJMARTINEZ/WalMart/ne_10m_admin_1_states_provinces/ne_10m_admin_1_states_provinces.shp')
mexico = mexico[mexico['iso_a2'] == 'MX']

# Dictionary to map state names in store data to state names in shapefile
state_name_map = {
    'Baja California Norte': 'Baja California',
    'Estado De México': 'México',
}

# Update the state names in the store data
store_locations['Estado'] = store_locations['Estado'].replace(state_name_map)

# Calculate store count per state
state_store_count = store_locations.groupby('Estado').size().reset_index(name='store_count')

# Merge store count data with Mexican states
mexico_with_store_count = mexico.merge(state_store_count, left_on='name', right_on='Estado')

# Calculate the center of the map
map_center = mexico.geometry.centroid.unary_union.centroid.coords[:][0]
map_center = (map_center[1], map_center[0])  # Swap coordinates to match Folium's (lat, lon) format

# Create the base map
m = folium.Map(location=map_center, zoom_start=5)

# Define the tooltip
tooltip = GeoJsonTooltip(
    fields=["name"],
    aliases=["State:"],
    localize=True,
    sticky=False,
    labels=True,
    style="""
        background-color: #F0EFEF;
        border: 2px solid black;
        border-radius: 3px;
        box-shadow: 3px;
    """,
    max_width=800,
)

# Add state polygons with choropleth
choropleth = folium.Choropleth(
    geo_data=mexico_with_store_count.to_json(),
    name="choropleth",
    data=state_store_count,
    columns=["Estado", "store_count"],
    key_on="feature.properties.name",
    fill_color="YlOrRd",
    fill_opacity=0.7,
    line_opacity=0.5,
    legend_name="Store Count",
    highlight=True,  # Add highlight=True for better interactivity
).add_to(m)

# Add the tooltip to the choropleth layer
tooltip = folium.features.GeoJsonTooltip(
    fields=["name", "store_count"], 
    aliases=["Estado:", "Número de Tiendas:"], 
    localize=True
)
choropleth.geojson.add_child(tooltip)

# Add store points
for idx, row in store_locations.iterrows():
    folium.CircleMarker(
        location=[row["latitude"], row["longitude"]],
        radius=5,
        color="red",
        fill=True,
        fill_color="red",
        fill_opacity=0.7,
    ).add_to(m)

# Add layer control
folium.LayerControl().add_to(m)

# Add a title to the map
title_html = '''
             <h3 align="center" style="font-size:20px"><b>Tiendas X en México</b></h3>
             '''
m.get_root().html.add_child(folium.Element(title_html))

# Save the map
m.save("BrandX_Stores_Mexico.html")
