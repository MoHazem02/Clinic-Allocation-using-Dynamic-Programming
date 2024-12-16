from dash import dcc, html, dash_table
import pandas as pd

# Initial data for the areas
areas = ["Dokki", "New Cairo", "New Giza", "Administrative Capital", "Obour"]
populations = [500000, 700000, 300000, 800000, 400000]
costs = [100, 150, 70, 200, 90]
data = pd.DataFrame({"Area": areas, "Population": populations, "Cost": costs})

# UI Layout
def create_layout():
    return html.Div([
        html.Div([
            html.Img(src="/assets/logo.png", className="inline-block h-12 mr-4 mt-4"),
            html.H1("Optimize Clinic Locations", 
                    className="inline-block text-white text-center text-4xl font-bold mt-4")
        ], className="flex items-center justify-center mb-6"),

        html.Div([
            html.Div([
                html.H3("Areas Data Table", className="text-white text-xl font-semibold mb-4"),
                dash_table.DataTable(
                    id="input-table",
                    columns=[{"name": col, "id": col} for col in data.columns],
                    data=data.to_dict("records"),
                    editable=True,
                    style_table={"width": "100%", "borderRadius": "8px", "overflow": "hidden"},
                    style_cell={"textAlign": "center", "color": "#FFFFFF", "backgroundColor": "#1E293B"},
                    style_header={
                        "backgroundColor": "#4CAF50",
                        "color": "white",
                        "fontWeight": "bold",
                        "textAlign": "center",
                        "border": "1px solid #4CAF50"
                    },
                    style_data={"border": "1px solid #4CAF50"}
                ),
                html.Button(
    "Add Area",
    id="add-area-button",
    n_clicks=0,
    className="bg-blue-500 text-white py-2 px-8 rounded hover:bg-blue-600 mt-4 self-end"
)

            ], className="w-1/2 inline-block align-top h-70 relative"),

            html.Div([
                html.Div(
                    id="add-area-modal",
                    style={"display": "none", "height": "100%"},
                    className="p-4 border border-green-500 rounded bg-gray-800 ml-10 w-90 h-70",
                    children=[
                        html.Label("Area Name:", className="text-white block mb-2"),
                        dcc.Input(id="new-area-name", type="text", className="w-full mb-4 p-2 rounded bg-gray-700 text-white"),

                        html.Label("Population:", className="text-white block mb-2"),
                        dcc.Input(id="new-area-population", type="number", className="w-full mb-4 p-2 rounded bg-gray-700 text-white"),

                        html.Label("Cost:", className="text-white block mb-2"),
                        dcc.Input(id="new-area-cost", type="number", className="w-full mb-4 p-2 rounded bg-gray-700 text-white"),

                        html.Div([
                            html.Button(
                                "Add",
                                id="submit-new-area",
                                n_clicks=0,
                                className="bg-green-500 text-white py-2 px-4 rounded hover:bg-green-600 mr-2"
                            ),
                            html.Button(
                                "Cancel",
                                id="cancel-new-area",
                                n_clicks=0,
                                className="bg-red-500 text-white py-2 px-4 rounded hover:bg-red-600"
                            )
                        ])
                    ]
                )
            ], className="w-1/4 inline-block align-top ml-5 h-70")
        ], className="flex items-center mb-8"),

        html.Div([
            html.Label("Enter Budget:", className="text-white mr-4"),
            dcc.Input(id="budget-input", type="number", value=300, min=1, step=1, 
                      className="w-36 p-2 rounded bg-gray-700 text-white mr-4"),
            html.Button(
                "Optimize Allocation",
                id="optimize-button",
                n_clicks=0,
                className="bg-green-500 text-white py-2 px-4 rounded hover:bg-green-600"
            )
        ], className="mt-4 mb-8 text-left"),

        html.Div([
            html.Div([
                html.H3("Optimization Results", className="text-white text-xl font-semibold mb-4"),
                dash_table.DataTable(
                    id="output-table",
                    columns=[
                        {"name": "Area", "id": "Area"},
                        {"name": "Population", "id": "Population"},
                        {"name": "Cost", "id": "Cost"},
                        {"name": "Status", "id": "Status"}
                    ],
                    data=[],
                    style_table={"width": "100%", "borderRadius": "8px", "overflow": "hidden"},
                    style_cell={"textAlign": "center", "color": "#FFFFFF", "backgroundColor": "#1E293B"},
                    style_header={
                        "backgroundColor": "#4CAF50",
                        "color": "white",
                        "fontWeight": "bold",
                        "textAlign": "center",
                        "border": "1px solid #4CAF50"
                    },
                    style_data={"border": "1px solid #4CAF50"},
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
    className="text-white mt-8 text-2xl font-bold p-4 rounded-lg inline-block",
    style={"border": "2px solid #4CAF50"}
)


            ], className="w-1/2 inline-block align-top"),

           html.Div([
    html.H3("Population Contribution", className="text-white text-xl font-semibold mb-4"),
    dcc.Graph(id="population-chart")
], className="w-2/5 inline-block align-top ml-8 bg-[#001f3f] rounded-lg p-4", style={"border": "2px solid #4CAF50"})

        ])
    ], className="bg-gray-800 p-8")
