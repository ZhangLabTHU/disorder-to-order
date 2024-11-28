# Import necessary libraries from ASE and other dependencies
from ase import atoms  # For atomic structures
from ase.io import read  # For reading structure files
import numpy as np  # For numerical operations
from ase import units  # For unit conversions
from ase import Atom, Atoms  # For creating atom and atom list objects
from ase.neighborlist import NeighborList  # For calculating the neighbor list of atoms
import random  # For random number generation
import math  # For mathematical operations
import os  # For interacting with the operating system (e.g., creating directories)
from deepmd.calculator import DP  # For the Deep Potential (DP) calculator
from ase.optimize import BFGS  # For optimization algorithm

# Read initial atomic structure from a POSCAR file
atoms_initial = read('POSCAR')  # Read atomic structure from POSCAR file
atoms = atoms_initial * [3, 3, 3]  # Replicate the structure to increase size (3x3x3)

# Set up the Deep Potential calculator with a trained model
calc = DP(model="dpa_sy_finetune.pb")  # Load a pre-trained Deep Potential model

# Re-read the initial structure from the POSCAR file (overwrites atoms from the previous line)
atoms = read('POSCAR')

# Define the radius for the neighbor list. This controls the cutoff for atom neighbors.
radius = [1.4] * len(atoms)  # Set a fixed radius of 1.4 for all atoms
nl = NeighborList(radius, self_interaction=False, bothways=True)  # Create NeighborList object
nl.update(atoms)  # Update the neighbor list based on the atom positions

# Initialize dictionaries to store neighbors and coordination numbers
neighbor_list = {}
coordination_list = {}

# Loop over all atoms to collect neighbors and coordination numbers
for index in range(len(atoms)):
    indices, offsets = nl.get_neighbors(index)  # Get the neighbors for atom at `index`
    indices = indices.tolist()  # Convert indices to a list
    neighbor_list[index] = indices  # Store neighbors for the atom at `index`
    coordination_list[index] = len(indices)  # Store the coordination number

# Function to calculate Short-Range Order (SRO) for different atom pairs
def get_sro(config_int=[], neighbor_list={}):
    # SRO for Co-Cu pairs
    SRO_co_cu = []
    ratio_cu = 0.25
    for i in range(len(config_int)):
        if config_int[i] == 1:  # If atom i is Co
            neighbor_i = neighbor_list[i]  # Get neighbors of Co atom
            neighbor_i_num_cu = [config_int[j] for j in neighbor_i].count(2)  # Count Cu neighbors
            sro = 1 - neighbor_i_num_cu / 12 / ratio_cu  # Calculate SRO
            SRO_co_cu.append(sro)
    sro_co_cu = np.mean(SRO_co_cu)  # Average SRO for Co-Cu

    # SRO for Pt-Cu pairs
    SRO_pt_cu = []
    ratio_cu = 0.25
    for i in range(len(config_int)):
        if config_int[i] == 0:  # If atom i is Pt
            neighbor_i = neighbor_list[i]
            neighbor_i_num_cu = [config_int[j] for j in neighbor_i].count(2)  # Count Cu neighbors
            sro = 1 - neighbor_i_num_cu / 12 / ratio_cu
            SRO_pt_cu.append(sro)
    sro_pt_cu = np.mean(SRO_pt_cu)  # Average SRO for Pt-Cu

    # SRO for Pt-Co pairs
    SRO_pt_co = []
    ratio_co = 0.25
    for i in range(len(config_int)):
        if config_int[i] == 0:  # If atom i is Pt
            neighbor_i = neighbor_list[i]
            neighbor_i_num_co = [config_int[j] for j in neighbor_i].count(1)  # Count Co neighbors
            sro = 1 - neighbor_i_num_co / 12 / ratio_co
            SRO_pt_co.append(sro)
    sro_pt_co = np.mean(SRO_pt_co)  # Average SRO for Pt-Co

    # SRO for Pt-M pairs (Co and Cu)
    SRO_pt_m = []
    ratio_m = 0.5
    for i in range(len(config_int)):
        if config_int[i] == 0:  # If atom i is Pt
            neighbor_i = neighbor_list[i]
            neighbor_i_num_cu = [config_int[j] for j in neighbor_i].count(2)
            neighbor_i_num_co = [config_int[j] for j in neighbor_i].count(1)
            neighbor_i_num_m = neighbor_i_num_cu + neighbor_i_num_co
            sro = 1 - neighbor_i_num_m / 12 / ratio_m
            SRO_pt_m.append(sro)
    sro_pt_m = np.mean(SRO_pt_m)  # Average SRO for Pt-M

    # Return the calculated SRO values
    sro = [sro_pt_m, sro_co_cu, sro_pt_cu, sro_pt_co]
    return sro

