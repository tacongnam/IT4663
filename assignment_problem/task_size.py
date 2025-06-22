from ortools.sat.python import cp_model

costs = [
    [90, 76, 75, 70, 50, 74, 12, 68],
    [35, 85, 55, 65, 48, 101, 70, 83],
    [125, 95, 90, 105, 59, 120, 36, 73],
    [45, 110, 95, 115, 104, 83, 37, 71],
    [60, 105, 80, 75, 59, 62, 93, 88],
    [45, 65, 110, 95, 47, 31, 81, 34],
    [38, 51, 107, 41, 69, 99, 115, 48],
    [47, 85, 57, 71, 92, 77, 109, 36],
    [39, 63, 97, 49, 118, 56, 92, 61],
    [47, 101, 71, 60, 88, 109, 52, 90],
]
num_workers = len(costs)
num_tasks = len(costs[0])

task_sizes = [10, 7, 3, 12, 15, 4, 11, 5]
# Maximum total of task sizes for any worker
total_size_max = 15

model = cp_model.CpModel()

x = {}
for worker in range(num_workers):
    for task in range(num_tasks):
        x[worker, task] = model.new_bool_var(f'{worker}_{task}')

for worker in range(num_workers):
    model.add_at_most_one(x[worker, j] for j in range(num_tasks))
    model.add(
        sum(x[worker, j] * task_sizes[j] for j in range(num_tasks)) <= total_size_max
    )

for task in range(num_tasks):
    model.add_exactly_one(x[i, task] for i in range(num_workers))

objective_term = []
for worker in range(num_workers):
    for task in range(num_tasks):
        objective_term.append(x[worker, task] * costs[worker][task])
model.minimize(sum(objective_term))

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