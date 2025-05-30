import gurobipy as gp
from gurobipy import GRB
import json

# Load the data from the provided JSON
data = {
  "n": 10,
  "m": 4,
  "depot": {
    "id": 0,
    "x": 50,
    "y": 50
  },
  "vehicles": [
    {
      "id": 1,
      "capacity": 100
    },
    {
      "id": 2,
      "capacity": 100
    },
    {
      "id": 3,
      "capacity": 100
    },
    {
      "id": 4,
      "capacity": 100
    }
  ],
  "customers": [
    {
      "id": 1,
      "x": 20,
      "y": 30,
      "demand": 10
    },
    {
      "id": 2,
      "x": 25,
      "y": 60,
      "demand": 20
    },
    {
      "id": 3,
      "x": 40,
      "y": 20,
      "demand": 15
    },
    {
      "id": 4,
      "x": 60,
      "y": 30,
      "demand": 25
    },
    {
      "id": 5,
      "x": 70,
      "y": 70,
      "demand": 10
    },
    {
      "id": 6,
      "x": 55,
      "y": 90,
      "demand": 30
    },
    {
      "id": 7,
      "x": 80,
      "y": 40,
      "demand": 20
    },
    {
      "id": 8,
      "x": 30,
      "y": 80,
      "demand": 15
    },
    {
      "id": 9,
      "x": 65,
      "y": 10,
      "demand": 25
    },
    {
      "id": 10,
      "x": 45,
      "y": 65,
      "demand": 10
    }
  ],
  "distance_matrix": [
    [0.0, 36.06, 26.93, 31.62, 22.36, 28.28, 40.31, 31.62, 36.06, 42.72, 15.81],
    [36.06, 0.0, 30.41, 22.36, 40.0, 64.03, 69.46, 60.83, 50.99, 49.24, 43.01],
    [26.93, 30.41, 0.0, 42.72, 46.1, 46.1, 42.43, 58.52, 20.62, 64.03, 20.62],
    [31.62, 22.36, 42.72, 0.0, 22.36, 58.31, 71.59, 44.72, 60.83, 26.93, 45.28],
    [22.36, 40.0, 46.1, 22.36, 0.0, 41.23, 60.21, 22.36, 58.31, 20.62, 38.08],
    [28.28, 64.03, 46.1, 58.31, 41.23, 0.0, 25.0, 31.62, 41.23, 60.21, 25.5],
    [40.31, 69.46, 42.43, 71.59, 60.21, 25.0, 0.0, 55.9, 26.93, 80.62, 26.93],
    [31.62, 60.83, 58.52, 44.72, 22.36, 31.62, 55.9, 0.0, 64.03, 33.54, 43.01],
    [36.06, 50.99, 20.62, 60.83, 58.31, 41.23, 26.93, 64.03, 0.0, 78.26, 21.21],
    [42.72, 49.24, 64.03, 26.93, 20.62, 60.21, 80.62, 33.54, 78.26, 0.0, 58.52],
    [15.81, 43.01, 20.62, 45.28, 38.08, 25.5, 26.93, 43.01, 21.21, 58.52, 0.0]
  ],
  "demands": [10, 20, 15, 25, 10, 30, 20, 15, 25, 10],
  "vehicle_capacities": [100, 100, 100, 100]
}

# Extract parameters
n = data['n']  # Number of customers (excluding depot)
m = data['m']  # Number of vehicles
customers = data['customers']
distance_matrix = data['distance_matrix']
demands = data['demands']
vehicle_capacities = data['vehicle_capacities']

# Create model
model = gp.Model('VRP')

# Create variables
x = {}  # Binary variables for arcs
u = {}  # Continuous variables for MTZ subtour elimination

# Create arc variables (x_ijk)
for k in range(m):
    for i in range(n + 1):  # 0 is depot, 1..n are customers
        for j in range(n + 1):
            if i != j:  # No self-loops
                x[i, j, k] = model.addVar(vtype=GRB.BINARY, name=f'x_{i}_{j}_{k}')

# Create MTZ variables (u_i)
for i in range(1, n + 1):  # Only for customers, not depot
    u[i] = model.addVar(vtype=GRB.CONTINUOUS, name=f'u_{i}')

# Set objective: minimize total distance
obj = gp.quicksum(distance_matrix[i][j] * x[i, j, k] 
                 for k in range(m) 
                 for i in range(n + 1) 
                 for j in range(n + 1) 
                 if i != j)
model.setObjective(obj, GRB.MINIMIZE)

# Constraints

# 1. Each customer must be visited exactly once
for i in range(1, n + 1):  # For each customer
    model.addConstr(
        gp.quicksum(x[i, j, k] for k in range(m) for j in range(n + 1) if i != j) == 1,
        name=f'visit_customer_{i}'
    )

# 2. Each vehicle starts and ends at the depot
for k in range(m):
    # Vehicle leaves depot exactly once
    model.addConstr(
        gp.quicksum(x[0, j, k] for j in range(1, n + 1)) == 1,
        name=f'vehicle_{k}_start'
    )
    # Vehicle returns to depot exactly once
    model.addConstr(
        gp.quicksum(x[i, 0, k] for i in range(1, n + 1)) == 1,
        name=f'vehicle_{k}_end'
    )

# 3. Flow conservation (if vehicle enters a node, it must leave)
for k in range(m):
    for i in range(1, n + 1):  # For each customer
        model.addConstr(
            gp.quicksum(x[j, i, k] for j in range(n + 1) if i != j) == 
            gp.quicksum(x[i, j, k] for j in range(n + 1) if i != j),
            name=f'flow_{i}_{k}'
        )

# 4. MTZ subtour elimination constraints
for k in range(m):
    for i in range(1, n + 1):
        for j in range(1, n + 1):
            if i != j:
                model.addConstr(
                    u[i] - u[j] + (n + 1) * x[i, j, k] <= n,
                    name=f'mtz_{i}_{j}_{k}'
                )

# 5. Capacity constraints (optional)
for k in range(m):
    model.addConstr(
        gp.quicksum(demands[i-1] * x[i, j, k] 
                   for i in range(1, n + 1) 
                   for j in range(n + 1) 
                   if i != j) <= vehicle_capacities[k],
        name=f'capacity_{k}'
    )

# Optimize the model
model.optimize()

# Print solution
if model.status == GRB.OPTIMAL:
    print('Optimal solution found!')
    print(f'Total distance: {model.ObjVal:.2f}')
    
    # Print routes for each vehicle
    for k in range(m):
        route = []
        current = 0  # Start at depot
        route.append(current)
        visited = set()
        
        while True:
            next_node = None
            for j in range(n + 1):
                if current != j and x[current, j, k].X > 0.5:
                    next_node = j
                    break
            
            if next_node is None or next_node == 0:
                break  # Back to depot
                
            route.append(next_node)
            current = next_node
        
        route.append(0)  # Return to depot
        print(f'Vehicle {k+1} route: {route}')
else:
    print('No solution found or optimization failed')
