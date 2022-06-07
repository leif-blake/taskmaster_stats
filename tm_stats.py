# Functions for getting statistical values

from itertools import combinations
from scipy.stats import norm
from scipy.stats import linregress
import tm_parser


# Get the mean and std dev of average scores for a specific contestant
# in a given episode, assuming a random selection of remaining (ie, not used
# in previous episodes) tasks
def ep_stats(ep_arr, episode_num, cont_num, brute=False):
    scores = []
    for ep_index in range((0 if brute else episode_num), len(ep_arr)): # brute condition means used scores are still counted
        for task in ep_arr[ep_index]:
            scores.append(task[cont_num])
    combs = list(combinations(scores, len(ep_arr[episode_num])))  # 2d list of all possible combinations of scores
    avgs = [sum(comb)/len(comb) for comb in combs]  # averages of each combination of scores
    mu, std = norm.fit(avgs)  # mean and std deviation for the expected average score in the episode

    real_ep_scores = [task[cont_num] for task in ep_arr[episode_num]]
    real_avg = sum(real_ep_scores) / len(real_ep_scores)  # actual average score the contestant, ep

    return mu, std, real_avg


# Returns the number of episodes that a contestant wins based on a given arrangement of tasks into episodes
def num_eps_won(ep_arr, cont_num):
    num_eps_won = 0
    for ep in ep_arr:
        ep_pts_arr = [0, 0, 0, 0, 0]
        for task in ep:
            ep_pts_arr = [x + y for x, y in zip(ep_pts_arr, task)]  # Add task points to episode total
        # Check if contestant won the episode. If tied, counts as win
        max_pts = max(ep_pts_arr)
        if ep_pts_arr[cont_num] == max_pts:
            num_eps_won += 1
    return num_eps_won


# Returns the number of episodes that a contestant wins based on a random arrangement of tasks into episodes
def rand_num_eps_won(ep_arr, cont_num):
    ep_arr = tm_parser.rand_ep_arr(ep_arr)
    return num_eps_won(ep_arr, cont_num)


# Returns the distribution of episodes won by a contestant given randomly distributed tasks
def num_eps_won_stats(ep_arr, cont_num, num_iter=1000):
    eps_won = []
    for i in range(0, num_iter):
        eps_won.append(rand_num_eps_won(ep_arr, cont_num))

    mu, std = norm.fit(eps_won)  # mean and std deviation for the expected number of episodes won
    real_eps_won = num_eps_won(ep_arr, cont_num)

    return mu, std, real_eps_won


# Returns a list of mean episode wins for each contestant
def mean_eps_won(ep_arr):
    mean_eps_won = []
    for cont_num in range(0, 5):
        mu, std, real_eps_won = num_eps_won_stats(ep_arr, cont_num)
        mean_eps_won.append(mu)

    return mean_eps_won


# Returns the distribution of slopes in a mean wins-deviation plot
def mean_dev_slope_stats(ep_arr, num_iter):
    mean_eps_won_arr = mean_eps_won(ep_arr)

    # Actual slope
    dev_eps_won = []
    for cont_num in range(0, len(mean_eps_won_arr)):
        dev_eps_won.append(num_eps_won(ep_arr, cont_num) - mean_eps_won_arr[cont_num])
    m_real, b, r, p, err = linregress(mean_eps_won_arr, dev_eps_won)

    # Randomized slopes
    slopes = []
    for i in range(0, num_iter):
        rand_ep_arr = tm_parser.rand_ep_arr(ep_arr)
        dev_eps_won = []
        for cont_num in range(0, len(mean_eps_won_arr)):
            dev_eps_won.append(num_eps_won(rand_ep_arr, cont_num) - mean_eps_won_arr[cont_num])
        m, b, r, p, err = linregress(mean_eps_won_arr, dev_eps_won)
        slopes.append(m)

    mu, std = norm.fit(slopes)

    return mu, std, m_real, slopes
