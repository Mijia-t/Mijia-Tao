import copy
import os

class Solution:
    def __init__(self, grid, blockAvailable, lasers, targets, name):
        '''

        Initializes the solution class.

        Parameters
        ----------
        grid : list of str
            The game grid layout.
        blockAvailable : list of int
            List of counts for each block type.
        lasers : list of tuple
            List of laser start positions and directions.
        targets : list of tuple
            List of target points.
        name : str
            The file name to save the solution.

        Returns
        -------
        None.

        '''
        self.blockType = len(blockAvailable)
        self.laserQueue = lasers
        self.blockAvailable = blockAvailable
        
        # Doubling the grid size helps track the laser path and reflections more accurately.
        self.M = 2 * len(grid)
        self.N = 2 * len(grid[0])
        self.targets = targets
        self.name = name
        self.terminate = False
        self.grid = grid
        self.ans = None

    def solve(self):
        '''
        Begins the block placement and outputs the solution if found.

        Returns
        -------
        None.

        '''
        self.solvehelper(0, 0)
        self.printAns()

    def nextMove(self, i, j):
        '''
        Find the next cell to move to in the grid.
        Move to the next column in the same row.
        Or else move to the first column of the next row if at the end.

        Parameters
        ----------
        i : int
            Current row position.
        j : int
            Current column position.

        Returns
        -------
        tuple
            The next position (i, j) to move.
        '''
        return (i, j + 1) if j + 1 < len(self.grid[0]) else (i + 1, 0)

    def solvehelper(self, i, j):
        '''
        Try to place blocks and check the solution.
        If find the solution, then exit the function.
        If reach the end of the grid rows;
        check if blocks are all placed and if the solution is valid;
        If so, save a copy of the solution.
        Get the next cell position and skip the cell that cannot have a block placed.
        Save the original cell then try every available type in the current cell.

        Parameters
        ----------
        i : int
            Current row position.
        j : int
            Current column position.

        Returns
        -------
        None.
        '''
        if self.terminate:
            return
        if i >= len(self.grid):
            if sum(self.blockAvailable) == 0 and self.checkResult():
                self.ans = copy.deepcopy(self.grid)
            return

        nextI, nextJ = self.nextMove(i, j)
        self.solvehelper(nextI, nextJ)
        if self.grid[i][j] != 'o':
            return

        initialType = self.grid[i][j]
        for type in range(self.blockType):
            charType = chr(ord('A') + type)
            if self.blockAvailable[type] == 0:
                continue
            self.grid[i][j] = charType
            self.blockAvailable[type] -= 1
            self.solvehelper(nextI, nextJ)
            self.blockAvailable[type] += 1
            self.grid[i][j] = initialType

    def nextPassThrough(self, laser):
        '''
        Finds the next cell that the laser will pass through.

        Parameters
        ----------
        laser : tuple
            The current laser position and direction.

        Returns
        -------
        tuple
           The next cell position for the laser to pass through.
        '''
        nextI, nextJ = laser[0] + laser[2], laser[1] + laser[3]
        return int((nextI + laser[0]) / 2 // 2), int((nextJ + laser[1]) / 2 // 2)

    def moveLaser(self, laser, tempQueue, path):
        '''
        Moves the laser within the grid and tracks its path.
        
        Firsly, check the laser's next position, and stop the loop 
        if the laser goes out of grid bounds.
        Then calculate the position in different cases.
        After that update the laser to move to its next position.

        Parameters
        ----------
        laser : tuple
            The current position and direction of laser
        tempQueue : list
            A list that tracks the laser's movement.
        path : set
            The set of positions that the laser has passed through

        Returns
        -------
        None.
        '''
        while True:
            path.add((laser[0], laser[1]))
            nextI, nextJ = laser[0] + laser[2], laser[1] + laser[3]
            if nextI > self.M or nextJ > self.N or nextI < 0 or nextJ < 0:
                break
            x, y = self.nextPassThrough(laser)
            passThroughType = self.grid[x][y]
            if passThroughType == 'A' or passThroughType == 'C':
                refI = int(nextI if (nextI % 2 == 0) else (2 * laser[0] - nextI))
                refJ = int(nextJ if (nextJ % 2 == 0) else (2 * laser[1] - nextJ))
                newLaser = (refI, refJ, refI - laser[0], refJ - laser[1])
                tempQueue.append(newLaser)
            if passThroughType == 'B' or passThroughType == 'A':
                break
            laser = (nextI, nextJ, laser[2], laser[3])

    def checkResult(self):
        '''
        Checks if all target points are hit by the laser paths.
        
        Firstly, process every laser path;
        then check if each target is in the path.

        Returns
        -------
        True if all targets are hit; False otherwise.
        '''
        path = set()
        tempQueue = copy.deepcopy(self.laserQueue)
        while len(tempQueue) > 0:
            laser = tempQueue.pop()
            self.moveLaser(laser, tempQueue, path)
        for target in self.targets:
            if target not in path:
                return False
        self.terminate = True
        return True

    def printAns(self):
        '''
        Saves the solution grid to a file; 
        prints a message if no solution is found otherwise.

        Returns
        -------
        None.
        '''
        base_name = os.path.splitext(self.name)[0]
        filename = base_name + '_solution.txt'
        if self.ans is None:
            print("No solution found.")
            with open(filename, 'w') as file:
                file.write("No solution found.\n")
        else:
            with open(filename, 'w') as file:
                for j in range(len(self.ans[0])):
                    for i in range(len(self.ans)):
                        file.write(f"{self.ans[i][j]} ")
                    file.write("\n")
                    
                    
                    
# Test                 
from file_reader import read_bff_file
# Load data
file_path = '/Users/mijia/Desktop/bff_files/mad_1.bff'
output_file_path = file_path.replace('.bff', '_solution.txt')
grid, blocks, lasers, targets = read_bff_file(file_path)

# Test and create a solution file
solution = Solution(grid, blocks, lasers, targets, file_path)
solution.solve()
solution.printAns()

if os.path.exists(output_file_path):
    print("Solution file creation successful.")

          
