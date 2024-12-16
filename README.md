# Optimizing Clinic Allocation Using 0/1 Knapsack

## Overview

This program solves a real-world optimization problem: **The Egyptian Ministry of Health (MOH) aims to allocate new clinics to specific areas to maximize the population served within a given budget.** Each area has an associated population (benefit) and cost (expense). The goal is to select areas such that the total cost does not exceed the budget while maximizing the total population served.

The program employs the **0/1 Knapsack Algorithm**, implemented using Dynamic Programming (DP), to determine the optimal selection of areas.

---

## Problem Definition

The problem can be mapped to the 0/1 Knapsack Problem as follows:

- **Values**: Population of each area (benefit to maximize).
- **Weights**: Cost of establishing a clinic in each area (constraint to limit).
- **Capacity**: The total budget allocated by the government.
- **Objective**: Maximize the total population served without exceeding the budget.

### Real-World Context

- Areas represent potential locations for clinics.
- Population serves as a measure of the benefit of opening a clinic in that area.
- Cost represents the financial expense of setting up a clinic.
- The Ministry of Health wants to maximize the impact of its resources.

---

## Features

### 1. Add and Manage Areas
Users can dynamically add new areas with:
- Area name.
- Population served by a clinic in that area.
- Cost of setting up a clinic in the area.

### 2. Optimize Clinic Allocation
The program calculates the optimal set of areas to allocate clinics using the 0/1 Knapsack Algorithm. It outputs:
- A list of selected and non-selected areas.
- Total population served by the selected areas.

### 3. Visualize Results
- **Pie Chart**: Displays the contribution of each selected area to the total population served.
- **Table**: Shows all areas with their population, cost, and selection status.

---

## Logic of the 0/1 Knapsack Algorithm

The program uses a **Dynamic Programming (DP)** approach to solve the 0/1 Knapsack problem. Here’s how it works:

1. **DP Table Setup**:
   - Create a 2D DP table, `dp[i][w]`, where:
     - `i` represents the first `i` items (areas).
     - `w` represents the budget limit (capacity).
     - `dp[i][w]` stores the maximum population that can be served using the first `i` areas without exceeding the budget `w`.

2. **Fill the DP Table**:
   - Iterate over each area and budget value.
   - If the cost of the current area is less than or equal to the budget:
     - Either **include** the area (add its population and reduce the remaining budget).
     - Or **exclude** the area.
     - Take the maximum of these two options.
   - Otherwise, exclude the area.

3. **Trace Back Selected Areas**:
   - Start from the bottom-right of the DP table.
   - If the value changes when moving to the previous row, the area was included in the optimal solution.

---

## How to Run the Program

### Prerequisites
1. Python 3.x installed.
2. Required libraries:
   - Dash
   - Pandas
   - NumPy
   - Plotly

Install dependencies using:
```bash
pip install dash pandas numpy plotly
```

### Execution
Run the program using:
```bash
python app.py
```
The web application will start, and you can access it at `http://127.0.0.1:8050` in your browser.

---

## Usage

1. **Add Areas**:
   - Use the "Add Area" button to input the name, population, and cost for a new area.

2. **Set Budget**:
   - Input the total budget allocated for the project.

3. **Optimize Allocation**:
   - Click the "Optimize" button to calculate the best allocation of clinics.

4. **View Results**:
   - The output table lists all areas with their status (Selected/Not Selected).
   - A pie chart visualizes the population contribution of selected areas.
   - The total population served is displayed.

---

## Example

### Input Data
| Area  | Population | Cost |
|-------|------------|------|
| Area1 | 5000       | 10   |
| Area2 | 3000       | 5    |
| Area3 | 4000       | 7    |
| Area4 | 2500       | 3    |

**Budget**: 15

### Output
| Area  | Population | Cost | Status      |
|-------|------------|------|-------------|
| Area1 | 5000       | 10   | Selected    |
| Area2 | 3000       | 5    | Selected    |
| Area3 | 4000       | 7    | Not Selected|
| Area4 | 2500       | 3    | Selected    |

**Total Selected Population**: 10500

**Pie Chart**: Visualizes the contribution of Area1, Area2, and Area4.

---

## Technical Details

### Function Descriptions

1. **`knapsack(values, weights, capacity)`**:
   - Solves the 0/1 Knapsack problem using Dynamic Programming.
   - Returns the indices of selected areas.

2. **`add_new_area`**:
   - Callback to add new areas to the input table.

3. **`optimize_allocation`**:
   - Callback to calculate the optimal allocation and update the output table, pie chart, and total population.

4. **`toggle_add_area_modal`**:
   - Callback to toggle the "Add Area" modal visibility.

---

---

## License
This project is licensed under the MIT License. See the LICENSE file for details.

---

## Acknowledgments
Thanks to:
- Omar Khaled
- Nada Omar
- Mohamed Hazem
- Ahmed Taha
- Hamza El Ghonemy
- Abdelrahman Hesham

