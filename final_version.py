import numpy as np
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


