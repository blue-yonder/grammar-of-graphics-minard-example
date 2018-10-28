import pandas as pd
import altair as alt
import numpy as np
from vega_datasets import data

cities = pd.read_csv("data/minard_cities.txt", sep=" ", names=["lon", "lat", "city"])
temperatures = pd.read_csv("data/minard_temperature.txt", sep=" ", names=["lon", "temp", "days", "day"])
troops = pd.read_csv("data/minard_troops.txt", sep=" ", names=["lon",  "lat", "survivors" , "direction", "division"])

temperatures["label"] = temperatures.fillna("").apply(
    axis=1, func=lambda row: "{}° {}".format(row[1], row[3].replace("-", " "))
)
troops = troops.sort_values(by=["division", "survivors"], ascending=False)

troops_chart = alt.Chart(troops).mark_trail().encode(
    x='lon:Q',
    y='lat:Q',
    size=alt.Size('survivors', scale=alt.Scale(range=[1, 75]), legend=None),
    color=alt.Color('direction')
)
troops_chart.save("troops_first_try.html")

troops_chart = alt.Chart(troops).mark_trail().encode(
    longitude='lon:Q',
    latitude='lat:Q',
    size=alt.Size(
        'survivors', 
        scale=alt.Scale(range=[1, 75]), 
        legend=None
    ),
    detail='division',
    color=alt.Color(
        'direction', 
        scale=alt.Scale(
            domain=['A', 'R'],
            range=['#EBD2A8', '#888888']
        ), 
        legend=None
    ),
).project(
    type="mercator"
)
troops_chart.save("troops.html")

# Small manipulation to scatter the troop size text a bit
troops_text = troops.iloc[::2, :].copy()
troops_text["lon"] += 0.13 * (troops_text["division"])
troops_text["lat"] += troops_text["direction"].replace({"A": 0.35, "R": -0.21})

troops_text_chart = alt.Chart(troops_text).mark_text(
    font='Cardo',
    fontSize=7,
    fontStyle='italic',
    angle=280
).encode(
    longitude='lon:Q',
    latitude='lat:Q',
    text='survivors'
).project(
    type="mercator"
)
troops_text_chart.save("troops_text.html")

cities_chart = alt.Chart(cities).mark_text(
    font='Cardo',
    fontSize=11,
    fontStyle='italic',
    dx=-3
).encode(
    longitude='lon:Q',
    latitude='lat:Q',
    text='city',
).project(
    type="mercator"
)
cities_chart.save("cities.html")

x_encode = alt.X(
    'lon:Q', 
    scale=alt.Scale(
        domain=[cities["lon"].min(), cities["lon"].max()]
    ),
    axis=None
)

y_encode = alt.Y(
    'temp',
    axis=alt.Axis(
        title="Temperature on Retreat", 
        grid=True, 
        orient='right'
    )
)

temperatures_chart = alt.Chart(temperatures).mark_line(
    color="#888888"
).encode(
    x=x_encode,
    y=y_encode
) + alt.Chart(temperatures).mark_text(
    dx=5, 
    dy=20, 
    font='Cardo', 
    fontSize=10
).encode(
    x=x_encode,
    y=y_encode,
    text='label'
)
temperatures_chart.save("temperature.html")

temperatures_chart = temperatures_chart.properties(
    height=100
)

map_chart = troops_chart + cities_chart + troops_text_chart

final_chart = alt.vconcat(map_chart, temperatures_chart).configure_view(
    width=900,
    height=400,
    strokeWidth=0
).configure_axis(
    grid=False,
    labelFont="Cardo",
    titleFont="Cardo"
)

final_chart.save("minard_chart.html")