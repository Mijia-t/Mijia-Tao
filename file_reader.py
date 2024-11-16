import numpy as np
def read_bff_file(file_path):
    '''
    Reads a '.bff' file to get grid, blocks, lasers, and target points.
    Buld a grid to mark the different block and position.
    Mark different types of blocks and calculate the number; 'A' as Reflect blocks; 'B' as Opaque blocks; 'C' as Refract blocks.
    Mark laser position and its direction.
    Mark the target points.

    Parameters
    file_path: str
        Path to '.bff' files.

    Returns

    '''

    # Initialize the data stracture
    grid = []
    blocks = {'A': 0, 'B': 0, 'C': 0}
    block_types = {'A', 'B', 'C'}
    lasers = []
    points = []
    laser = 'L'
    point = "p"
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
                block_types, count = line.split()
                blocks[block_types] = int(count)

            # store lines in lasor if it starts with 'L'
            elif line[0] == laser:
                _, x, y, vx, vy = line.spilt()
                lasers.append(int(x), int(y), int(vx), int(vy))

            # store lines in target points if it starts with "P"
            elif line[0] == 'P':
                _, x, y, = line.split()
                points.append(int(x), int(y))

    # Update the data
    updated_grid = [row.split() for row in grid]
    updated_blocks = [blocks[num] for num in ['A', 'B', 'C']]

    return updated_grid, updated_blocks, lasers, points

if __name__ == '__main__':
    file_path = '/bff_files/mad_1.bff'
    grid, block_available, lasers, points = read__bff_file(file_path)
    
















