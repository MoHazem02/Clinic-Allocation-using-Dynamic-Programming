from dash import Dash, Input, Output, State, dcc, html, dash_table, ctx
import pandas as pd
import numpy as np
import plotly.express as px

areas = ["Dokki", "New Cairo", "New Giza", "Administrative Capital", "Obour"]
populations = [500000, 700000, 300000, 800000, 400000]
costs = [100, 150, 70, 200, 90]
data = pd.DataFrame({"Area": areas, "Population": populations, "Cost": costs})

app = Dash(__name__)
app.layout = html.Div([
    html.H1("Optimize Clinic Locations", style={"color": "#FFFFFF", "textAlign": "center"}),

html.Div([
    html.Div([
        html.H3("Areas Data Table", style={"color": "#FFFFFF"}),
        dash_table.DataTable(
            id="input-table",
            columns=[{"name": col, "id": col} for col in data.columns],
            data=data.to_dict("records"),
            editable=True,
            style_table={"backgroundColor": "#2C2C2C", "width": "100%"},
            style_cell={"textAlign": "center", "color": "#FFFFFF", "backgroundColor": "#2C2C2C"},
            style_header={
                "backgroundColor": "#4CAF50",
                "color": "white",
                "fontWeight": "bold",
                "textAlign": "center"
            }
        )
    ], style={"width": "50%", "display": "inline-block", "verticalAlign": "top"}),

    html.Div([
        html.Button(
            "Add Area",
            id="add-area-button",
            n_clicks=0,
            style={
                "backgroundColor": "#2196F3",
                "color": "#FFFFFF",
                "padding": "10px 20px",
                "border": "none",
                "cursor": "pointer",
                "marginBottom": "10px",
            }
        ),
        html.Div(
            id="add-area-modal",
            style={"display": "none", "padding": "10px", "border": "1px solid #4CAF50", "borderRadius": "5px", 
                   "backgroundColor": "#2C2C2C", "marginLeft": "20px", "width": "200px"},
            children=[
                html.Label("Area Name:", style={"color": "#FFFFFF"}),
                dcc.Input(id="new-area-name", type="text", style={"marginBottom": "10px", "width": "100%"}),

                html.Label("Population:", style={"color": "#FFFFFF"}),
                dcc.Input(id="new-area-population", type="number", style={"marginBottom": "10px", "width": "100%"}),

                html.Label("Cost:", style={"color": "#FFFFFF"}),
                dcc.Input(id="new-area-cost", type="number", style={"marginBottom": "10px", "width": "100%"}),

                html.Div([
                    html.Button(
                        "Add",
                        id="submit-new-area",
                        n_clicks=0,
                        style={"backgroundColor": "#4CAF50", "color": "#FFFFFF", "padding": "10px 20px", "border": "none", 
                               "cursor": "pointer", "marginRight": "10px"}
                    ),
                    html.Button(
                        "Cancel",
                        id="cancel-new-area",
                        n_clicks=0,
                        style={"backgroundColor": "#FF5722", "color": "#FFFFFF", "padding": "10px 20px", "border": "none", 
                               "cursor": "pointer"}
                    )
                ])
            ]
        )
        ], style={"width": "25%", "display": "inline-block", "verticalAlign": "top", "marginLeft": "20px"})
        ], style={"marginBottom": "20px", "display": "flex", "alignItems": "center"}),

    html.Div([
        html.Label("Enter Budget:", style={"color": "#FFFFFF", "marginRight": "10px"}),
        dcc.Input(id="budget-input", type="number", value=300, min=1, step=1, style={"width": "150px", "marginRight": "10px"}),
        html.Button(
            "Optimize Allocation",
            id="optimize-button",
            n_clicks=0,
            style={"backgroundColor": "#4CAF50", "color": "#FFFFFF", "padding": "10px 20px", "border": "none", "cursor": "pointer"}
        )
    ], style={"marginTop": "20px", "marginBottom": "20px", "textAlign": "left"}),

    html.Div([
        html.Div([
            html.H3("Optimization Results", style={"color": "#FFFFFF"}),
            dash_table.DataTable(
                id="output-table",
                columns=[
                    {"name": "Area", "id": "Area"},
                    {"name": "Population", "id": "Population"},
                    {"name": "Cost", "id": "Cost"},
                    {"name": "Status", "id": "Status"}
                ],
                data=[],
                style_table={"backgroundColor": "#2C2C2C", "width": "100%"},
                style_cell={"textAlign": "center", "color": "#FFFFFF", "backgroundColor": "#2C2C2C"},
                style_header={
                    "backgroundColor": "#4CAF50",
                    "color": "white",
                    "fontWeight": "bold",
                    "textAlign": "center"
                },
                style_data_conditional=[
                    {
                        "if": {"filter_query": "{Status} = 'Selected'"},
                        "backgroundColor": "#DFF2BF", 
                        "color": "#000000"
                    },
                    {
                        "if": {"filter_query": "{Status} = 'Not Selected'"},
                        "backgroundColor": "#FFBABA", 
                        "color": "#000000"
                    }
                ]
            ), 
            html.Div(
                id="total-selected-population",
                style={"color": "#FFFFFF", "marginTop": "30px", "fontSize": "40px", "fontWeight": "bold"}
            )
            
        ], style={"width": "50%", "display": "inline-block", "verticalAlign": "top"}),

        html.Div([
            html.H3("Population Contribution", style={"color": "#FFFFFF"}),
            dcc.Graph(id="population-chart")
        ], style={"width": "40%", "display": "inline-block", "verticalAlign": "top", "marginLeft": "20px"})
    ])
], style={"backgroundColor": "#121212", "padding": "20px"})


