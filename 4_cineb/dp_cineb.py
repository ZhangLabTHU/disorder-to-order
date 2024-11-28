# Import necessary libraries
import os  # For interacting with the operating system (e.g., file management)
import numpy as np  # For numerical operations
from ase.calculators.eam import EAM  # For the Embedded Atom Method (EAM) calculator (not used in this code, but imported)
from ase.io import read  # For reading structure files (e.g., VASP, POSCAR)
from ase.optimize import BFGS  # For the BFGS optimization algorithm
from ase.mep import NEB, NEBTools  # For Nudged Elastic Band (NEB) method and tools to analyze results
from deepmd.calculator import DP  # For the Deep Potential (DP) calculator
import warnings  # For suppressing warnings during execution

# Suppress all warnings
warnings.filterwarnings("ignore")

# Initialize the Deep Potential calculator with a pre-trained model
dp_calc = DP(model="dpa_sy_finetune.pb")

# Read initial and final atomic structures from VASP files
initial = read('is.vasp')  # Initial structure
final = read('fs.vasp')  # Final structure

# Ensure periodic boundary conditions (PBC) are set correctly for both initial and final structures
pbc = initial.get_pbc()  # Get the periodic boundary conditions from the initial structure
initial.set_pbc(pbc)  # Apply PBC to the initial structure
final.set_pbc(pbc)  # Apply PBC to the final structure

# Create the NEB images: These are intermediate structures between the initial and final configurations
images = [initial]  # Start with the initial structure
images += [initial.copy() for _ in range(3)]  # Create 3 intermediate copies of the initial structure
images += [final]  # Add the final structure

# Set PBC and cell parameters for each image to ensure consistency
for image in images:
    image.set_pbc(pbc)  # Apply the PBC to all images
    image.set_cell(initial.get_cell())  # Ensure all images have the same cell dimensions as the initial structure

# Initialize the NEB object with the created images and enable the "climbing" image feature (for transition states)
neb = NEB(images, climb=True)

# Interpolate the atomic positions of the middle images to generate an initial NEB path
neb.interpolate(mic=True)

# Set the Deep Potential calculator for each image
for image in images:
    image.calc = DP(model="dpa_sy_finetune_neb.pb")  # Assign the DP calculator with a different model for NEB

# Optimize the NEB path using the BFGS algorithm
traj_name = 'neb.traj'  # Define the name for the trajectory file to save optimization steps
optimizer = BFGS(neb, trajectory=traj_name)  # Initialize BFGS optimizer with NEB object and trajectory saving
optimizer.run(fmax=0.03, steps=300)  # Run the optimization with a force tolerance of 0.03 eV/Å and 300 steps
        
# Read the optimized NEB images from the trajectory file (last 5 images)
images = read(traj_name+'@-5:')  # Load the last 5 frames from the trajectory file
for image in images:
    image.calc = DP(model="dpa_sy_finetune.pb")  # Reassign the original DP calculator to the images after optimization

# Analyze the NEB results using the NEBTools
nebtools = NEBTools(images)  # Initialize NEBTools with the optimized images
Ea, dE = nebtools.get_barrier(fit=True)  # Calculate the activation energy barrier and its uncertainty (dE)
