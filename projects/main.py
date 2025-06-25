import sys
import time
import pandas as pd
from io_test import parse_input, print_solution
from greedy import solve_with_greedy
from branch import solve_with_bnb
from cp import solve_with_cp
from ilp import solve_with_ilp
import gc
import argparse

MAX_TIME_LIMIT = 1800

def parse_input_file(path: str):
    with open(path, "r", encoding="utf-8") as f:
        raw = f.read().strip()
    return raw

parser = argparse.ArgumentParser(description='Input')
parser.add_argument('--limit', metavar='limit', type=int, dest="limit",
                    help='MAX_TIME_LIMIT', default=1800)
parser.add_argument('--tmin', metavar='tmin', type=int, dest="tmin",
                    help='Start testing from ...', default=0)
parser.add_argument('--tmax', metavar='tmax', type=int, dest='tmax',
                    help='to ...', default=10)
parser.add_argument('--inv', metavar='inv', type=bool, dest='inv',
                    help='Testing inverse?', default=False)
parser.add_argument('--algo', metavar='algo', type=str, dest='algo',
                    help='[c (cp - benchmark) ; g (greedy) ; b (branch and bound) ; i (ilp)]', default='cgbi')

args = parser.parse_args()

algo_mapping = {
    'g': 'Greedy',
    'i': 'ILP',
    'b': 'BnB'
}

if __name__ == "__main__":
    inc = 0
    if args.inv == True:
        inc = -1
        args.tmin, args.tmax = args.tmax, args.tmin
    else:
        inc = 1

    for test_id in range(args.tmin, args.tmax, inc):
        print(f'Test {test_id}')
        records = []
        example_input = parse_input_file(f'tests/test{test_id}.txt')
        T, N, M, class_subjects, teacher_subjects, subject_duration = parse_input(example_input)

        # CP for benchmark
        t0 = time.perf_counter()
        cp_obj = solve_with_cp(T, N, M, class_subjects, teacher_subjects, subject_duration, MAX_TIME_LIMIT)
        cp_time = time.perf_counter() - t0
        cp_time = round(cp_time, 6)
        records.append({
            "instance": f'Test {test_id}',
            "method":   "CP",
            "objective": cp_obj,
            "time":      cp_time,
            "∆obj_vs_CP": 0.0,
            "speedup_vs_CP": 1.0,
        })

        #print(f'CP - objective: {len(cp_obj)} - time: {cp_time}')
    
        for name, fn in [("Greedy", solve_with_greedy),
                        ("ILP", solve_with_ilp),
                        ("BnB",    solve_with_bnb)]:
            if not any(char in algo_mapping and algo_mapping[char] == name for char in args.algo):
                continue
                
            t0 = time.perf_counter()
            obj = fn(T, N, M, class_subjects, teacher_subjects, subject_duration, MAX_TIME_LIMIT)
            elapsed = time.perf_counter() - t0
            elapsed = round(elapsed, 6)
            records.append({
                "instance": f'Test {test_id}',
                "method":   name,
                "objective": obj,
                "time":      elapsed,
                "∆obj_vs_CP": obj - cp_obj,
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

        gc.collect()
