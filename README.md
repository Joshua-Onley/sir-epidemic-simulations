# SIR Epidemic Model Simulations

A collection of agent-based simulations exploring disease spread dynamics using the Susceptible-Infected-Recovered (SIR) model. These simulations examine various factors affecting epidemic progression, including network topology, vaccination strategies, and spatial population structure. The simulations in this project were developed as part of university Game Theory coursework.

## Overview

This project implements several variations of the SIR epidemiological model to understand how different parameters and intervention strategies affect disease transmission in populations.

## Files

### 1. `sir_model_simulation.py`
Basic SIR model implementation comparing different transmission (β) and recovery (γ) rates.

**Features:**
- Simple agent-based simulation
- Parameter comparison across multiple β and γ values
- Monte Carlo averaging over multiple runs

**Parameters:**
- Population size: 50 agents
- Transmission rates (β): 0.9, 0.5, 0.2
- Recovery rates (γ): 0.125, 0.1, 0.07

### 2. `sir_network_topology_comparison.py`
Compares epidemic spread across different network structures.

**Network Topologies:**
- **Lattice Network:** 10×10 grid where agents only interact with immediate neighbors (4-connectivity)
- **All-to-All Network:** Complete graph where every agent can interact with every other agent

**Key Insight:** Network structure significantly impacts disease spread speed and final outbreak size.

### 3. `sir_vaccination_model.py`
Explores the impact of vaccination coverage on epidemic dynamics.

**Features:**
- Vaccinated agents have reduced infection probability (β/3)
- Vaccinated agents recover twice as fast (2γ)
- Comparison across vaccination probabilities: 0.0, 0.25, 0.5, 0.75, 1.0

**Key Insight:** Demonstrates threshold effects in vaccination coverage required for epidemic control.

### 4. `sir_multi_village_model.py`
Metapopulation model simulating disease spread across multiple interconnected villages.

**Features:**
- 3 villages with equal population distribution
- 90% intra-village contact, 10% inter-village contact
- Tracks epidemic progression separately for each subpopulation

**Key Insight:** Shows how spatial structure and limited mobility affect disease spread patterns.

### 5. `sir_vaccinated_village_model.py`
Combines metapopulation structure with targeted vaccination intervention.

**Features:**
- 3 villages: one unvaccinated (initial outbreak), one fully vaccinated, one unvaccinated
- Demonstrates protective effect of vaccination on connected populations
- Vaccinated individuals have 50% reduced infection probability

**Key Insight:** Illustrates herd immunity effects and how vaccinating one community can protect neighboring populations.

## Requirements

```bash
pip install numpy matplotlib
```

## Usage

Run any simulation file directly:

```bash
python sir_model_simulation.py
python sir_network_topology_comparison.py
python sir_vaccination_model.py
python sir_multi_village_model.py
python sir_vaccinated_village_model.py
```

Each script will generate matplotlib visualizations showing the disease dynamics over time.

## Model Parameters

Common parameters across simulations:

- **β (beta):** Transmission rate - probability of disease transmission upon contact between susceptible and infected agents
- **γ (gamma):** Recovery rate - probability that an infected agent recovers in a given time step
- **N:** Population size
- **T:** Total simulation time steps
- **v:** Number of villages (metapopulation models)

## Simulation Approach

All models use:
- Agent-based modeling with discrete time steps
- Monte Carlo methods with multiple simulation runs for statistical averaging
- Random sampling for contact and state transitions
- Assertions to verify population conservation

## Key Findings

1. **Transmission dynamics**: Higher β leads to faster, larger outbreaks; higher γ reduces outbreak severity
2. **Network effects**: Lattice networks slow disease spread compared to all-to-all networks
3. **Vaccination thresholds**: Partial vaccination can dramatically reduce outbreak size
4. **Spatial heterogeneity**: Village structure creates temporal delays and spatial patterns in disease spread
5. **Herd immunity**: Vaccinating subpopulations provides indirect protection to connected communities

## Future Extensions

Potential areas for extension:
- Heterogeneous contact rates
- Age-structured populations
- Waning immunity
- Multiple disease strains
- Adaptive behavioral responses
- More complex network topologies (small-world, scale-free)

## Author

Joshua Onley