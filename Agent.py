#This file will be used for the AI which will be trained using reinforcement learning

#this is just planning for main logic
#training mode
#testing mode

#training mode:
    #will automatically put agent v optimal until a stop button is hit
#testing mode:
    # will allow any matchup of player v agent v optimal
#title screen will have ability to go to either
#training mode needs to have a stop button which will stop after current game is finished and return to title screen
#testing mode will play one game and then ask to play again or return to title
#need to make sure progress is saved between closing of program
import torch as T
import torch.nn as nn
import random
import pandas as pd
import numpy as np
import copy


def agent_move(board, piece):
    return 4, 4


EPOCHS = 100
POP_SIZE = 20
MUTATION_RATE = 0.2
ELITISM_RATE = 0.1

env = gym.make("CartPole-v0")
env = env.unwrapped
NUM_ACTIONS = env.action_space.n
NUM_STATES = env.observation_space.shape[0]

if __name__ == '__main__':
    # initialize population
    agents = []
    for _ in range(POP_SIZE):
        agent = Policy(obs_dim=NUM_STATES, act_dim=NUM_ACTIONS)
        agents.append(agent)

    fitness_list = evaluate_agents(env, agents)

    population = pd.DataFrame({'agents': agents,
                               'fitness': fitness_list})

    # Sort population dataframe descending by fitness (highest fitness at row 0)
    population = population.sort_values('fitness', ascending=False, ignore_index=True)

    for epoch in range(EPOCHS):
        evolved_agents = []  # new population of agents to be populated
        # Perform Elitism
        for i in range(int(POP_SIZE * ELITISM_RATE)):
            evolved_agents.append(population.iloc[i]['agents'])

        while len(evolved_agents) < POP_SIZE:
            # Perform Selection
            parent_a, parent_b = selection(population)

            # Perform Crossover
            offspring_a, offspring_b = crossover(parent_a, parent_b)

            # Perform Mutation only on offspring a (arbitrary choice)
            # offspring_a = mutate(offspring_a, MUTATION_RATE)

            # Add to new agents population
            evolved_agents.append(offspring_a)
            evolved_agents.append(offspring_b)

        population['agents'] = evolved_agents
        fitness_list = evaluate_agents(env, evolved_agents)

        population['fitness'] = fitness_list

        population = population.sort_values('fitness', ascending=False, ignore_index=True)
        best_fit = population.iloc[0]['fitness']
        print(f'epoch: {epoch}, current best: {best_fit}')
    best_agent = population.iloc[0]['agents']


# Loop over agents and evaluate each agents performance in the environment
def evaluate_agents(env, agents):
    fitness_list = []
    for agent in agents:
        state = env.reset()
        state = T.from_numpy(state)
        ep_rewards = 0
        while True:
            act_probs = agent(state.float())
            action = T.argmax(act_probs)

            state, reward, done, _ = env.step(action.item())
            state = T.from_numpy(state)
            ep_rewards += reward

            if done or ep_rewards == 19500:
                break

        fitness_list.append(ep_rewards)

    return fitness_list


# Helper function to apply crossover between two matrices
def single_mat_crossover(mat_a, mat_b):
    # Save shape to reshape after flattening
    mat_shape = mat_a.shape

    mat_a_flat = mat_a.flatten()
    mat_b_flat = mat_b.flatten()

    # random crossover point for flattened matrices
    crossover_point = random.randint(1, len(mat_a_flat))

    offspring1 = T.cat((mat_a_flat[:crossover_point], mat_b_flat[crossover_point:]))
    offspring2 = T.cat((mat_a_flat[crossover_point:], mat_b_flat[:crossover_point]))

    # Reshape to original matrix shape
    offspring1 = offspring1.reshape(mat_shape)
    offspring2 = offspring2.reshape(mat_shape)

    return offspring1, offspring2


# Apply crossover between two parent agents
def crossover(parent_a, parent_b):
    # Copy parent agents to new variables
    offspring_a = copy.deepcopy(parent_a)
    offspring_b = copy.deepcopy(parent_b)

    # Loop over each matrix in our two policy networks and apply crossover
    for param_a, param_b in zip(offspring_a.parameters(), offspring_a.parameters()):
        mat_a, mat_b = single_mat_crossover(param_a.data, param_b.data)
        param_a.data = nn.parameter.Parameter(T.zeros_like(param_a))
        param_b.data = nn.parameter.Parameter(mat_b)

    return offspring_a, offspring_b


def single_mat_mutation(mat, mutation_rate):
    mat_shape = mat.shape
    flattened_mat = mat.flatten()
    indices = random.sample(range(1, len(flattened_mat)), int(len(flattened_mat) * mutation_rate))

    sigma = (max(flattened_mat) - min(flattened_mat)) / max(flattened_mat)
    for idx in indices:
        flattened_mat[idx] = random.gauss(flattened_mat[idx], sigma)

    # Reshape to original matrix shape
    mat = flattened_mat.reshape(mat_shape)
    # print(mat.shape)
    return mat


# Mutate each
def mutate(agent, mutation_rate):
    mutated_agent = copy.deepcopy(agent)
    for param in mutated_agent.parameters():
        mat = single_mat_mutation(param.data, mutation_rate)
        param.data = nn.parameter.Parameter(mat)

    return mutated_agent


# Select two parents from population based on fitness
def selection(population):
    # Define a probability distribution proportional to each agent's fitness/reward score
    fit_sum = sum(population['fitness'])
    prob_dist = population['fitness'] / fit_sum

    # Choose random indices from distribution making sure they're not equal
    par_a_idx = 0
    par_b_idx = 0
    while par_a_idx == par_b_idx:
        par_a_idx = np.random.choice(np.arange(0, len(prob_dist)), p=prob_dist)
        par_b_idx = np.random.choice(np.arange(0, len(prob_dist)), p=prob_dist)

    parent_a = population.iloc[par_a_idx]['agents']
    parent_b = population.iloc[par_b_idx]['agents']

    # Return two picked parents
    return parent_a, parent_b


class Policy(nn.Module):
    def __init__(self, obs_dim, act_dim):
        super(Policy, self).__init__()

        # Layers
        self.linear1 = nn.Linear(obs_dim, 50)
        self.linear2 = nn.Linear(50, 30)
        self.linear3 = nn.Linear(30, act_dim)

    def forward(self, x):
        x = self.linear1(x)
        x = self.linear2(x)
        x = self.linear3(x)

        return x