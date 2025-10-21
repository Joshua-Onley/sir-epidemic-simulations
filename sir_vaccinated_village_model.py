import random
import numpy as np
import matplotlib.pyplot as plt
import copy


def runVillageSimulation(β: float, γ: float, N: int, T: int, t: int = 0, v: int = 3) -> tuple[list[list[int]], list[list[int]], list[list[int]]]:
    """
    Simulates the spread of an infectious disease in multiple villages, with the second village fully vaccinated.
    Vaccinated individuals are counted as susceptible but have half the chance of getting infected.

    Parameters:
    β : Transmission rate
    γ : Recovery rate
    N : Total population size
    T : End time-step
    t : Initial time-step
    v : Number of villages

    Returns:
        - sv: Time series of susceptible counts (including vaccinated individuals) per village
        - iv: Time series of infected counts per village
        - rv: Time series of recovered counts per village
    """
    # Creating v villages with (N//v) agents each (all susceptible initially)
    agents = [['S']*(N//v) for _ in range(v)]
    
    # fully vaccinate the second village 
    agents[1] = ['V']*(N//v)
    
    # randomly infect one agent in village 0
    randomVillage = 0  
    randomAgent = random.randint(0, (N//v) - 1)
    agents[randomVillage][randomAgent] = 'I'
    
    # track population counts per village over time
    # vaccinated individuals ("V") are counted as susceptible
    sv = [[row.count('S')+row.count('V') for row in agents]]
    iv = [[row.count('I') for row in agents]]
    rv = [[row.count('R') for row in agents]]
    
    while t < T:
        newAgents = copy.deepcopy(agents)
        
        # Select first agent
        randomAgent1VillageIdx = random.randint(0, v-1)
        randomAgent1Idx = random.randint(0, (N//v)-1)
        
        # Select a second agent with 10% probability from a different village; otherwise, same village.
        if random.random() < 0.1:
            randomAgent2VillageIdx = random.randint(0, v-1)
            randomAgent2Idx = random.randint(0, (N//v)-1)
        else:
            randomAgent2VillageIdx = randomAgent1VillageIdx
            possibleIndices = list(range(N//v))
            if (N//v) > 1:
                possibleIndices.remove(randomAgent1Idx)
            randomAgent2Idx = random.choice(possibleIndices)
        
        randomAgent1 = agents[randomAgent1VillageIdx][randomAgent1Idx]
        randomAgent2 = agents[randomAgent2VillageIdx][randomAgent2Idx]
        
        # Infection process:
        # If one agent is infected and the other is either susceptible or vaccinated,
        # apply infection probability accordingly.
        if randomAgent1 =='I' and randomAgent2 in ['S', 'V']:
            # full probability if target is "S"; half if "V".
            prob = β if randomAgent2 == 'S' else β/2
            if random.random() < prob:
                newAgents[randomAgent2VillageIdx][randomAgent2Idx] = 'I'
        elif randomAgent2 == 'I' and randomAgent1 in ['S', 'V']:
            prob = β if randomAgent1 == 'S' else β/2
            if random.random() < prob:
                newAgents[randomAgent1VillageIdx][randomAgent1Idx] = 'I'
        
        # Recovery process: randomly select an agent for potential recovery.
        randomRecoveryVillage = random.randint(0, v-1)
        randomRecoveryAgent = random.randint(0, (N // v)-1)
        if agents[randomRecoveryVillage][randomRecoveryAgent] == 'I' and random.random() < γ:
            newAgents[randomRecoveryVillage][randomRecoveryAgent] = 'R'
        
        agents = newAgents
        t+=1
        
        # Update population counts per village (treat vaccinated as susceptible)
        sv.append([row.count('S') + row.count('V') for row in agents])
        iv.append([row.count('I') for row in agents])
        rv.append([row.count('R') for row in agents])
        
        # total population should stay constant otherwise there is a logical error somewhere.
        totalPopulation = sum(row.count('S') + row.count('I') + row.count('R') + row.count('V') for row in agents)
        assert totalPopulation == N
    
    return sv, iv, rv


β = 0.6 # transmission rate.
γ = 0.1 # recovery rate.
N = 150 # total population.
T = 2500 # number of time steps.
v = 3 # number of villages.
numSimulations = 50  # number of simulation runs.

# averaging over simulations
sTotal = np.zeros((T+1, v))
iTotal = np.zeros((T+1, v))
rTotal = np.zeros((T+1, v))

for sim in range(numSimulations):
    sv, iv, rv = runVillageSimulation(β, γ, N, T, t=0, v=v)
    sTotal += np.array(sv)
    iTotal += np.array(iv)
    rTotal += np.array(rv)

sAvg = sTotal/numSimulations
iAvg = iTotal/numSimulations
rAvg = rTotal/numSimulations

timeSteps = np.arange(T+1)

# Plot the results
fig, axes = plt.subplots(3, 1, figsize=(10, 12), sharex=True)

for village in range(v):
    axes[0].plot(timeSteps, sAvg[:, village], label=f'Village {village + 1}')
    axes[0].set_title("Susceptible (Including Vaccinated) Over Time (Average)")
    axes[0].set_ylabel("Susceptible Count")
    axes[0].legend()
for village in range(v):
    axes[1].plot(timeSteps, iAvg[:, village], label=f'Village {village + 1}')
    axes[1].set_title("Infected Over Time (Average)")
    axes[1].set_ylabel("Infected Count")
    axes[1].legend()
for village in range(v):
    axes[2].plot(timeSteps, rAvg[:, village], label=f'Village {village + 1}')
    axes[2].set_title("Recovered Over Time (Average)")
    axes[2].set_xlabel("Time Steps")
    axes[2].set_ylabel("Recovered Count")
    axes[2].legend()

plt.tight_layout()
plt.subplots_adjust(bottom=0.15)
plt.show()
