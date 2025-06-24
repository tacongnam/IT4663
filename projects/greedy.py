# 2.3. Thuật toán Tham lam (Greedy)
def solve_with_greedy(T, N, M, class_subjects, teacher_subjects, subject_duration, MAX_TIME_LIMIT):
    print("--- Solving with Greedy Algorithm ---")
    jobs = []
    for i in range(1, N + 1):
        for j in class_subjects[i]:
            jobs.append({'class': i, 'subject': j})

    def get_teacher_count(subject_id):
        return sum(1 for k in range(1, T + 1) if subject_id in teacher_subjects.get(k, []))

    jobs.sort(key=lambda x: (-subject_duration[x['subject']], get_teacher_count(x['subject'])))

    class_schedule = {i: [False] * 61 for i in range(1, N + 1)}
    teacher_schedule = {k: [False] * 61 for k in range(1, T + 1)}
    solution = []
    
    for job in jobs:
        i, j = job['class'], job['subject']
        duration = subject_duration[j]
        is_scheduled = False
        possible_teachers = [k for k in range(1, T + 1) if j in teacher_subjects.get(k, [])]
        
        for k in possible_teachers:
            for p in range(1, 61 - duration + 1):
                is_class_free = all(not class_schedule[i][t] for t in range(p, p + duration))
                is_teacher_free = all(not teacher_schedule[k][t] for t in range(p, p + duration))
                
                if is_class_free and is_teacher_free:
                    for t in range(p, p + duration):
                        class_schedule[i][t] = True
                        teacher_schedule[k][t] = True
                    
                    solution.append({'class': i, 'subject': j, 'teacher': k, 'start': p})
                    is_scheduled = True
                    break
            if is_scheduled:
                break
    return len(solution)