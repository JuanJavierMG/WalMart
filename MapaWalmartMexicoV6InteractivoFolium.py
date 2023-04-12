import pandas as pd
import geopandas as gpd
import folium
from folium.plugins import HeatMap
import folium.plugins as plugins
import base64

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
m = folium.Map(location=map_center, zoom_start=5, control_scale=True)

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
    legend_name="Tiendas X en México",
).add_to(m)

# Add tooltips for states
tooltip = folium.features.GeoJsonTooltip(
    fields=["name", "store_count"],
    aliases=["Estado: ", "Número de tiendas: "],
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

choropleth.geojson.add_child(tooltip)

# Add store points with tooltips
for idx, row in store_locations.iterrows():
    tooltip = folium.Tooltip(f"Store Name: {row['Tienda']}<br>Coordinates: ({row['latitude']}, {row['longitude']})")
    folium.CircleMarker(
        location=[row["latitude"], row["longitude"]],
        radius=5,
        color="red",
        fill=True,
        fill_color="red",
        fill_opacity=0.7,
        tooltip=tooltip,
    ).add_to(m)

# Add a search box for states
search = plugins.Search(
    layer=choropleth.geojson,
    search_label="name",
    search_zoom=7,
    geom_type="Polygon",
    position="topleft",
).add_to(m)

# Enable clustering of store markers
marker_cluster = plugins.MarkerCluster().add_to(m)
for idx, row in store_locations.iterrows():
    folium.CircleMarker(
        location=[row["latitude"], row["longitude"]],
        radius=5,
        color="red",
        fill=True,
        fill_color="red",
        fill_opacity=0.7,
    ).add_to(marker_cluster)

# Add layer control
folium.LayerControl().add_to(m)

# Add fullscreen button
plugins.Fullscreen(position='topright').add_to(m)

# Add the title
title_html = '''
             <h3 align="center" style="font-size:20px"><b>Brand X Stores in Mexico</b></h3>
             '''
m.get_root().html.add_child(folium.Element(title_html))

# Add the company logo
logo_path = "logo.png"  # Replace this with the path to your company logo
logo_base64 = base64.b64encode(open(logo_path, "rb").read()).decode()
logo_html = f'<img src="data:image/png;base64,{logo_base64}" style="position:fixed; bottom:10px; right:10px; width:100px; height:auto; z-index:9999; opacity: 0.8;">'
m.get_root().html.add_child(folium.Element(logo_html))

# Save the map as an HTML file
m.save("BrandX_Stores_Mexico.html")




