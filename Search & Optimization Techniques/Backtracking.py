def solve_n_queens(n: int):
    solutions = []
    cols = set()        # columns that are already used
    diag1 = set()       # r - c diagonals in use
    diag2 = set()       # r + c diagonals in use
    board = ["." * n for _ in range(n)]
    board = [list(row) for row in board]

    def backtrack(row):
        # base case: placed queens in all rows
        if row == n:
            solutions.append(["".join(r) for r in board])
            return

        # try each column in this row
        for c in range(n):
            if c in cols or (row - c) in diag1 or (row + c) in diag2:
                # PRUNE: can't put queen here, it would conflict
                continue

            # choose
            cols.add(c)
            diag1.add(row - c)
            diag2.add(row + c)
            board[row][c] = "Q"

            # explore
            backtrack(row + 1)

            # un-choose (backtrack)
            cols.remove(c)
            diag1.remove(row - c)
            diag2.remove(row + c)
            board[row][c] = "."

    backtrack(0)
    return solutions
