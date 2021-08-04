from dataclasses import dataclass

@dataclass
class Context:
    data: list
    idx: int


class Backtracking:
    def init_solution(ctx):
        pass

    def _str(ctx):
        return " ".join(ctx.data)

    def _next_nodes(ctx):
        return ctx.data[ctx.idx + 1]

    def _allowed(ctx, solution):
        # beyond boundaries
        if ctx.i ==  len(ctx.data)):
            return False

        # blocked
        #  ...

        # visited?
        if solution[ctx.idx]:
            return False
        return True

    def _done(ctx, solution):
        if i == (len(ctx.data) - 1):
            print(self._str(solution))
            return True
        return False


    def _process_node(ctx, solution):
        if not self._allowed(ctx, solution):
            return
        solution[row][col] = 1
        if self._done(ctx, solution):
            solution[row][col] = 0
            return

        for c in _next_nodes(ctx):
            self._process_node(c, solution)

        # all child nodes are checked.
        solution[row][col] = 0


if __name__ == "__main__":
    for l in [[1, 2, 3], [1, 1, 2]]:
        print("{} => {}".format(l, subsets(l)))
