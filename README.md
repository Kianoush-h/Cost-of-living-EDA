# Cost of living EDA


## install libraries

```python
pip3 install folium
pip3 install geopandas
pip3 install opencage
```
* Using OpenCage to Retrieve Latitude and Longitude

```python
def color_producer(val):
    if val <= df[item].quantile(.25):
        return 'forestgreen'
    elif val <= df[item].quantile(.50):
        return 'goldenrod'
    elif val <= df[item].quantile(.75):
        return 'darkred'
    else:
        return 'black'
```
* A Function called "color_producer"  takes a numerical value val as its input and assigns a color based on its relationship to the quantiles of a DataFrame column (df[item]). The colors are chosen in a way that reflects different ranges of the data distribution.



## Analysis & Visualizations
# Visualizition Analysis


![Image 1](./plots/base_map.png)
*A bar plot focusing on the Transactions over months.*
