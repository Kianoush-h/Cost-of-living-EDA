
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


output_folder = 'output_plots'
os.makedirs(output_folder, exist_ok=True)

prices = countries.columns[2:-2]

i_list = []
# Plot each subplot separately and save them
for i in range(len(prices)):
    fig, ax = plt.subplots(figsize=(16, 6))
    
    # Handle the repeated columns
    if type(world[prices[i]]) is pd.DataFrame:
        col = world[prices[i]].iloc[:, c]
        c -= 1
        c = abs(c)
    else:
        col = world[prices[i]]

    world.plot(column=col, ax=ax, legend=True, legend_kwds={'label': "Cost"})
    ax.set_title(prices[i])

    # Save the individual plot
    plot_filename = os.path.join(output_folder, f'{i}_plot.png')
    plt.savefig(plot_filename)
    plt.close()
    i_list += [i]

# Read all the saved plots and concatenate them vertically
all_plots = [plt.imread(os.path.join(output_folder, f'{price}_plot.png')) for price in i_list]
concatenated_image = np.concatenate(all_plots, axis=0)

# Save the concatenated image
output_filename = 'concatenated_plots.png'
plt.imsave(output_filename, concatenated_image)





# =============================================================================
# PART 4: Mapping All Columns Normalized
# =============================================================================


data = world.iloc[:,9:]
x = data.values

min_max_scalar = preprocessing.MinMaxScaler()
x_scaled = min_max_scalar.fit_transform(x)

data_norm = pd.DataFrame(x_scaled)
data_norm.columns = data.columns

df_summary = pd.DataFrame(world['country'])
df_summary['total'] = data_norm.iloc[:,:56].mean(axis=1)

fig, ax = plt.subplots(1, figsize=(16,6))
                              

world.plot(column=df_summary['total'], ax=ax,
            legend=True,
            legend_kwds={'label': "Most to least expensive place to live"})

ax.title.set_text("All prices normalized for each Country")










