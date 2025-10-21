import random
import numpy as np
import matplotlib.pyplot as plt
import copy

def runVillageSimulation(β: float, γ: float, N: int, T: int, v: int) -> tuple[list[list[int]], list[list[int]], list[list[int]]]:
    """
    Simulates the spread of an infectius disease in multiple villages

    Parameters:
    β: transmission rate
    γ: recovery rate
    N: total population size
    T: end time-step
    v: number of supopulations (i.e., number of different villages)

    Returns:
    Tuple[List[int], List[int], List[int]]: 
        - s: time series of the total susceptible population.
        - i: time series of the total infected population.
        - r: time series of the total recovered population.
    """

    t = 0
    
    # Creating v villages with (N//v) agents each (all susceptible initially)
    agents = [['S'] * (N // v) for _ in range(v)]
    
    # Randomly infect one agent in one village
    randomVillage = 0
    randomAgent = random.randint(0, (N // v) - 1)
    agents[randomVillage][randomAgent] = 'I'
    
    # track population counts per village over time.
    # each element is a list of counts for the v villages at that time step.
    sv = [ [row.count('S') for row in agents] ]
    iv = [ [row.count('I') for row in agents] ]
    rv = [ [row.count('R') for row in agents] ]
    
    while t < T:
        newAgents = copy.deepcopy(agents)
        
        # pick a random agent
        randomAgent1VillageIdx = random.randint(0, v - 1)
        randomAgent1Idx = random.randint(0, (N // v) - 1)
        
        # Select a second agent with 10% probability from a different village, otherwise same village
        if random.random() < 0.1:
            randomAgent2VillageIdx = random.randint(0, v - 1)
            randomAgent2Idx = random.randint(0, (N // v) - 1)
        else:
            randomAgent2VillageIdx = randomAgent1VillageIdx
            possibleIndices = list(range(N // v))
            if (N // v) > 1:
                possibleIndices.remove(randomAgent1Idx)
            randomAgent2Idx = random.choice(possibleIndices)
        
        randomAgent1 = agents[randomAgent1VillageIdx][randomAgent1Idx]
        randomAgent2 = agents[randomAgent2VillageIdx][randomAgent2Idx]
        
        # if one is infected and the other is susceptible
        if randomAgent1 == 'I' and randomAgent2 == 'S' and random.random() < β:
            newAgents[randomAgent2VillageIdx][randomAgent2Idx] = 'I'
        elif randomAgent1 == 'S' and randomAgent2 == 'I' and random.random() < β:
            newAgents[randomAgent1VillageIdx][randomAgent1Idx] = 'I'
        
        # randomly selecting an agent for potential recovery
        randomRecoveryVillage = random.randint(0, v - 1)
        randomRecoveryAgent = random.randint(0, (N // v) - 1)
        if agents[randomRecoveryVillage][randomRecoveryAgent] == 'I' and random.random() < γ:
            newAgents[randomRecoveryVillage][randomRecoveryAgent] = 'R'
        
        agents = newAgents
        t += 1
        
        sv.append([row.count('S') for row in agents])
        iv.append([row.count('I') for row in agents])
        rv.append([row.count('R') for row in agents])
        
        assert sum(sv[-1]) + sum(iv[-1]) + sum(rv[-1]) == N
    
    return sv, iv, rv

β = 0.6 # transmission rate 
γ = 0.1 # recovery rate
N = 150 # total population
T = 2500 # number of time steps
v = 3 # number of villages
numSimulations = 50 # number of simulation runs

sTotal = np.zeros((T+1, v))
iTotal = np.zeros((T+1, v))
rTotal = np.zeros((T+1, v))

for sim in range(numSimulations):
    sv, iv, rv = runVillageSimulation(β, γ, N, T, v=v)
    sTotal += np.array(sv)
    iTotal += np.array(iv)
    rTotal += np.array(rv)

# compute averages
sAvg = sTotal / numSimulations
iAvg = iTotal / numSimulations
rAvg = rTotal / numSimulations

timeSteps = np.arange(T + 1)

# Plot the results
fig, axes = plt.subplots(3, 1, figsize=(10, 12), sharex=True)

for village in range(v):
    axes[0].plot(timeSteps, sAvg[:, village], label=f'Village {village + 1}')
axes[0].set_title("Susceptible Over Time")
axes[0].set_ylabel("Susceptible Count")
axes[0].legend()
for village in range(v):
    axes[1].plot(timeSteps, iAvg[:, village], label=f'Village {village + 1}')
axes[1].set_title("Infected Over Time")
axes[1].set_ylabel("Infected Count")
axes[1].legend()
for village in range(v):
    axes[2].plot(timeSteps, rAvg[:, village], label=f'Village {village + 1}')
axes[2].set_title("Recovered Over Time")
axes[2].set_xlabel("Time Steps")
axes[2].set_ylabel("Recovered Count")
axes[2].legend()

plt.tight_layout()
plt.subplots_adjust(bottom=0.15)
plt.show()