# Function to calculate the potential energy for a given atomic configuration
def get_potential_energy(config_int=[]):
    atoms = read('POSCAR')  # Read the structure from POSCAR file
    symbols = []  # List to store atomic symbols
    for index in config_int:
        if index == 0:
            symbols.append('Pt')
        elif index == 1:
            symbols.append('Co')
        elif index == 2:
            symbols.append('Mn')
    atoms.set_chemical_symbols(symbols)  # Update the atom types based on configuration
    atoms.calc = calc  # Assign the Deep Potential calculator to atoms
    opt = BFGS(atoms)  # Use the BFGS optimizer
    opt.run(fmax=0.03, steps=500)  # Optimize the structure with a force tolerance of 0.03 eV/Å
    return atoms.get_potential_energy()  # Return the potential energy after optimization

# Function to calculate the configurational entropy for a given atomic configuration
def get_configurational_entropy(config_int=[], neighbor_list={}):
    c_pt = config_int.count(0) / len(config_int)  # Fraction of Pt atoms
    c_co = config_int.count(1) / len(config_int)  # Fraction of Co atoms
    c_cu = config_int.count(2) / len(config_int)  # Fraction of Cu atoms

    # Arrays to store the probabilities for different pairwise configurations
    P_pt_pt, P_pt_co, P_pt_cu = [], [], []
    P_co_pt, P_co_co, P_co_cu = [], [], []
    P_cu_pt, P_cu_co, P_cu_cu = [], [], []

    for i in range(len(config_int)):
        if config_int[i] == 0:  # If atom i is Pt
            neighbor_i = neighbor_list[i]
            neighbor_i_num_pt = [config_int[j] for j in neighbor_i].count(0)
            neighbor_i_num_co = [config_int[j] for j in neighbor_i].count(1)
            neighbor_i_num_cu = [config_int[j] for j in neighbor_i].count(2)
            P_pt_pt.append(neighbor_i_num_pt / 12)
            P_pt_co.append(neighbor_i_num_co / 12)
            P_pt_cu.append(neighbor_i_num_cu / 12)
        elif config_int[i] == 1:  # If atom i is Co
            neighbor_i = neighbor_list[i]
            neighbor_i_num_pt = [config_int[j] for j in neighbor_i].count(0)
            neighbor_i_num_co = [config_int[j] for j in neighbor_i].count(1)
            neighbor_i_num_cu = [config_int[j] for j in neighbor_i].count(2)
            P_co_pt.append(neighbor_i_num_pt / 12)
            P_co_co.append(neighbor_i_num_co / 12)
            P_co_cu.append(neighbor_i_num_cu / 12)
        elif config_int[i] == 2:  # If atom i is Cu
            neighbor_i = neighbor_list[i]
            neighbor_i_num_pt = [config_int[j] for j in neighbor_i].count(0)
            neighbor_i_num_co = [config_int[j] for j in neighbor_i].count(1)
            neighbor_i_num_cu = [config_int[j] for j in neighbor_i].count(2)
            P_cu_pt.append(neighbor_i_num_pt / 12)
            P_cu_co.append(neighbor_i_num_co / 12)
            P_cu_cu.append(neighbor_i_num_cu / 12)

    # Calculate the average probabilities for each pair type
    f_pt_pt, f_pt_co, f_pt_cu = np.mean(P_pt_pt), np.mean(P_pt_co), np.mean(P_pt_cu)
    f_co_pt, f_co_co, f_co_cu = np.mean(P_co_pt), np.mean(P_co_co), np.mean(P_co_cu)
    f_cu_pt, f_cu_co, f_cu_cu = np.mean(P_cu_pt), np.mean(P_cu_co), np.mean(P_cu_cu)

    # Boltzmann constant in eV/K
    Kb = 8.6173e-5  # eV/K

    # Calculate the configurational entropy
    Smix = Kb * (
        c_pt * f_pt_pt * math.log((c_pt * f_pt_pt + c_co * f_co_pt + c_cu * f_cu_pt) / (c_pt * f_pt_pt)) +
        c_pt * f_pt_co * math.log((c_pt * f_pt_co + c_co * f_co_co + c_cu * f_cu_co) / (c_pt * f_pt_co)) +
        c_pt * f_pt_cu * math.log((c_pt * f_pt_cu + c_co * f_co_cu + c_cu * f_cu_cu) / (c_pt * f_pt_cu)) +
        c_co * f_co_pt * math.log((c_pt * f_pt_pt + c_co * f_co_pt + c_cu * f_cu_pt) / (c_co * f_co_pt)) +
        c_co * f_co_co * math.log((c_pt * f_pt_co + c_co * f_co_co + c_cu * f_cu_co) / (c_co * f_co_co)) +
        c_co * f_co_cu * math.log((c_pt * f_pt_cu + c_co * f_co_cu + c_cu * f_cu_cu) / (c_co * f_co_cu)) +
        c_cu * f_cu_pt * math.log((c_pt * f_pt_pt + c_co * f_co_pt + c_cu * f_cu_pt) / (c_cu * f_cu_pt)) +
        c_cu * f_cu_co * math.log((c_pt * f_pt_co + c_co * f_co_co + c_cu * f_cu_co) / (c_cu * f_cu_co)) +
        c_cu * f_cu_cu * math.log((c_pt * f_pt_cu + c_co * f_co_cu + c_cu * f_cu_cu) / (c_cu * f_cu_cu))
    ) * len(config_int)
    
    return Smix  # Return the configurational entropy

