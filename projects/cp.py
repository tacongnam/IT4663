from ortools.sat.python import cp_model

def solve_with_cp(T, N, M, class_subjects, teacher_subjects, subject_duration, MAX_TIME_LIMIT):
    print("--- Solving with Constraint Programming (CP) ---")
    model = cp_model.CpModel()
    horizon = 60

    tasks = {}
    
    for i in range(1, N + 1):
        for j in class_subjects[i]:
            for k in range(1, T + 1):
                if j in teacher_subjects.get(k, []):
                    duration = subject_duration[j]
                    is_present = model.NewBoolVar(f'present_{i}_{j}_{k}')
                    start_var = model.NewIntVar(1, horizon - duration + 1, f'start_{i}_{j}_{k}')
                    interval = model.NewOptionalIntervalVar(start_var, duration, start_var + duration,
                                                             is_present, f'interval_{i}_{j}_{k}')
                    tasks[(i, j, k)] = {'interval': interval, 'present': is_present, 'start': start_var}

    objective_vars = []
    for i in range(1, N + 1):
        for j in class_subjects[i]:
            possible_tasks = [tasks[key]['present'] for key in tasks if key[0] == i and key[1] == j]
            if possible_tasks:
                is_scheduled = model.NewBoolVar(f'scheduled_{i}_{j}')
                model.Add(sum(possible_tasks) == is_scheduled)
                objective_vars.append(is_scheduled)

    for i in range(1, N + 1):
        intervals_for_class = [tasks[key]['interval'] for key in tasks if key[0] == i]
        if intervals_for_class:
            model.AddNoOverlap(intervals_for_class)

    for k in range(1, T + 1):
        intervals_for_teacher = [tasks[key]['interval'] for key in tasks if key[2] == k]
        if intervals_for_teacher:
            model.AddNoOverlap(intervals_for_teacher)

    model.Maximize(sum(objective_vars))

    solver = cp_model.CpSolver()
    solver.parameters.max_time_in_seconds = MAX_TIME_LIMIT
    status = solver.Solve(model)

    solution = []
    if status == cp_model.OPTIMAL or status == cp_model.FEASIBLE:
        for (i, j, k), task_vars in tasks.items():
            if solver.BooleanValue(task_vars['present']):
                start_time = solver.Value(task_vars['start'])
                solution.append({'class': i, 'subject': j, 'teacher': k, 'start': start_time})
    return len(solution)


