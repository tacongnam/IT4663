import sys
import time
import pandas as pd
from io_test import parse_input, print_solution
from greedy import solve_with_greedy
from branch import solve_with_bnb
from cp import solve_with_cp
from ilp import solve_with_ilp

def parse_input_file(path: str):
    with open(path, "r", encoding="utf-8") as f:
        raw = f.read().strip()
    return raw

if __name__ == "__main__":
    for test_id in range(11):
        print(f'Test {test_id}')
        records = []
        example_input = parse_input_file(f'tests/test{test_id}.txt')
        T, N, M, class_subjects, teacher_subjects, subject_duration = parse_input(example_input)

        # CP for benchmark
        t0 = time.perf_counter()
        cp_obj = solve_with_cp(T, N, M, class_subjects, teacher_subjects, subject_duration)
        cp_time = time.perf_counter() - t0
        cp_time = round(cp_time, 6)
        records.append({
            "instance": f'Test {test_id}',
            "method":   "CP",
            "objective": len(cp_obj),
            "time":      cp_time,
            "∆obj_vs_CP": 0.0,
            "speedup_vs_CP": 1.0,
        })

        #print(f'CP - objective: {len(cp_obj)} - time: {cp_time}')
    
        for name, fn in [("Greedy", solve_with_greedy),
                        ("ILP",    solve_with_ilp),
                        ("BnB",    solve_with_bnb)]:
            t0 = time.perf_counter()
            obj = fn(T, N, M, class_subjects, teacher_subjects, subject_duration)
            elapsed = time.perf_counter() - t0
            elapsed = round(elapsed, 6)
            records.append({
                "instance": f'Test {test_id}',
                "method":   name,
                "objective": len(obj),
                "time":      elapsed,
                "∆obj_vs_CP": len(obj) - len(cp_obj),
                "speedup_vs_CP": cp_time / elapsed if elapsed > 0 else float("inf"),
            })

            #print(f'CP - objective: {len(obj)} - time: {elapsed} - obj_vs_bm: {len(obj) - len(cp_obj)} - time_vs_bm: {cp_time / elapsed if elapsed > 0 else float("inf")}')

        df = pd.DataFrame(records)

        # sắp xếp cho dễ đọc
        df = df.sort_values(["instance", "method"])

        # nếu muốn làm tròn cột time:
        df["time"] = df["time"].round(6)

        # in dạng Markdown (terminal hỗ trợ màu & bảng kẻ, Jupyter cũng OK)
        print(df.to_markdown(index=False))