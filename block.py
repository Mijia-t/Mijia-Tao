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
