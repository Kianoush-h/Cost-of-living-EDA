
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






























