import random
import numpy as np
import matplotlib.pyplot as plt
import copy

def runSimulation(β: float, γ: float, N: int, T: int , v: int) ->  tuple[list[int], list[int], list[int]]:

    """
    simulates the spread of an infectious disease in an SIR model with vaccination

    Parameters:

    β : Transmission rate
    γ : Recovery rate
    N : Total population size
    T : End time-step
    v : Probability of an agent receiving the vaccination

    Returns:
        s : list containing the count of susceptible agents at each time step
        i : list containing the count of infected agents at each time step
        r : list containing the count of recovered agents at each time step 

    """

    t = 0

    agents = [['S', 'L'] for _ in range(N-1)] + [['I', 'L']]
    
    # Vaccinate agents with probability v
    for agent in agents:
        if agent[0] == 'S' and agent[1] == 'L' and random.random() < v:
            agent[1] = 'V'

    s = [N-1]
    i = [1]
    r = [0]

    while t < T:
        new_agents = copy.deepcopy(agents)
        randomAgent1, randomAgent2 = random.sample(range(N), 2)

        # infection from an infected to a susceptible (not vaccinated)
        if (agents[randomAgent1][0] == 'I' and agents[randomAgent2][0] == 'S') and (agents[randomAgent2][1] == 'L'):
            if random.random() < β:
                new_agents[randomAgent2][0] = 'I'
        # infection when the susceptible is vaccinated (half probability)
        elif (agents[randomAgent1][0] == 'I' and agents[randomAgent2][0] == 'S') and (agents[randomAgent2][1] == 'V'):
            if random.random() < (β / 3):
                new_agents[randomAgent2][0] = 'I'
        # Reverse roles: susceptible agent is randomAgent1
        elif (agents[randomAgent1][0] == 'S' and agents[randomAgent2][0] == 'I') and (agents[randomAgent1][1] == 'L'):
            if random.random() < β:
                new_agents[randomAgent1][0] = 'I'
        elif (agents[randomAgent1][0] == 'S' and agents[randomAgent2][0] == 'I') and (agents[randomAgent1][1] == 'V'):
            if random.random() < (β / 3):
                new_agents[randomAgent1][0] = 'I'

        # Recovery step
        recoveryAgent = random.randint(0, N-1)
        if agents[recoveryAgent][0] == 'I' and agents[recoveryAgent][1] == 'L' and random.random() < γ:
            new_agents[recoveryAgent][0] = 'R'
        elif agents[recoveryAgent][0] == 'I' and agents[recoveryAgent][1] == 'V' and random.random() < γ*2:
            new_agents[recoveryAgent][0] = 'R'
        
        agents = new_agents
        s.append(sum(1 for a in agents if a[0] == 'S'))
        i.append(sum(1 for a in agents if a[0] == 'I'))
        r.append(sum(1 for a in agents if a[0] == 'R'))
        t += 1

    return s, i, r


β = 0.6 # Transmission rate
γ = 0.1 # Recovery rate
N = 50 # Population size
T = 2000 # Number of time steps
numSimulations = 10 # Number of simulations per vaccination probability

# vaccination probabilities for subplots
vaccinationRates = [0.0, 0.25, 0.5, 0.75, 1.0]

# subplots
fig, axes = plt.subplots(1, len(vaccinationRates), figsize=(20, 4), sharey=True)

for idx, v in enumerate(vaccinationRates):
    sTotal = np.zeros(T+1)
    iTotal = np.zeros(T+1)
    rTotal = np.zeros(T+1)
    
    for _ in range(numSimulations):
        s, i, r = runSimulation(β, γ, N, T, v=v)
        sTotal += np.array(s)
        iTotal += np.array(i)
        rTotal += np.array(r)
    
    sAvg = sTotal / numSimulations
    iAvg = iTotal / numSimulations
    rAvg = rTotal / numSimulations
    
    ax = axes[idx]
    ax.plot(sAvg, label='Susceptible', color='blue')
    ax.plot(iAvg, label='Infected', color='red')
    ax.plot(rAvg, label='Recovered', color='green')
    ax.set_title(f"Vaccination Probability = {v}")
    ax.set_xlabel("Time Steps")
    if idx == 0:
        ax.set_ylabel("Average Population")
    ax.legend(fontsize=8)

plt.tight_layout()
plt.subplots_adjust(bottom=0.15)
plt.show()
