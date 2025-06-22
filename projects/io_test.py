from io import StringIO

def parse_input(input_str):
    """
    Đọc và phân tích dữ liệu đầu vào từ một chuỗi.
    """
    # Sử dụng StringIO để đọc chuỗi như một file
    f = StringIO(input_str)

    T, N, M = map(int, f.readline().strip().split())

    # Đọc danh sách môn học của từng lớp (1-indexed)
    class_subjects = {}
    for i in range(1, N + 1):
        # Đọc dòng, loại bỏ số 0 ở cuối
        subjects = list(map(int, f.readline().strip().split()))[:-1]
        class_subjects[i] = subjects

    # Đọc danh sách môn học mỗi giáo viên có thể dạy (1-indexed)
    teacher_subjects = {}
    for t in range(1, T + 1):
        subjects = list(map(int, f.readline().strip().split()))[:-1]
        teacher_subjects[t] = subjects

    # Đọc số tiết của mỗi môn (1-indexed)
    durations = list(map(int, f.readline().strip().split()))
    subject_duration = {m + 1: durations[m] for m in range(M)}

    return T, N, M, class_subjects, teacher_subjects, subject_duration

def print_solution(solution):
    """
    In giải pháp theo định dạng đầu ra yêu cầu.
    Solution là một danh sách các dictionary.
    """
    if not solution:
        print(0)
        return
        
    print(len(solution))
    # Sắp xếp để output ổn định
    solution.sort(key=lambda s: (s['class'], s['subject']))
    for s in solution:
        print(f"{s['class']} {s['subject']} {s['start']} {s['teacher']}")
