from ortools.linear_solver import pywraplp

# Problem data
costs = [
    [90, 80, 75, 70],
    [35, 85, 55, 65],
    [125, 95, 90, 95],
    [45, 110, 95, 115],
    [50, 100, 90, 100],
]
num_workers = len(costs)
num_tasks = len(costs[0])

model = pywraplp.Solver.CreateSolver('SCIP')

x = {}
for worker_id in range(num_workers):
    for task_id in range(num_tasks):
        x[worker_id, task_id] = model.IntVar(0, 1, f'{worker_id}_{task_id}')

for worker_id in range(num_workers):
    model.Add(model.Sum([x[worker_id, j] for j in range(num_tasks)]) <= 1)

for task_id in range(num_tasks):
    model.Add(model.Sum([x[i, task_id] for i in range(num_workers)]) == 1)

objective_terms = []
for i in range(num_workers):
    for j in range(num_tasks):
        objective_terms.append(costs[i][j] * x[i, j])
model.Minimize(model.Sum(objective_terms))

status = model.Solve()

if status == pywraplp.Solver.OPTIMAL:
    print(f'Total cost: {model.Objective().Value()}')
    for i in range(num_workers):
        for j in range(num_tasks):
            if x[i, j].solution_value() > 0.5:
                print(f'Task {j} is assigned to worker {i}')
else:
    print('No solution found')