import os
import time
import copy
import numpy as np
from PIL import Image

def read_bff_file(file_path):
    '''
    Reads a '.bff' file to get grid, blocks, lasers, and target points.
    Buld a grid to mark the different block and position.
    Mark different types of blocks and calculate the number; 'A' as Reflect blocks; 'B' as Opaque blocks; 'C' as Refract blocks.
    Mark laser position and its direction.
    Mark the target points.

    Parameters
    ----------
    file_path: str
        Path to '.bff' files.

    Returns
    -------
    trans_grid : list of str
        Transposed grid showing each cell's content
    updated_blocks :  list of int
        Numbers of each block type: A, B, C.
    lasers : list of tuple
        Laser information for start position and direction.
    points : list of tuple
        Target points at (x, y) coordinates.

    '''

    # Initialize the data stracture
    grid = []
    blocks = {'A': 0, 'B': 0, 'C': 0}
    block_types = ['A', 'B', 'C']
    lasers = []
    points = []
    laser = 'L'
    point = "P"
    grid_start = 'GRID START'
    grid_stop = 'GRID STOP'

    # Read files
    with open(file_path, 'r') as file:
        for line in file:
            line = line.strip() # Remove white sapce
            if not line:
                continue # Skip empty lines

            # store lines in grid
            if line == grid_start:
                for line in file:
                    line = line.strip()
                    if line == grid_stop:
                        break
                    if line:
                        grid.append(line)

            # store lines in blocks if it starts with 'A', 'B', 'C' 
            elif line[0] in block_types:
                current_block, count = line.split()
                blocks[current_block] = int(count)

            # store lines in lasor if it starts with 'L'
            elif line[0] == laser:
                _, x, y, vx, vy = line.split()
                lasers.append((int(x), int(y), int(vx), int(vy)))

            # store lines in target points if it starts with "P"
            elif line[0] == 'P':
                _, x, y, = line.split()
                points.append((int(x), int(y)))

    # Update the data
    # Convert grid indices (i, j) (row, column) to coordinates (x, y), 
    # where (x = j) (horizontal) and (y = i) (vertical).
    updated_grid = [row.split() for row in grid]
    updated_blocks = [blocks[num] for num in ['A', 'B', 'C']]
    trans_grid = np.transpose(updated_grid)

    return trans_grid, updated_blocks, lasers, points

class Block:
    def __init__(self, block_type, position):
        '''
        Initializes a block object with a specified type and position.

        Parameters
        ----------
        block_type : str
            The type includes 'reflect', 'opaque', or 'refract'.
        position : tuple
            The (x, y) coordinates representing the position on the grid.

        Returns
        -------
        None
        '''
        self.block_type = block_type
        self.position = position
        
        
    def interact_with_laser(self, laser):
            
        '''
        Defines how the block interacts with a laser.
        
        Parameters
        ----------
        laser : laser type
            The laser interacting with the block, which has a direction.

        Raises
        ------
        ValueError
            If the block type is not known.

        Returns
        -------
        Tuple or None
            A tuple showing the new laser direction after hitting the block
            None if the laser stops at an opaque block.

        '''
        
        if self.block_type == 'reflect':
            return self.reflect_laser(laser.direction)
        
        # Laser stops at an opaque block
        elif self.block_type == 'opaque':
            return None
        
        elif self.block_type == 'refract':
            return self.refract_laser(laser.direction)
        
        # Value error if can not read the block type
        else:
            raise ValueError(f"Unknown block type: {self.block_type}")

    def reflect_laser(self, direction):
        '''
        Changes the laser’s direction if it is reflected.

        Parameters
        ----------
        direction : tuple
            The direction of the laser before hitting the block.

        Returns
        -------
        tuple
            The direction after reflection.


        '''
        return (-direction[0], -direction[1])

    def refract_laser(self, direction):
        '''
        Allows the laser passing through if it is refracted.

        Parameters
        ----------
        direction : tuple
            The direction of the laser.

        Returns
        -------
        list
            The same direction of the laser.

        '''
        return [direction]
        
    def __str__(self):
        '''
        Get the block's type and position information.

        Returns
        -------
        str
            A string contains info about block's type and position.

        '''
        return f"Block(type={self.block_type}, position={self.position})"

