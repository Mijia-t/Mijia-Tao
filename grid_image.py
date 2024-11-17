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
      
