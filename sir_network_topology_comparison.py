import random
import numpy as np
import matplotlib.pyplot as plt
import copy

def latticeSimulation(β: float, γ: float, N: int, T: int) -> tuple[list[int], list[int], list[int]]:
    """
    simulates the spread of an infectious disease in a lattice network topology

    Parameters:

    β : Transmission rate
    γ : Recovery rate
    N : Total population size
    T : End time-step

    Returns:
        s : list containing the count of susceptible agents at each time step
        i : list containing the count of infected agents at each time step
        r : list containing the count of recovered agents at each time step 

    """

    t = 0 # initial time step

    # initialisation - everyone is susceptible except one infected agent
    agents = [['S' for _ in range(N)] for _ in range(N)]
    randomRow = random.randint(0, N - 1)
    randomCol = random.randint(0, N - 1)
    agents[randomRow][randomCol] = 'I'

    # trackers for each timestep
    s = [N * N - 1]
    i = [1]
    r = [0]

    # Run simulation for T timesteps
    while t < T:
        
        newAgents = copy.deepcopy(agents)
        neighbours = [(1, 0), (0, 1), (-1, 0), (0, -1)]
        
        # iterate through each agent in the grid
        for rowIdx in range(N):
            for colIdx in range(N):
                if agents[rowIdx][colIdx] == 'I':
                    # infecting susceptible neighbours
                    for dr, dc in neighbours:
                        ni, nj = rowIdx + dr, colIdx + dc
                        if 0 <= ni < N and 0 <= nj < N and agents[ni][nj] == 'S':
                            if random.random() < β:
                                newAgents[ni][nj] = 'I'
                    # Check for recovery
                    if random.random() < γ:
                        newAgents[rowIdx][colIdx] = 'R'
        
        agents = newAgents
    
        # record the counts after this timestep
        s.append(sum(row.count('S') for row in agents))
        i.append(sum(row.count('I') for row in agents))
        r.append(sum(row.count('R') for row in agents))


        assert sum(row.count('S') + row.count('I') + row.count('R') for row in agents)  == N*N

        t += 1
    
    return s, i, r


def all_to_all_simulation(β: float, γ: float, N: int, T: int) -> tuple[list[int], list[int], list[int]]:

    """
    simulates the spread of an infectious disease in an all-to-all network topology
    Parameters:
    β : Transmission rate
    γ : Recovery rate
    N : Total population size
    T : End time-step
    Returns:
        s : list containing the count of susceptible agents at each time step
        i : list containing the count of infected agents at each time step
        r : list containing the count of recovered agents at each time step 

    """

    t = 0
    # initialising the population with one infected individual and N-1 susceptible individuals
    agents = (N-1) * ['S']
    agents.append('I')

    s = [N - 1]
    i = [1]
    r = [0]

    while t < T:

        newAgents = copy.deepcopy(agents)

        # loop through all agents
        for i_ in range(N):
            if agents[i_] == 'I':
                # if the agent is infected, they come into contact with all other agents in the network and infect them with Probability β
                for j in range(N):
                    if j != i_ and agents[j] == 'S' and random.random() < β:
                        newAgents[j] = 'I'
                if random.random() < γ:
                    newAgents[i_] = 'R'
        
        agents = newAgents

        s.append(agents.count('S'))
        i.append(agents.count('I'))
        r.append(agents.count('R'))

        assert agents.count('S') + agents.count('I') + agents.count('R') == N
                
        t += 1

    return s, i, r


runs = 50           
grid_N = 10 # grid size for lattice (10x10 = 100 agents)
population_N = 100 # population size for all-to-all
T = 50 # end time step
β = 0.3 # transmission probability
γ = 0.1 # recovery probability

# plotting results
def plot_comparison(latticeData, allToAllData, title):
    plt.figure(figsize=(12, 6))
    
    # Plot lattice results
    plt.subplot(1, 2, 1)
    plt.plot(latticeData['susceptible'], label='Susceptible', color='blue')
    plt.plot(latticeData['infected'], label='Infected', color='red')
    plt.plot(latticeData['recovered'], label='Recovered', color='green')
    plt.title(f'Lattice Model (N={grid_N}x{grid_N})')
    plt.xlabel('Time Step')
    plt.ylabel('Population')
    plt.legend()
    plt.grid(True)
    
    # Plot all-to-all results
    plt.subplot(1, 2, 2)
    plt.plot(allToAllData['susceptible'], label='Susceptible', color='blue')
    plt.plot(allToAllData['infected'], label='Infected', color='red')
    plt.plot(allToAllData['recovered'], label='Recovered', color='green')
    plt.title(f'All-to-All Model (N={population_N})')
    plt.xlabel('Time Step')
    plt.ylabel('Population')
    plt.legend()
    plt.grid(True)
    
    plt.suptitle(title)
    plt.tight_layout()
    plt.show()

def run_comparison():
    latticeSusceptible, latticeInfected, latticeRecovered = [], [], []
    for _ in range(runs):
        s, i, r = latticeSimulation(β, γ, grid_N, T)
        latticeSusceptible.append(s)
        latticeInfected.append(i)
        latticeRecovered.append(r)
    
    allToAllSusceptible, allToAllInfected, allToAllRecovered = [], [], []
    for _ in range(runs):
        s, i, r = all_to_all_simulation(β, γ, population_N, T)
        allToAllSusceptible.append(s)
        allToAllInfected.append(i)
        allToAllRecovered.append(r)
    
    latticeData = {
        'susceptible': np.mean(latticeSusceptible, axis=0),
        'infected': np.mean(latticeInfected, axis=0),
        'recovered': np.mean(latticeRecovered, axis=0)
    }
    
    allToAllData = {
        'susceptible': np.mean(allToAllSusceptible, axis=0),
        'infected': np.mean(allToAllInfected, axis=0),
        'recovered': np.mean(allToAllRecovered, axis=0)
    }
    
    plot_comparison(latticeData, allToAllData, 
                   f"Epidemic Spread Comparison (β={β}, γ={γ})")

run_comparison()



