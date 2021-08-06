# Back Tracking
* 2D question. Tree / Matrix / Graph.
    * depth first traversal
    * rollback when finish iteration of a branch
* Path may be blocked
* question: matrix / maze / sudoku, trie / tree / graph / subset

## key concept:
* data: matrix, or tree node
* solution / visited: may use the data, or clone / init of the data
    * update the solution / visited
    * rollback the solution: solution[row][col] = i => solution[row][col] = 0 / None
* next_nodes: children / directions to go in depth search
    * define the rules only
    * e.g., matrix: left / right / up / down
* allowed: check visited, boundary, or any other conditions
    * self allowed?
    * children allowed?
* traverse: depth first iteratiion
* done? stop iteration / log the solution

## google's OR tools
* combinatorial optimization
* https://developers.google.com/optimization/introduction/overview

## other references
* https://www.algotree.org/algorithms/backtracking/nqueens/
* https://fizzbuzzed.com/top-interview-questions-3/
* https://leetfree.com/
* https://www.techiedelight.com/