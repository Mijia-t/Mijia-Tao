# Lazor Project

# Overview
This project is used to solve the Lazor game by using python language. In the lazor game, it needs to guide a laser beam arond a grid to hit a target, 
which may require it to go around and bounce off different types of blocks.
The project includes a script that automatically finds a solution to place blocks in efficient location to guide the laser to the target points.

# How to Use
1. Requirements : make sure python installed on the computer.
2. Prepare : download final_version.py and .bff files.
3. Run final_version.py. The program will read the .ff files, solve the puzzles, and get the answer.
4. Output: save the solution files in .txt format.

# Input 
1. Grid:
   'o': Empty (can place blocks).
   'x': Fixed (blocks cannot be placed).
2. Blocks: 'A': reflective, 'B': opaque, 'C': refractive.
3. Lasers: 'L': start position and direction.
4. Targets: 'P': points to hit.

# Progress
1. Reads the .bff file to extract:
   Grid layout, laser positions/directions, target points, and available block counts.
2. Implements a backtracking algorithm to place blocks efficiently.
3. Strategically prioritizes placements to hit all targets.
4. Stops once all targets are hit and blocks are used, recording the solution.
5. Saves block placements in a .txt file.
6. Logs the solving time for each puzzle in the terminal.   








