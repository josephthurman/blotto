import numpy as np
import numpy.random as random
import pandas as pd

# Return a tuple with the score for each strategy in a single match
def score_game(strategy1, strategy2):
    strategy1_score = 0
    strategy2_score = 0
    for points, (a,b) in enumerate(zip(strategy1, strategy2)):
        if a > b:
            strategy1_score += points + 1
        elif a < b:
            strategy2_score += points + 1
    return (strategy1_score, strategy2_score)

# Return list of M strategies, each one generated by the function strategy_generator
def generate_strategy_list(M, strategy_generator):
    k = len(strategy_generator())
    strategies = np.zeros((M,k), dtype = int)
    for i in range(M):
        strategies[i] = strategy_generator()
    return strategies

# Return the average score of strategy played against every opponent in opponents list
def score_vs_opponents(strategy, opponents):
    total_score = 0
    for opponent in opponents:
        a, _ = score_game(strategy, opponent)
        total_score += a
    return total_score / len(opponents)

def estimate_score_of(strategy, opponent_generator, N, M ):
    """
    strategy - strategy to score
    opponent_generator - function that generates M opponent strategies
    N - number of games to simulate
    M - size of game to simulate
    """
    scores = np.zeros(N, dtype = float)
    for i in range(N):
        opponents = opponent_generator(M)
        scores[i] = score_vs_opponents(strategy, opponents)
    return np.mean(scores)

# Sample M elements from empirical_sample, with replacement
def bootstrap_sample(M):
    strategies = np.zeros((M,10), dtype = int)
    for i in range(M):
        strategies[i] = empirical_sample[random.choice(len(empirical_sample))]
    return strategies

def random_candidate(total):
    strategy = np.zeros(10, dtype = int)
    unallocated = total
    choice8 = random.choice(range(max(0,total//5 -4), total//3 + 4))
    unallocated -= choice8
    choice7 = random.choice(range(max(0,total//8 -4), min(unallocated,total//3 + 4)))
    unallocated -= choice7
    choice9 = random.choice(range(min(unallocated, total // 10)))
    unallocated -= choice9
    choice10 = random.choice(range(min(unallocated, total // 10)))
    unallocated -= choice10
    strategy[6:10] = [choice7, choice8, choice9, choice10]
    for i in reversed(range(5)):
        allocation = random.choice(range(min(unallocated+1, total//3 + 4)))
        strategy[i] = allocation
        unallocated -= allocation
    strategy[5] = unallocated
    return strategy


def strategy_90_generator():
    return random_candidate(total = 90)

def strategy_100_generator():
    return random_candidate(total = 100)

def strategy_110_generator():
    return random_candidate(total = 110)

def find_best_strategy(candidates, opponent_generator, N, M):
    scores = np.zeros(len(candidates), dtype = float)
    for (i, candidate) in enumerate(candidates):
        scores[i] = estimate_score_of(candidate, opponent_generator,  N, M)
    best = np.argmax(scores)
    return (candidates[best], scores[best])

if __name__ == "__main__":
    data = pd.read_csv("castle-solutions.csv")
    data['sum'] = data.sum(axis = 1)
    valid = data[data['sum'] == 100]
    cleaned = valid.drop(['Why did you choose your troop deployment?','sum'], axis = 1)
    empirical_sample = cleaned.as_matrix()

    random.seed(123)
    candidates_90 = generate_strategy_list(1500, strategy_90_generator)
    candidates_100 = generate_strategy_list(1500, strategy_100_generator)
    candidates_110 = generate_strategy_list(1500, strategy_110_generator)

    (best_90, best_90_score) = find_best_strategy(candidates_90, bootstrap_sample, 10, 500)
    (best_100, best_100_score) = find_best_strategy(candidates_100, bootstrap_sample, 10, 500)
    (best_110, best_110_score) = find_best_strategy(candidates_110, bootstrap_sample, 10, 500)

    print("Stategy for 90 Soldiers: " + str(list(best_90)))
    print("Stategy for 100 Soldiers: " + str(list(best_100)))
    print("Stategy for 110 Soldiers: " + str(list(best_110)))
    print("with expected scores:")
    print((best_90_score, best_100_score, best_110_score))
