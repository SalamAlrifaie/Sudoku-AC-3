# Sudoku AC-3 Algorithm
*Implements the AC-3 algorithm to enforce arc-consistency to an arbitrary Sudoku puzzle.*

## Binary Constraints 
*For each pair of squares (Ai,Aj) in the Sudoku grid that shares the same row, column, or 3x3 box, impose a binary constraint that ensures their values are different. i.e.:  Ai != Aj*

## Input Format
*The sudoku puzzle will be inputted as a .txt file containing exactly 9 lines, each line has 9 characters separated by spaces, representing 9 rows with 9 squares (81 characters in total).
Filled cells are represented by digits 1 to 9. Empty cells are represented by dots (.) An example txt input file is provided*

## CSP Representation
- Variables: each cell in the puzzle
- Domains: the possible values for each variable (range 1-9). Filled cells have a single (given) value in their domain.
- Constraints: binary constraints defined in part 1
- Neighbours: map each variable to the set of variables it shares constraints with

## Algorithm Implementation
*The code keeps track of and reports the queue length at each step of the AC-3 algorithm.*

**Additional Algorithm:** In case the AC-3 Algorithm fails to find a solution, the program will use **Backtracking Search**
*Implement an additional algorithm to solve the puzzle in case no solution is found by AC-3*

## Output
*The code will output a CSP object as well as the status of the queue on each step. The path to finding the solution will depend on which algorithm was used.*
*If the inputted sudoku puzzle can be solved with the AC-3 Algorithm, the program will output the solved sudoku puzzle*
*Otherwise, if the solution cannot be found using the AC-3 Algorithm, the program will use Backtracking search and report the solution*

