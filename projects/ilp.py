import pulp

def solve_with_ilp(T, N, M, class_subjects, teacher_subjects, subject_duration, MAX_TIME_LIMIT):
    print("--- Solving with Integer Linear Programming (ILP) ---")
    model = pulp.LpProblem("School_Timetabling_ILP", pulp.LpMaximize)
    time_slots = range(1, 61)
    
    x = {}
    for i in range(1, N + 1):
        for j in class_subjects[i]:
            for k in range(1, T + 1):
                if j in teacher_subjects[k]:
                    duration = subject_duration[j]
                    for p in time_slots:
                        if p + duration - 1 <= 60:
                            var_name = f'x_{i}_{j}_{k}_{p}'
                            x[i, j, k, p] = pulp.LpVariable(var_name, cat=pulp.LpBinary)

    model += pulp.lpSum(x.values()), "Maximize_Scheduled_Classes"

    for i in range(1, N + 1):
        for j in class_subjects[i]:
            model += pulp.lpSum(x.get((i, j, k, p)) for k in range(1, T + 1) for p in time_slots if (i, j, k, p) in x) <= 1

    for i in range(1, N + 1):
        for q in time_slots:
            model += pulp.lpSum(x.get((i, j, k, p)) 
                               for j in class_subjects[i] 
                               for k in range(1, T + 1)
                               for p in range(max(1, q - subject_duration.get(j, 100) + 1), q + 1)
                               if (i, j, k, p) in x) <= 1

    for k in range(1, T + 1):
        for q in time_slots:
            model += pulp.lpSum(x.get((i, j, k, p)) 
                               for i in range(1, N + 1)
                               for j in teacher_subjects.get(k, [])
                               for p in range(max(1, q - subject_duration.get(j, 100) + 1), q + 1)
                               if (i, j, k, p) in x) <= 1

    model.solve(pulp.PULP_CBC_CMD(
        msg=1,
        timeLimit=MAX_TIME_LIMIT,
        options=[
            '-maxNodes', '10000',
            '-ratioGap', '0.05',
            '-heuristics', 'on',
            '-preprocess', 'on'
        ]
    ))

    solution = []
    if model.status == pulp.LpStatusOptimal:
        for var in x.values():
            if var.value() == 1:
                parts = var.name.split('_')
                i, j, k, p = map(int, parts[1:])
                solution.append({'class': i, 'subject': j, 'teacher': k, 'start': p})
    return len(solution)
