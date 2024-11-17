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





# Test
from file_reader import read_bff_file
import os

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

      
