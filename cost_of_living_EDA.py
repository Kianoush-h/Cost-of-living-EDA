
"""
@author: Kianoush 

GitHUb: https://github.com/Kianoush-h
YouTube: https://www.youtube.com/channel/UCvf9_53f6n3YjNEA4NxAkJA
LinkedIn: https://www.linkedin.com/in/kianoush-haratiannejadi/

Email: haratiank2@gmail.com

"""


import pandas as pd
import geopandas as gpd
import numpy as np
import folium
from folium import Circle
import matplotlib.pyplot as plt
from sklearn import preprocessing

from opencage.geocoder import OpenCageGeocode


df = pd.read_csv("data/cost-of-living.csv", index_col=[0]).T.reset_index()
df = df.rename(columns={'index':'location'})
head = df.head()


# =============================================================================
# PART 1: preparing geo maping
# Using OpenCage to Retrieve Latitude and Longitude
# =============================================================================

geocoder = OpenCageGeocode("0eca49e8e89d4b6e9485ef2fac579f82")

list_lat = [] 
list_long = []

for row in df.location:
    try:
        query = str(row)
        results = geocoder.geocode(query)   
        lat = results[0]['geometry']['lat']
        long = results[0]['geometry']['lng']
        list_lat.append(lat)
        list_long.append(long)
    except:
        list_lat.append(None)
        list_long.append(None)

df['lat'] = list_lat   
df['lon'] = list_long




df['city'] = df['location'].apply(lambda x: str(x).split(', ')[0])


# =============================================================================
# PART 2: Mapping with Folium
# =============================================================================

top_range = (df.describe().loc['min',:]/df.describe().loc['max',:]).sort_values().index[2:22]
print(list(top_range))



def color_producer(val):
    if val <= df[item].quantile(.25):
        return 'forestgreen'
    elif val <= df[item].quantile(.50):
        return 'goldenrod'
    elif val <= df[item].quantile(.75):
        return 'darkred'
    else:
        return 'black'


# Price of:  Taxi 1hour Waiting (Normal Tariff)
m_1 = folium.Map(location=[df.lat.mean(),df.lon.mean()], tiles='cartodbpositron', zoom_start=2)

item = top_range[0]

# Add a bubble map to the base map
for i in range(0,len(df)):
    Circle(
        location=[df.iloc[i]['lat'], df.iloc[i]['lon']],
        radius=1000,
        color=color_producer(df.iloc[i][item])).add_to(m_1)

print ('Price of: ', item)

m_1.show_in_browser()


#Price of:  Price per Square Meter to Buy Apartment Outside of Centre
m_2= folium.Map(location=[df.lat.mean(),df.lon.mean()], tiles='cartodbpositron', zoom_start=2)
item = top_range[2]

# Add a bubble map to the base map
for i in range(0,len(df)):
    Circle(
        location=[df.iloc[i]['lat'], df.iloc[i]['lon']],
        radius=1000,
        color=color_producer(df.iloc[i][item])).add_to(m_2)

print ('Price of: ', item)


# Price of:  Average Monthly Net Salary (After Tax)
m_3= folium.Map(location=[df.lat.mean(),df.lon.mean()], tiles='cartodbpositron', zoom_start=2)
item = top_range[9]

# Add a bubble map to the base map
for i in range(0,len(df)):
    Circle(
        location=[df.iloc[i]['lat'], df.iloc[i]['lon']],
        radius=1000,
        color=color_producer(df.iloc[i][item])).add_to(m_3)

print ('Price of: ', item)


# Price of:  Toyota Corolla 1.6l 97kW Comfort (Or Equivalent New Car)
m_4= folium.Map(location=[df.lat.mean(),df.lon.mean()], tiles='cartodbpositron', zoom_start=2)
item = 'Toyota Corolla 1.6l 97kW Comfort (Or Equivalent New Car)'

# Add a bubble map to the base map
for i in range(0,len(df)):
    Circle(
        location=[df.iloc[i]['lat'], df.iloc[i]['lon']],
        radius=1000,
        color=color_producer(df.iloc[i][item])).add_to(m_4)

print ('Price of: ', item)





# =============================================================================
# PART 3: Mapping a Choropleth with MatPlotLib
# =============================================================================


cities = gpd.read_file(gpd.datasets.get_path('naturalearth_cities'))
world = gpd.read_file(gpd.datasets.get_path('naturalearth_lowres'))



df['country'] = df.location.apply(lambda x: str(x).split(', ')[-1])
countries = df.groupby('country', as_index=False).mean()
name_change = {'Bosnia And Herzegovina' : 'Bosnia and Herz.',
'United States' : 'United States of America',
'Czech Republic' : 'Czechia',
'Dominican Republic' : 'Dominican Rep.'}

countries['country'] = countries.country.replace(name_change)




world = world[world.name.isin(countries.country.values)]
world = world.sort_values(by='name').reset_index()
countries = countries.sort_values(by='country').reset_index()
world = world.merge(countries, left_on=['name'], right_on=['country'])

prices = countries.columns[2:-2]
fig, ax = plt.subplots(len(prices), figsize=(16,6*len(prices)))

c = 0
for i in range(len(prices)):
    
    # some column names are repeated in the dataset, but the data is different.
    # An if-else makes sure each of these repeated columns in mapped.
    if type(world[prices[i]]) is pd.DataFrame:
        col = world[prices[i]].iloc[:,c]
        c -= 1
        c = abs(c)
    else:
        col = world[prices[i]] 
                              
    world.plot(column=col,
                ax=ax[i],
                legend=True,
                legend_kwds={'label': "Cost"})
    ax[i].title.set_text(prices[i])







# Create subplots based on the number of prices
fig, ax = plt.subplots(len(prices), figsize=(16, 6 * len(prices)))

# Iterate over the prices
for i, price in enumerate(prices):
    # Extract the column from the 'world' DataFrame
    col = world[price]

    # Check if the column is a DataFrame and extract the appropriate column
    if isinstance(col, pd.DataFrame):
        col = col.iloc[:, c]
        c -= 1
        c = abs(c)

    # Plot the data
    world.plot(column=col, ax=ax[i], legend=True, legend_kwds={'label': "Cost"})

    # Set subplot title
    ax[i].set_title(price)

# Adjust layout to prevent overlap
plt.tight_layout()

# Show the plots
plt.show()



