class GridImage:
    def __init__(self, grid, lasers, points, file_path):
        '''
        Sets up the GridImage.
        
        Parameters
        ----------
        grid : list of str
            A 2D list shows the grid layout
        lasers : list of tuple
            List of laser start points
        points : list of tuple
            List of target points
        file_path : str
            The path of saving image

        Returns
        -------
        None.

        '''
        self.grid = grid
        self.lasers = lasers
        self.points = points
        self.file_path = file_path

    def build_image(self):
        '''
        Creates and saves an image of the grid, lasers, and points.

        Returns
        -------
        None.

        '''
        
        # Creat the image
        img = Image.new(mode="RGB", size=(100, 100))
        
        # Draw the grid and color the cells, black as 'x' , white as 'o'
        x = 0
        for i in self.grid:
            y = 0
            string = i.split(' ')
            for j in string:
                color = (0, 0, 0) if j == 'x' else (255, 255, 255)
                img.putpixel((10 * x, 10 * y), color)
                y += 1
            x += 1
            
        # Draw the laser and color it as red
        for laser in self.lasers:
            x, y = laser[:2]
            img.putpixel((10 * x, 10 * y), (255, 0, 0))
            
        # Draw the target points and color it as green
        for x, y in self.points:
            img.putpixel((10 * x, 10 * y), (0, 255, 0))
            
        # Save the updated image
        img.save(self.file_path + '.png')

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
                    
base_dir = '/Users/mijia/Desktop/bff_files'
file_names = ["yarn_5.bff", "tiny_5.bff", "numbered_6.bff", "mad_1.bff", "mad_7.bff", "mad_4.bff", "dark_1.bff"]

if __name__ == "__main__":
    # Store runtime for each file
    times = []
    
    for name in file_names:
        file_path = os.path.join(base_dir, name)
        
        # Start timer
        t0 = time.time()
        
        # Read data and get the solution
        grid, blockAvailable, lasers, targets = read_bff_file(file_path)
        sol = Solution(grid, blockAvailable, lasers, targets, file_path)
        sol.solve()
        
        # End timer
        t1 = time.time()
        
        times.append(t1 - t0)
        print(f"File: {name}, Time: {t1 - t0} seconds")
                
# Other Test
if __name__ == '__main__':
    file_path = '/Users/mijia/Desktop/bff_files/mad_1.bff'
    grid, block_available, lasers, points = read_bff_file(file_path)
    print(f"Successfully read {file_path}")
    
    # Test Block Initialization
    block = Block('reflect', (1, 1))
    if block.block_type == 'reflect' and block.position == (1, 1):
        print("Initialization test passed.")

    # Test Reflect Block Interaction
    laser = type('Laser', (object,), {'direction': (1, 1)})
    reflected_direction = block.interact_with_laser(laser)
    if reflected_direction == (-1, -1):
        print("Reflect interaction test passed.")

    # Test Opaque Block Interaction
    opaque_block = Block('opaque', (2, 2))
    laser_stopped = opaque_block.interact_with_laser(laser)
    if laser_stopped is None:
        print("Opaque interaction test passed.")

    # Test Refract Block Interaction
    refract_block = Block('refract', (3, 3))
    refracted_direction = refract_block.interact_with_laser(laser)
    if refracted_direction == [laser.direction]:
        print("Refract interaction test passed.")

    # Define file paths
    file_path = '/Users/mijia/Desktop/bff_files/mad_1.bff'
    output_image_path = '/Users/mijia/Desktop/bff_files/mad_1_image'

    # Read the .bff file
    grid, blocks, lasers, points = read_bff_file(file_path)

    # Convert grid to the format expected by GridImage
    grid_for_image = [' '.join(row) for row in grid]

    # Create the image
    grid_image = GridImage(grid_for_image, lasers, points, output_image_path)
    grid_image.build_image()

if os.path.exists(output_image_path + '.png'):
    print("Image creation successful.")

                
