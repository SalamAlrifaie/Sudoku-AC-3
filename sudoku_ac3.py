import sys
from collections import deque
import copy

class CSP:
    def __init__(self, variables, domains, neighbors):
        """
        Initializes the CSP.
        parameters- 
        variables: A list of variables.
        domains: A dictionary mapping variables to their domains.
        neighbors: A dictionary mapping variables to their neighbors.
        """
        self.variables = variables
        self.domains = domains
        self.neighbors = neighbors

def parse_sudoku(file_path):
    """
    Parses the Sudoku puzzle from a text file.
    parameters-
    file_path: Path to the input file.
    returns- A CSP object representing the Sudoku puzzle.
    """
    rows = 'ABCDEFGHI'
    cols = '123456789'
    variables = [r + c for r in rows for c in cols]
    domains = {var: set('123456789') for var in variables}
    neighbors = {var: set() for var in variables}

    # read the input file sudoku.txt
    with open(file_path, 'r') as f:
        lines = f.readlines()
        if len(lines) != 9:
            raise ValueError("Input file must have exactly 9 lines.")
        for i, line in enumerate(lines):
            parts = line.strip().split()
            if len(parts) != 9:
                raise ValueError(f"Line {i+1} must have exactly 9 characters.")
            for j, val in enumerate(parts):
                var = rows[i] + cols[j]
                if val in '123456789':
                    domains[var] = set(val)
                elif val in '.0':
                    continue
                else:
                    raise ValueError(f"Invalid character '{val}' in input.")

    # Define the neighbors of each variable
    for var in variables:
        row, col = var[0], var[1]
        # Row neighbors
        row_vars = [row + c_j for c_j in cols if row + c_j != var]
        # Column neighbors
        col_vars = [r_j + col for r_j in rows if r_j + col != var]
        # Box neighbors
        # Determine the top-left corner of the box
        box_row_start = chr(((ord(row) - ord('A')) // 3) * 3 + ord('A'))
        box_col_start = str(((int(col) - 1) // 3) * 3 + 1)
        box_vars = []
        for r in range(ord(box_row_start), ord(box_row_start) + 3):
            for c in range(int(box_col_start), int(box_col_start) + 3):
                cell = chr(r) + str(c)
                if cell != var:
                    box_vars.append(cell)
        # Combine all neighbors and remove duplicates
        neighbors[var] = set(row_vars + col_vars + box_vars)

    return CSP(variables, domains, neighbors)

def AC3(csp):
    """
    Implements the AC-3 algorithm.
    parameters-
    csp: The CSP object.
    returns- (is_consistent, csp)
             is_consistent: False if inconsistency is found, True otherwise.
             csp: The potentially revised CSP.
    """
    queue = deque()
    # Initialize queue with all arcs
    for xi in csp.variables:
        for xj in csp.neighbors[xi]:
            queue.append((xi, xj))
    
    print(f"Initial queue length: {len(queue)}")
    
    step = 0
    while queue:
        xi, xj = queue.popleft()
        step += 1
        print(f"\nStep {step}: Processing arc ({xi}, {xj})")
        print(f"Current queue length: {len(queue)}")
        if Revise(csp, xi, xj):
            if not csp.domains[xi]:
                print(f"Domain of {xi} has been emptied. No solution exists.")
                return False, csp
            for xk in csp.neighbors[xi]:
                if xk != xj:
                    queue.append((xk, xi))
                    print(f"Added arc ({xk}, {xi}) to the queue")
    return True, csp

def Revise(csp, xi, xj):
    """
    Revise the domain of xi to enforce arc consistency with xj.
    parameters-
    csp: The CSP object.
    xi: Variable Xi.
    xj: Variable Xj.
    returns- True if the domain of xi was revised, False otherwise.
    """
    revised = False
    to_remove = set()
    for x in csp.domains[xi]:
        # If no value y in Dj allows (x,y) to satisfy the constraint, remove x from Di
        if not any(y != x for y in csp.domains[xj]):
            to_remove.add(x)
    if to_remove:
        csp.domains[xi] -= to_remove
        revised = True
        print(f"Revised domain of {xi}: removed {to_remove}")
    return revised

def is_solved(csp):
    """
    Checks if the CSP is solved.
    parameters-
    csp: The CSP object.
    returns- True if every variable has a singleton domain, False otherwise.
    """
    return all(len(domain) == 1 for domain in csp.domains.values())

def select_unassigned_variable(csp):
    """
    Selects an unassigned variable using the Minimum Remaining Values (MRV) heuristic.
    parameters-
    csp: The CSP object.
    returns- A variable with the smallest domain size greater than one.
    """
    unassigned = [v for v in csp.variables if len(csp.domains[v]) > 1]
    # MRV heuristic
    return min(unassigned, key=lambda var: len(csp.domains[var]), default=None)

def backtrack(csp):
    """
    Implements the backtracking search algorithm.
    parameters-
      csp: The CSP object.
    returns- A solved CSP or False if no solution exists.
    """
    if is_solved(csp):
        return csp
    
    var = select_unassigned_variable(csp)
    if var is None:
        return False
    
    for value in sorted(csp.domains[var]):
        new_csp = copy.deepcopy(csp)
        new_csp.domains[var] = set(value)
        print(f"\nBacktracking: Trying {var} = {value}")
        is_consistent, revised_csp = AC3(new_csp)
        if is_consistent:
            result = backtrack(revised_csp)
            if result:
                return result
    return False

def print_solution(csp):
    """
    Prints the Sudoku solution in a readable format.
    parameters-
    csp: The CSP object.
    """
    if not is_solved(csp):
        print("No solution found.")
        return
    rows = 'ABCDEFGHI'
    cols = '123456789'
    for r in rows:
        row = []
        for c in cols:
            row.append(next(iter(csp.domains[r + c])))
        print(' '.join(row))

def main(file_path):
    """
    Main function to solve the Sudoku puzzle using AC-3 and backtracking.
    parameters-
      file_path: Path to the input Sudoku file.
    """
    csp = parse_sudoku(file_path)
    print("Parsed Sudoku puzzle and initialized CSP.")
    
    # Apply AC-3
    print("\nStarting AC-3 algorithm...")
    is_consistent, revised_csp = AC3(csp)
    
    if not is_consistent:
        print("Sudoku puzzle has no solution.")
        return
    
    if is_solved(revised_csp):
        print("\nSudoku puzzle is solved by AC-3.")
        print_solution(revised_csp)
    else:
        print("\nAC-3 completed. Puzzle is not fully solved. Applying backtracking...")
        solution = backtrack(revised_csp)
        if solution:
            print("\nSudoku puzzle solved with backtracking:")
            print_solution(solution)
        else:
            print("Sudoku puzzle has no solution.")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python sudoku_ac3.py <path_to_sudoku_input_file>")
    else:
        main(sys.argv[1])
