import random
import numpy as np
import matplotlib.pyplot as plt

β_values = [0.9, 0.5, 0.2] # transmission rates to simulate
γ_values = [0.125, 0.1, 0.07] # recovery rates to simulate
N = 50 # population size
T = 2000 # number of time steps
numSimulations = 50 # number of simulation runs per parameter set (for the graphs in the report i used numSimulations = 1000)

def runSimulation(β: float, γ: float, N: int, T: int) -> tuple[list[int], list[int], list[int]]:
    """
    simulates the spread of an infectious disease in a simple SIR model

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

    t = 0 # starting time step

    # initialise population with N-1 susceptibles and 1 infected
    agents = ['S'] * (N-1) + ['I']

    # track the population counts for s, i, and r over each time step
    s = [N-1]
    i = [1]
    r = [0]
    
    while t < T:

        newAgents = agents.copy()

        # infection
        randomAgent1, randomAgent2 = random.sample(range(N), 2) # two random indexes (agents)
        if (agents[randomAgent1], agents[randomAgent2]) in [('S', 'I'), ('I', 'S')]: # if one agent is susceptible and the other agent is infected
            susceptible = randomAgent1 if agents[randomAgent1] == 'S' else randomAgent2 
            if random.random() < β: 
                newAgents[susceptible] = 'I' # infect the susceptible agent with probability β
        
        # recovery
        recoveryAgentIndex = random.randint(0, N-1)
        if agents[recoveryAgentIndex] == 'I' and random.random() < γ: # if the agent randomly chosen is infected, recover them with probability γ
            newAgents[recoveryAgentIndex] = 'R'
        
        # update counts
        agents = newAgents
        s.append(agents.count('S'))
        i.append(agents.count('I'))
        r.append(agents.count('R'))

        # population change indicates logical error
        assert agents.count('S') + agents.count('I') + agents.count('R') == N

        # increment time step
        t += 1
    
    return s, i, r

# results for each parameter combination
results = []

# run simulations for each parameter set
for β, γ in zip(β_values, γ_values):
    sRuns = []
    iRuns = []
    rRuns = []
    
    for _ in range(numSimulations):
        s, i, r = runSimulation(β, γ, N, T)
        sRuns.append(s)
        iRuns.append(i)
        rRuns.append(r)
    

    results.append((
        np.mean(sRuns, axis=0),
        np.mean(iRuns, axis=0),
        np.mean(rRuns, axis=0)
    ))


# plot results
plt.figure(figsize=(12, 8))
for index, (β, γ) in enumerate(zip(β_values, γ_values)):
    averageS, averageI, averageR = results[index]
    plt.subplot(3, 1, index+1)
    plt.plot(averageS, label='Susceptible', color='blue')
    plt.plot(averageI, label='Infected', color='red')
    plt.title(f'β = {β}, γ = {γ}')
    plt.xlabel('Time Steps')
    plt.ylabel('Population')
    plt.legend()
    plt.grid(True)
plt.tight_layout()
plt.show()