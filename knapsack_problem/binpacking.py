from ortools.linear_solver import pywraplp

def create_data_model():
    """Create the data for the example."""
    data = {}
    weights = [48, 30, 19, 36, 36, 27, 42, 42, 36, 24, 30]
    data["weights"] = weights
    data["items"] = list(range(len(weights)))
    data["bins"] = data["items"]
    data["bin_capacity"] = 100
    return data

def main():
    data = create_data_model()

    solver = pywraplp.Solver.CreateSolver('SCIP')
    
    x = {}
    for i in data['items']:
        for j in data['bins']:
            x[(i, j)] = solver.IntVar(0, 1, f'{i}_{j}')
    
    y = {}
    for j in data['bins']:
        y[j] = solver.IntVar(0, 1, f'{j}')

    for i in data['items']:
        solver.Add(
            sum(x[i, j] for j in data['bins']) == 1
        )

    for j in data['bins']:
        solver.Add(
            sum(x[(i, j)] * data['weights'][i] for i in data['items']) <= y[j] * data['bin_capacity']
        )
    
    solver.Minimize(solver.Sum([y[j] for j in data['bins']]))

    status = solver.Solve()
    if status == pywraplp.Solver.OPTIMAL:
        num_bins = 0
        for j in data["bins"]:
            if y[j].solution_value() == 1:
                bin_items = []
                bin_weight = 0
                for i in data["items"]:
                    if x[i, j].solution_value() > 0:
                        bin_items.append(i)
                        bin_weight += data["weights"][i]
                if bin_items:
                    num_bins += 1
                    print("Bin number", j)
                    print("  Items packed:", bin_items)
                    print("  Total weight:", bin_weight)
                    print()
        print()
        print("Number of bins used:", num_bins)
        print("Time = ", solver.WallTime(), " milliseconds")
    else:
        print("The problem does not have an optimal solution.")
    
if __name__ == '__main__':
    main()