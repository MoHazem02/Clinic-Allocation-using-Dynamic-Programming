from dash import Dash, Input, Output, State, ctx
import numpy as np
import pandas as pd
import plotly.express as px
from ui import create_layout, data

app = Dash(__name__, external_stylesheets=['https://cdn.jsdelivr.net/npm/tailwindcss@2.2.19/dist/tailwind.min.css'])

app.layout = create_layout()


def knapsack(values, weights, capacity):
    """Solves the 0/1 Knapsack problem using Dynamic Programming.
    Time Complexity: O(n * capacity), where n is the number of items and capacity is the maximum weight of the knapsack."""
    n = len(values)  
    # Create a 2D DP table where dp[i][w] represents the maximum value attainable 
    # with the first i items and a weight limit of w
    dp = np.zeros((n + 1, capacity + 1), dtype=int)

    # Fill the DP table
    for i in range(1, n + 1):  
        for w in range(1, capacity + 1): 
            if weights[i - 1] <= w:  # If the current item's weight is less than or equal to the capacity
                # Either exclude the item or include it (add its value and subtract its weight)
                dp[i][w] = max(dp[i - 1][w], dp[i - 1][w - weights[i - 1]] + values[i - 1])
            else:
                # If the item's weight is greater than the current capacity, exclude it
                dp[i][w] = dp[i - 1][w]

    # Trace back the items included in the optimal solution
    w = capacity 
    selected = []  # List to store indices of selected items
    for i in range(n, 0, -1):  
        if dp[i][w] != dp[i - 1][w]:  # If the value changes, the item was included
            selected.append(i - 1)  # Add the item's index (adjusted for 0-based indexing)
            w -= weights[i - 1]  # Reduce the remaining capacity by the item's weight

    return selected  # Return the indices of the selected items

# def knapsack(values, weights, capacity):
    
#     n = len(values)
#     # Call the recursive function with all items
#     return knapsack_recursive(values, weights, capacity, n)

# def knapsack_recursive(values, weights, capacity, n):
#     """Solves the 0/1 Knapsack problem using a recursive approach.
#     Time Complexity: O(2^n), where n is the number of items. This is because the function explores all subsets of items."""
    
#     # Base case: no items left or capacity becomes 0
#     if n == 0 or capacity == 0:
#         return []

#     # Case 1: If the weight of the nth item is greater than the capacity, we cannot include it
#     if weights[n - 1] > capacity:
#         return knapsack_recursive(values, weights, capacity, n - 1)

#     # Case 2: If we include the nth item:
#     # Recurse with reduced capacity and reduced number of items
#     include_items = knapsack_recursive(values, weights, capacity - weights[n - 1], n - 1)
#     include_items = include_items + [n - 1]  # Add current item to the list of selected items

#     # Case 3: If we exclude the nth item:
#     # Recurse without including the current item
#     exclude_items = knapsack_recursive(values, weights, capacity, n - 1)

#     # Compare the value of including or excluding the current item
#     include_value = sum(values[i] for i in include_items)  # Total value if we include the nth item
#     exclude_value = sum(values[i] for i in exclude_items)  # Total value if we exclude the nth item

#     # Return the better choice (including or excluding the nth item)
#     if include_value > exclude_value:
#         return include_items
#     else:
#         return exclude_items



@app.callback(
    Output("add-area-modal", "style"),
    [Input("add-area-button", "n_clicks"), Input("cancel-new-area", "n_clicks")]
)
def toggle_add_area_modal(add_clicks, cancel_clicks):
    if ctx.triggered_id == "add-area-button":
        return {"display": "block", "padding": "10px", "border": "1px solid #4CAF50", "borderRadius": "5px", "backgroundColor": "grey-800", "marginTop": "35px"}
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
    [Output("output-table", "data"), Output("population-chart", "figure"), Output("total-selected-population", "children")],
    Input("optimize-button", "n_clicks"),
    State("input-table", "data"),
    State("budget-input", "value")
)
def optimize_allocation(n_clicks, input_data, budget):
    if n_clicks == 0 or not input_data or budget is None:
        return [], {}, "Total Selected Population: 0"

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
    
    # Calculate Total Selected Population
    total_population = sum(row["Population"] for row in df.to_dict("records") if row["Status"] == "Selected")
    

    return df.to_dict("records"), pie_chart, f"Total Selected Population: {total_population}"


if __name__ == "__main__":
    app.run_server(debug=False)
