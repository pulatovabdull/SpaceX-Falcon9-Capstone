from pathlib import Path

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

from dash import Dash, dcc, html, Input, Output


# Load the CSV from the same directory as this script.
DATA_PATH = Path(__file__).resolve().parent / "spacex_launch_dash.csv"

spacex_df = pd.read_csv(DATA_PATH)

required_columns = [
    "Launch Site",
    "Payload Mass (kg)",
    "class",
    "Booster Version Category"
]

missing_columns = [
    column for column in required_columns
    if column not in spacex_df.columns
]

if missing_columns:
    raise ValueError(
        "Missing required columns: {}".format(missing_columns)
    )

spacex_df["Payload Mass (kg)"] = pd.to_numeric(
    spacex_df["Payload Mass (kg)"],
    errors="raise"
)

spacex_df["class"] = pd.to_numeric(
    spacex_df["class"],
    errors="raise"
)

if not spacex_df["class"].isin([0, 1]).all():
    raise ValueError("The class column must contain only 0 and 1.")

spacex_df["Booster Version Category"] = (
    spacex_df["Booster Version Category"].astype(str)
)

launch_sites = sorted(
    spacex_df["Launch Site"].dropna().unique()
)

app = Dash(__name__)
app.title = "SpaceX Launch Records Dashboard"


# Tasks 1 and 3: input components.
app.layout = html.Div(
    [
        html.H1(
            "SpaceX Launch Records Dashboard",
            style={
                "textAlign": "center",
                "color": "#333333"
            }
        ),

        html.Label("Select a Launch Site"),

        dcc.Dropdown(
            id="site-dropdown",
            options=[
                {"label": "All Sites", "value": "ALL"}
            ] + [
                {"label": site, "value": site}
                for site in launch_sites
            ],
            value="ALL",
            placeholder="Select a Launch Site here",
            searchable=True,
            clearable=False
        ),

        dcc.Graph(id="success-pie-chart"),

        html.Hr(),

        html.Label("Payload Range (kg)"),

        html.Div(
            dcc.RangeSlider(
                id="payload-slider",
                min=0,
                max=10000,
                step=1000,
                marks={
                    value: "{:,}".format(value)
                    for value in range(0, 10001, 1000)
                },
                value=[0, 10000],
                allowCross=False,
                tooltip={
                    "placement": "bottom",
                    "always_visible": True
                }
            ),
            style={
                "padding": "20px 15px 35px 15px"
            }
        ),

        dcc.Graph(id="success-payload-scatter-chart")
    ],
    style={
        "maxWidth": "1200px",
        "margin": "0 auto",
        "padding": "20px",
        "fontFamily": "Arial, sans-serif"
    }
)


def empty_figure(message):
    fig = go.Figure()

    fig.add_annotation(
        text=message,
        x=0.5,
        y=0.5,
        xref="paper",
        yref="paper",
        showarrow=False,
        font={"size": 18}
    )

    fig.update_xaxes(visible=False)
    fig.update_yaxes(visible=False)
    fig.update_layout(template="plotly_white")

    return fig


# Task 2: pie-chart callback.
@app.callback(
    Output("success-pie-chart", "figure"),
    Input("site-dropdown", "value")
)
def get_pie_chart(entered_site):
    if entered_site == "ALL":
        success_counts = (
            spacex_df.groupby("Launch Site", as_index=False)["class"]
            .sum()
            .rename(columns={"class": "Successful Launches"})
        )

        if success_counts["Successful Launches"].sum() == 0:
            return empty_figure("No successful launches found.")

        fig = px.pie(
            success_counts,
            names="Launch Site",
            values="Successful Launches",
            title="Successful Launches by Site"
        )

    else:
        filtered_df = spacex_df.loc[
            spacex_df["Launch Site"] == entered_site
        ]

        if filtered_df.empty:
            return empty_figure("No launches found for this site.")

        outcome_counts = (
            filtered_df["class"]
            .value_counts()
            .reindex([0, 1], fill_value=0)
        )

        outcome_df = pd.DataFrame({
            "Outcome": ["Failure", "Success"],
            "Launch Count": outcome_counts.to_numpy()
        })

        fig = px.pie(
            outcome_df,
            names="Outcome",
            values="Launch Count",
            color="Outcome",
            color_discrete_map={
                "Failure": "#d62728",
                "Success": "#2ca02c"
            },
            title="Success vs. Failure — {}".format(entered_site)
        )

    fig.update_traces(
        textinfo="label+percent",
        hovertemplate="%{label}<br>Count: %{value}<extra></extra>"
    )

    fig.update_layout(template="plotly_white")

    return fig


# Task 4: scatter-chart callback.
@app.callback(
    Output("success-payload-scatter-chart", "figure"),
    Input("site-dropdown", "value"),
    Input("payload-slider", "value")
)
def get_scatter_chart(entered_site, payload_range):
    low, high = payload_range

    filtered_df = spacex_df.loc[
        (spacex_df["Payload Mass (kg)"] >= low)
        & (spacex_df["Payload Mass (kg)"] <= high)
    ].copy()

    if entered_site != "ALL":
        filtered_df = filtered_df.loc[
            filtered_df["Launch Site"] == entered_site
        ]

    if filtered_df.empty:
        return empty_figure(
            "No launches match this site and payload range."
        )

    site_label = (
        "All Sites" if entered_site == "ALL"
        else entered_site
    )

    fig = px.scatter(
        filtered_df,
        x="Payload Mass (kg)",
        y="class",
        color="Booster Version Category",
        hover_data=["Launch Site"],
        title=(
            "Payload vs. Landing Outcome — {} "
            "({:,}–{:,} kg)"
        ).format(site_label, low, high),
        labels={
            "class": "Landing Outcome",
            "Booster Version Category": "Booster Version"
        },
        opacity=0.75
    )

    fig.update_traces(marker={"size": 11})

    fig.update_yaxes(
        tickmode="array",
        tickvals=[0, 1],
        ticktext=["Failure (0)", "Success (1)"],
        range=[-0.15, 1.15]
    )

    fig.update_layout(template="plotly_white")

    return fig


if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=8051,
        debug=False
    )