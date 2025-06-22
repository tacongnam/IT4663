from ortools.sat.python import cp_model

costs = [
    [90, 76, 75, 70],
    [35, 85, 55, 65],
    [125, 95, 90, 105],
    [45, 110, 95, 115],
    [60, 105, 80, 75],
    [45, 65, 110, 95],
]
num_workers = len(costs)
num_tasks = len(costs[0])

team1 = [0, 2, 4]
team2 = [1, 3, 5]
team_max = 2

model = cp_model.CpModel()

x = {}
for worker in range(num_workers):
    for task in range(num_tasks):
        x[worker, task] = model.new_bool_var(f'{worker}_{task}')

for worker in range(num_workers):
    model.add_at_most_one(x[worker, j] for j in range(num_tasks))

for task in range(num_tasks):
    model.add_exactly_one(x[i, task] for i in range(num_workers))

team1_task = []
for worker in team1:
    for task in range(num_tasks):
        team1_task.append(x[worker, task])
model.add(sum(team1_task) <= team_max)

team2_task = []
for worker in team2:
    for task in range(num_tasks):
        team2_task.append(x[worker, task])
model.add(sum(team2_task) <= team_max)

objective_terms = []
for worker in range(num_workers):
    for task in range(num_tasks):
        objective_terms.append(costs[worker][task] * x[worker, task])
model.minimize(sum(objective_terms))

solver = cp_model.CpSolver()
status = solver.solve(model)

if status == cp_model.OPTIMAL:
    print(f'Total cost: {solver.objective_value}')
    for worker in range(num_workers):
        for task in range(num_tasks):
            if solver.boolean_value(x[worker, task]):
                print(f'Task {task} is assigned to worker {worker}')
else:
    print('No optimal solution!')