def knapsack(values, weights, capacity):
    n = len(values)
    dp = np.zeros((n + 1, capacity + 1), dtype=int)

    for i in range(1, n + 1):
        for w in range(1, capacity + 1):
            if weights[i - 1] <= w:
                dp[i][w] = max(dp[i - 1][w], dp[i - 1][w - weights[i - 1]] + values[i - 1])
            else:
                dp[i][w] = dp[i - 1][w]

    w = capacity
    selected = []
    for i in range(n, 0, -1):
        if dp[i][w] != dp[i - 1][w]:
            selected.append(i - 1)
            w -= weights[i - 1]

    return selected


@app.callback(
    Output("total-selected-population", "children"),
    Input("optimize-button", "n_clicks"),
    State("output-table", "data")
)
def update_total_population(n_clicks, output_data):
    total_population = sum(
        row["Population"] for row in output_data if row["Status"] == "Selected"
    )
    return f"Total Selected Population: {total_population}"


@app.callback(
    Output("add-area-modal", "style"),
    [Input("add-area-button", "n_clicks"), Input("cancel-new-area", "n_clicks")]
)
def toggle_add_area_modal(add_clicks, cancel_clicks):
    if ctx.triggered_id == "add-area-button":
        return {"display": "block", "padding": "10px", "border": "1px solid #4CAF50", "borderRadius": "5px", "backgroundColor": "#2C2C2C", "marginTop": "10px"}
    return {"display": "none"}


@app.callback(
    Output("input-table", "data"),
    [Input("submit-new-area", "n_clicks")],
    [State("input-table", "data"),
     State("new-area-name", "value"),
     State("new-area-population", "value"),
     State("new-area-cost", "value")]
)
def add_new_area(n_clicks, table_data, area_name, population, cost):
    if n_clicks > 0 and area_name and population and cost:
        new_row = {"Area": area_name, "Population": population, "Cost": cost}
        table_data.append(new_row)
    return table_data


@app.callback(
    [Output("output-table", "data"), Output("population-chart", "figure")],
    Input("optimize-button", "n_clicks"),
    State("input-table", "data"),
    State("budget-input", "value")
)
def optimize_allocation(n_clicks, input_data, budget):
    if n_clicks == 0 or not input_data or budget is None:
        return [], {}

    df = pd.DataFrame(input_data)
    populations = df["Population"].tolist()
    costs = df["Cost"].tolist()

    selected_indices = knapsack(populations, costs, budget)
    df["Status"] = ["Selected" if i in selected_indices else "Not Selected" for i in range(len(df))]

    # Create Pie Chart
    selected_df = df[df["Status"] == "Selected"]
    pie_chart = px.pie(
        selected_df,
        values="Population",
        names="Area",
        title="Contribution to Total Population Served",
        color_discrete_sequence=px.colors.qualitative.Pastel
    )

    return df.to_dict("records"), pie_chart


if __name__ == "__main__":
    app.run_server(debug=False)