# Define the MenteCarlo class for performing Monte Carlo simulations
class MenteCarlo:
    def __init__(self, temperature=300, n_step=1000, initial_config=[], out_path=''):
        self.out_path = out_path  # Output path for saving results
        self.temperature = temperature  # Temperature for the simulation (in Kelvin)
        self.n_step = n_step  # Number of MC steps
        self.config = initial_config  # Initial atomic configuration
        print('Initialize...')

    # Function to evaluate short-range order (SRO) of a configuration
    def evaluate_sro(self, config_int, neighbor_list):
        sro = get_sro(config_int=config_int, neighbor_list=neighbor_list)
        return sro

    # Function to evaluate the free energy of a configuration
    def evaluate_free_energy(self, config_int=[], neighbor_list={}):
        h = get_potential_energy(config_int=config_int)  # Potential energy
        s = get_configurational_entropy(config_int=config_int, neighbor_list=neighbor_list)  # Entropy
        f = h - self.temperature * s  # Free energy: F = H - TS
        return f, h, s

    # Function to mutate the atomic configuration
    def get_mutated_config_int(self, config_int=[]):
        mutated_config_int = config_int.copy()
        
        # Randomly choose an atom to swap
        change_index_1 = random.choice([i for i in range(len(config_int))])

        # Find neighbors that have a different type than the chosen atom
        avail_change_indices = []
        for i in neighbor_list[change_index_1]:
            if config_int[change_index_1] != config_int[i]:
                avail_change_indices.append(i)

        # Randomly choose a neighbor to swap with
        if len(avail_change_indices) != 0:
            change_index_2 = random.choice(avail_change_indices)
        else:
            change_index_2 = change_index_1

        # Swap the atomic types
        mutated_config_int[change_index_2] = config_int[change_index_1]
        mutated_config_int[change_index_1] = config_int[change_index_2]
        return mutated_config_int

    # Function to perform Monte Carlo iterations
    def perform_mc_iterations(self):
        print('Start MC iteration:')
        Energy = []  # List to store energies during the simulation
        Energy_min = []  # List to store minimum energy during the simulation
        SRO = []  # List to store SRO values
        SRO_energy_min = []  # List to store SRO of the minimum energy configuration
        Config_int_mc_steps = []  # List to store configurations during the MC steps
        Config_int_energy_min = []  # List to store the configuration with minimum energy
        Enthalpy = []  # List to store enthalpies
        Entropy = []  # List to store entropies

        # Initialize with the given configuration
        config_int = self.config.copy()
        energy_prior, h_prior, s_prior = self.evaluate_free_energy(config_int, neighbor_list)

        energy_mutated = energy_prior
        energy_min = energy_prior
        config_int_min = config_int  # Initialize minimum configuration

        Energy.append(energy_prior)
        Enthalpy.append(h_prior)
        Entropy.append(s_prior)

        # Start MC loop
        for j in range(self.n_step):
            print('MC step:', j)

            config_int_mutated = self.get_mutated_config_int(config_int)  # Generate a mutated configuration
            energy_mutated, h_mutated, s_mutated = self.evaluate_free_energy(config_int_mutated, neighbor_list)  # Evaluate free energy of the mutated configuration
            delta_energy = energy_mutated - energy_prior  # Calculate the energy difference
            theta = np.random.rand()  # Generate a random number
            mi = -delta_energy / (units.kB * self.temperature)  # Boltzmann factor
            p_a = np.exp(mi)  # Probability factor
            prefilter = p_a - theta  # Prefilter for acceptance probability

            # Accept the mutated configuration if the energy is lower or with probability
            if delta_energy < 0 or prefilter > 0:
                energy_prior = energy_mutated
                h_prior = h_mutated
                s_prior = s_mutated
                config_int = config_int_mutated  # Update configuration

                # Update minimum energy and configuration
                if energy_mutated < energy_min:
                    energy_min = energy_mutated
                    config_int_min = config_int_mutated

            # Evaluate SRO for the current and minimum energy configurations
            sro = self.evaluate_sro(config_int=config_int, neighbor_list=neighbor_list)
            sro_energy_min = self.evaluate_sro(config_int=config_int_min, neighbor_list=neighbor_list)

            # Save results
            SRO.append(sro)
            SRO_energy_min.append(sro_energy_min)
            Energy.append(energy_prior)
            Energy_min.append(energy_min)
            Enthalpy.append(h_prior)
            Entropy.append(s_prior)

            if j % 500 == 0:
                Config_int_mc_steps.append(config_int)

        # Save the final configuration with the minimum energy
        Config_int_energy_min.append(config_int_min)

        # Save results to CSV files
        np.savetxt(self.out_path + '/energy.csv', Energy, delimiter=',')
        np.savetxt(self.out_path + '/energy_min.csv', Energy_min, delimiter=',')
        np.savetxt(self.out_path + '/enthalpy.csv', Enthalpy, delimiter=',')
        np.savetxt(self.out_path + '/entropy.csv', Entropy, delimiter=',')
        np.savetxt(self.out_path + '/config.csv', Config_int_mc_steps, delimiter=',')
        np.savetxt(self.out_path + '/config_min.csv', Config_int_energy_min, delimiter=',')
        np.savetxt(self.out_path + '/sro.csv', SRO, delimiter=',')
        np.savetxt(self.out_path + '/sro_energy_min.csv', SRO_energy_min, delimiter=',')
        print('End!')

# Function to run the Monte Carlo simulation
def mc_run(temperature=1, n_step=10000, initial_config='', out_path=''):
    mc = MenteCarlo(temperature=temperature, n_step=n_step, initial_config=initial_config, out_path=out_path)
    mc.perform_mc_iterations()

# Timing the execution of the program
import time
start_time = time.time()  # Record the start time

# Shuffle initial structure and run multiple MC simulations
for mc_num in range(0, 5):
    print('Generation ' + str(mc_num))

    # Initialize configuration from POSCAR
    p = read('POSCAR')
    initial_config = []
    for atom in p:
        if atom.symbol == 'Pt':
            initial_config.append(0)
        elif atom.symbol == 'Co':
            initial_config.append(1)
        elif atom.symbol == 'Mn':
            initial_config.append(2)

    # Create a folder for the simulation
    folder = os.getcwd() + '/' + str(mc_num)
    if not os.path.exists(folder):
        os.makedirs(folder)

    # Run the MC simulation
    mc_run(temperature=500, n_step=5000, initial_config=initial_config, out_path='./' + str
