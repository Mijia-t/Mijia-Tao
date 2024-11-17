import os
import copy

class Solution:
    def __init__(self, grid, block_available, lasers, targets, name):
        self.grid = grid
        self.block_available = block_available
        self.lasers = lasers
        self.targets = targets
        self.name = name
        self.terminate = False
        self.ans = None

    def solve(self):
        self.solve_helper(0, 0)
        self.print_solution()

    def solve_helper(self, i, j):
        if self.terminate:
            return
        if i >= len(self.grid):
            if sum(self.block_available) == 0 and self.check_result():
                self.ans = copy.deepcopy(self.grid)
                self.terminate = True
            return
        
        next_i, next_j = (i, j + 1) if j + 1 < len(self.grid[0]) else (i + 1, 0)
        self.solve_helper(next_i, next_j)

        if self.grid[i][j] == 'o':
            for b_type, count in enumerate(self.block_available):
                if count > 0:
                    self.grid[i][j] = chr(ord('A') + b_type)
                    self.block_available[b_type] -= 1
                    self.solve_helper(next_i, next_j)
                    self.block_available[b_type] += 1
                    self.grid[i][j] = 'o'

    def check_result(self):
        return True

    def print_solution(self):
        if self.ans:
            print("Solution found:")
            for row in self.ans:
                print(" ".join(row))
        else:
            print("No solution found.")
          
