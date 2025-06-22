from ortools.linear_solver import pywraplp

data = {}
data["weights"] = [48, 30, 42, 36, 36, 48, 42, 42, 36, 24, 30, 30, 42, 36, 36]
data["values"] = [10, 30, 25, 50, 35, 30, 15, 40, 30, 35, 45, 10, 20, 30, 25]
assert len(data["weights"]) == len(data["values"])
data["num_items"] = len(data["weights"])
data["all_items"] = range(data["num_items"])

data["bin_capacities"] = [100, 100, 100, 100, 100]
data["num_bins"] = len(data["bin_capacities"])
data["all_bins"] = range(data["num_bins"])

def main():
    solver = pywraplp.Solver.CreateSolver('SCIP')
    if solver is None:
        print('SCIP solver unavailable')
        return 

    x = {}
    for item in range(data['num_items']):
        for bin in range(data['num_bins']):
            x[item, bin] = solver.IntVar(0, 1, f'{item}_{bin}')

    for item in range(data['num_items']):
        solver.Add(
            sum(x[item, j] for j in range(data["num_bins"])) <= 1
        )
    
    for bin in range(data['num_bins']):
        solver.Add(
            sum(x[i, bin] * data['weights'][i] for i in range(data['num_items'])) <= data['bin_capacities'][bin]
        )
    
    objective_term = solver.Objective()
    for item in range(data['num_items']):
        for bin in range(data['num_bins']):
            objective_term.SetCoefficient(x[item, bin], data['values'][item])
    objective_term.SetMaximization()

    status = solver.Solve()

    if status == pywraplp.Solver.OPTIMAL:
        total_weight = 0
        for b in data["all_bins"]:
            print(f"Bin {b}")
            bin_weight = 0
            bin_value = 0
            for i in data["all_items"]:
                if x[i, b].solution_value() > 0:
                    print(
                        f"Item {i} weight: {data['weights'][i]} value:"
                        f" {data['values'][i]}"
                    )
                    bin_weight += data["weights"][i]
                    bin_value += data["values"][i]
            print(f"Packed bin weight: {bin_weight}")
            print(f"Packed bin value: {bin_value}\n")
            total_weight += bin_weight
        print(f"Total packed weight: {total_weight}")
    else:
        print("The problem does not have an optimal solution.")

if __name__ == "__main__":
    main()