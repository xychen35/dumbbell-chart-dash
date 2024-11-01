import plotly.graph_objects as go
from plotly import data

import pandas as pd
import dash

from dash import html, dcc

app = dash.Dash(__name__)

df = data.gapminder()
df = df.loc[(df.continent == "Europe") & (df.year.isin([1952, 2002]))]

# Interpolating values for the year 1977
def interpolate_row(country_df):
    # Perform linear interpolation between 1952 and 2002 for 1977
    row_1952 = country_df[country_df["year"] == 1952]
    row_2002 = country_df[country_df["year"] == 2002]

    # Interpolated values for 1977
    lifeExp_1977 = (
        row_1952["lifeExp"].values[0]
        + (row_2002["lifeExp"].values[0] - row_1952["lifeExp"].values[0]) * 0.5
    )
    pop_1977 = (
        row_1952["pop"].values[0]
        + (row_2002["pop"].values[0] - row_1952["pop"].values[0]) * 0.5
    )
    gdpPercap_1977 = (
        row_1952["gdpPercap"].values[0]
        + (row_2002["gdpPercap"].values[0] - row_1952["gdpPercap"].values[0]) * 0.5
    )

    # Return the new row for 1977
    return pd.Series(
        {
            "country": row_1952["country"].values[0],
            "continent": row_1952["continent"].values[0],
            "year": 1977,
            "lifeExp": lifeExp_1977,
            "pop": pop_1977,
            "gdpPercap": gdpPercap_1977,
            "iso_alpha": row_1952["iso_alpha"].values[0],
            "iso_num": row_1952["iso_num"].values[0],
        }
    )


# Apply interpolation to each country group and append new rows to the original dataframe
new_rows = df.groupby("country").apply(interpolate_row).reset_index(drop=True)
df_with_1977 = (
    pd.concat([df, new_rows], ignore_index=True)
    .sort_values(by=["country", "year"])
    .reset_index(drop=True)
)


countries = (
    df.loc[(df.continent == "Europe") & (df.year.isin([2002]))]
    .sort_values(by=["lifeExp"], ascending=True)["country"]
    .unique()
)

data = {
    "line_x": [],
    "line_y": [],
    "1952": [],
    "1977": [],
    "2002": [],
    "colors": [],
    "years": [],
    "countries": [],
}

for country in countries:
    data["1952"].extend(
        [df.loc[(df.year == 1952) & (df.country == country)]["lifeExp"].values[0]]
    )
    data["1977"].extend(
        [
            df_with_1977.loc[
                (df_with_1977.year == 1977) & (df_with_1977.country == country)
            ]["lifeExp"].values[0]
        ]
    )
    data["2002"].extend(
        [df.loc[(df.year == 2002) & (df.country == country)]["lifeExp"].values[0]]
    )
    data["line_x"].extend(
        [
            df.loc[(df.year == 1952) & (df.country == country)]["lifeExp"].values[0],
            df.loc[(df.year == 2002) & (df.country == country)]["lifeExp"].values[0],
            None,
        ]
    )
    data["line_y"].extend([country, country, None]),

fig = go.Figure(
    data=[
        go.Scatter(
            x=data["line_x"],
            y=data["line_y"],
            mode="lines",
            showlegend=False,
            marker=dict(color="grey"),
        ),
        go.Scatter(
            x=data["1952"],
            y=countries,
            mode="markers",
            name="1952",
            marker=dict(color="red", size=10),
        ),
        go.Scatter(
            x=data["1977"],
            y=countries,
            mode="markers",
            name="1977",
            marker=dict(color="orange", size=10),
        ),
        go.Scatter(
            x=data["2002"],
            y=countries,
            mode="markers",
            name="2002",
            marker=dict(color="blue", size=10),
        ),
    ]
)

fig.update_layout(
    title="Life Expectancy in Europe: 1952 and 2002",
    height=600,
    legend_itemclick=False,
)

app.layout = html.Div(
    [
        dcc.Graph(id="life-exp-graph", figure=fig),
    ]
)

if __name__ == "__main__":
    app.run_server(debug=True)
