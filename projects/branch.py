import time

def solve_with_bnb(T, N, M, class_subjects, teacher_subjects, subject_duration):
    print("--- Solving with Branch and Bound (BnB) ---")
    print("(Note: This can be very slow for non-trivial inputs)")
    
    jobs = []
    for i in range(1, N + 1):
        for j in class_subjects[i]:
            jobs.append({'class': i, 'subject': j})

    jobs.sort(key=lambda x: -subject_duration[x['subject']])

    global best_solution_bnb
    best_solution_bnb = []

    start_time = time.perf_counter()
    
    def backtrack(job_index, current_solution, class_sched, teacher_sched):
        global best_solution_bnb

        if time.perf_counter() - start_time > 3600.0:
            return
        
        upper_bound = len(current_solution) + (len(jobs) - job_index)
        if upper_bound <= len(best_solution_bnb):
            return

        if job_index == len(jobs):
            if len(current_solution) > len(best_solution_bnb):
                best_solution_bnb = list(current_solution)
            return

        current_job = jobs[job_index]
        i, j = current_job['class'], current_job['subject']
        duration = subject_duration[j]

        # Nhánh 1: Không xếp lịch
        backtrack(job_index + 1, current_solution, class_sched, teacher_sched)
        
        # Nhánh 2..n: Thử xếp lịch
        possible_teachers = [k for k in range(1, T + 1) if j in teacher_subjects.get(k, [])]
        for k in possible_teachers:
            for p in range(1, 61 - duration + 1):
                is_class_free = all(not class_sched[i][t] for t in range(p, p + duration))
                is_teacher_free = all(not teacher_sched[k][t] for t in range(p, p + duration))

                if is_class_free and is_teacher_free:
                    # Gán
                    for t in range(p, p + duration):
                        class_sched[i][t] = True
                        teacher_sched[k][t] = True
                    current_solution.append({'class': i, 'subject': j, 'teacher': k, 'start': p})

                    # Đệ quy
                    backtrack(job_index + 1, current_solution, class_sched, teacher_sched)
                    
                    # Hoàn lại
                    current_solution.pop()
                    for t in range(p, p + duration):
                        class_sched[i][t] = False
                        teacher_sched[k][t] = False

    initial_class_sched = {i: [False] * 61 for i in range(1, N + 1)}
    initial_teacher_sched = {k: [False] * 61 for k in range(1, T + 1)}
    backtrack(0, [], initial_class_sched, initial_teacher_sched)
    
    return best_solution_bnb