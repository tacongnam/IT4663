from ortools.sat.python import cp_model

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
    model = cp_model.CpModel()

    x = {}
    for item in range(data['num_items']):
        for bin in range(data['num_bins']):
            x[item, bin] = model.new_bool_var(f'{item}_{bin}')

    for item in range(data['num_items']):
        model.add_at_most_one(x[item, j] for j in range(data['num_bins']))
    
    for bin in range(data['num_bins']):
        model.add(
            sum(x[i, bin] * data['weights'][i] for i in range(data['num_items'])) <= data['bin_capacities'][bin]
        )
    
    objective_term = []
    for item in range(data['num_items']):
        for bin in range(data['num_bins']):
            objective_term.append(cp_model.LinearExpr.term(x[item, bin], data['values'][item]))
    model.maximize(cp_model.LinearExpr.sum(objective_term))

    solver = cp_model.CpSolver()
    status = solver.solve(model)

    if status == cp_model.OPTIMAL:
        total_weight = 0
        for b in data["all_bins"]:
            print(f"Bin {b}")
            bin_weight = 0
            bin_value = 0
            for i in data["all_items"]:
                if solver.value(x[i, b]) > 0:
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

if __name__ == '__main__':
    main()