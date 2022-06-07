# Graphing functions

import matplotlib.pyplot as plt
import numpy as np
from scipy.stats import norm
from scipy.stats import linregress

import tm_stats
import tm_parser


# Helper function to plot a normal distribution with highlighted two-tailed probability
# Returns two-tailed probability
def plot_nd(mu, std, value):
    # Plot the PDF.
    xmin = mu - 3 * std
    xmax = mu + 3 * std
    x = np.arange(xmin, xmax, 0.001)
    low_limit = mu - abs(mu - value)
    high_limit = mu + abs(mu - value)
    x_fill1 = np.arange(xmin, low_limit, 0.001)
    x_fill2 = np.arange(high_limit, xmax, 0.001)

    p = norm.pdf(x, mu, std)
    p_fill1 = norm.pdf(x_fill1, mu, std)
    p_fill2 = norm.pdf(x_fill2, mu, std)

    plt.fill_between(x, p, alpha=0.3, color='b')
    plt.fill_between(x_fill1, p_fill1, alpha=0.6, color='darkorange')
    plt.fill_between(x_fill2, p_fill2, alpha=0.6, color='darkorange')
    plt.plot(x, p)

    return norm(mu, std).cdf(low_limit) + (1 - norm(mu, std).cdf(high_limit))


# Plots the expected normal distributed of averages and the two-tailed probability
# that the contestant's episode average score is as far away from the mean of averages
# as it is
def plot_ep_stats(ep_arr, episode_num, cont_num, brute=False):
    mu, std, real_avg = tm_stats.ep_stats(ep_arr, episode_num=episode_num, cont_num=cont_num, brute=brute)
    ep_prob = plot_nd(mu, std, real_avg)

    title = "Episode %d, Contestant %d\n"\
            "Random Task Average: mean = %.2f,  std dev = %.2f\n" \
            "Episode Average: %.2f, Prob: %.3f" % (episode_num + 1, cont_num + 1, mu, std, real_avg, ep_prob)
    plt.title(title)
    plt.tight_layout()
    plt.show()


# Plots a normal distribution of episodes won and two-tailed probability that number of episodes won as far away from
# mean as it is
def plot_num_eps_won_stats(ep_arr, cont_num):
    mu, std, real_eps_won = tm_stats.num_eps_won_stats(ep_arr, cont_num)
    ep_prob = plot_nd(mu, std, real_eps_won)

    title = "Contestant %d\n"\
            "Episodes Won in Random Draw: mean = %.2f,  std dev = %.2f\n" \
            "Episodes Won on Show: %.2f, Prob: %.3f" % (cont_num + 1, mu, std, real_eps_won, ep_prob)
    plt.title(title)
    plt.tight_layout()
    plt.show()


# Plots a histogram of the expected number of episodes won by a contestant
def plot_num_eps_won_hist(ep_arr, cont_num, num_iter=5000):
    mu, std, real_eps_won = tm_stats.num_eps_won_stats(ep_arr, cont_num)
    eps_won = []
    for i in range(0, num_iter):
        eps_won.append(tm_stats.rand_num_eps_won(ep_arr, cont_num))

    print(real_eps_won)
    possible_eps_won = list(set(eps_won))
    real_eps_index = possible_eps_won.index(real_eps_won)
    n, bins, patches = plt.hist(eps_won, bins=possible_eps_won, density=True)
    patches[real_eps_index].set_fc('orange')

    # x ticks
    xticks = [(bins[idx + 1] + value) / 2 for idx, value in enumerate(bins[:-1])]
    xticks_labels = ["%d" % bins[i] for i in range(len(bins) - 1)]
    plt.xticks(xticks, labels=xticks_labels)

    # Formatting
    title = "Distribution of \"Wins\" for Contestant %d in Random Draw (n=%d)\n"\
            "(Actual Number of \"Wins\" in Orange)" % (cont_num + 1, num_iter)
    plt.title(title)
    plt.xlabel("Number of Episode Wins")
    plt.ylabel("Frequency")
    plt.tight_layout()
    plt.show()


# Helper function to plot points for deviation plot
def plot_lingress(x, y):
    # Fit line
    m, b, r, p, err = linregress(x, y)

    # Plot scatter and linear regression
    plt.plot(x, y, '.')
    plt.plot(x, [b + m * i for i in x], '-')

    return b, m, r

# Plots the mean number of episodes won by a contestant in a random draw against the deviation from this average on the
# show.
def plot_dev_from_eps_won_mean(ep_arr):
    mean_eps_won = tm_stats.mean_eps_won(ep_arr)
    dev_eps_won = []
    for cont_num in range(0, len(mean_eps_won)):
        dev_eps_won.append(tm_stats.num_eps_won(ep_arr, cont_num) - mean_eps_won[cont_num])
    b, m, r = plot_lingress(mean_eps_won,dev_eps_won)

    plt.xlabel("Mean Number of Episodes Won by a Contestant in Random Draw")
    plt.ylabel("Deviation in Real Show from Mean Number of Episodes Won")

    plt.axhline(y=0, color='k', linestyle='-', linewidth=1)
    title = "Mean Episodes Won in Random Draw vs \n"\
        "Deviation from Mean in Show\n"\
        "Slope = %.2f, R^2 = %.3f" % (m,r)
    plt.title(title)
    plt.show()


# Plots mean number of episodes won by a contestant in a random draw against the deviation from this average in
# randomly arranged shows
def plot_dev_rand(ep_arr, num_iter=1000):
    mean_eps_won = tm_stats.mean_eps_won(ep_arr)
    slopes = []
    for i in range(0, num_iter):
        rand_ep_arr = tm_parser.rand_ep_arr(ep_arr)
        dev_eps_won = []
        for cont_num in range(0, len(mean_eps_won)):
            dev_eps_won.append(tm_stats.num_eps_won(rand_ep_arr, cont_num) - mean_eps_won[cont_num])
        b, m, r = plot_lingress(mean_eps_won, dev_eps_won)
        slopes.append(m)

    mean_slope = sum(slopes)/len(slopes)

    plt.xlabel("Mean Number of Episodes Won by a Contestant in Random Draw")
    plt.ylabel("Deviation in Random Show from Mean Number of Episodes Won")

    plt.axhline(y=0, color='k', linestyle='-', linewidth=1)
    title = "Mean Episodes Won in Random Draw vs \n"\
        "Deviation from Mean in Random Show\n"\
        "Mean slope: %.2f" % mean_slope
    plt.title(title)
    plt.show()


# Plots a normal distribution of slopes in the mean-deviation graph, and the two-tailed probability that the actual
# slope is as far away from the mean as it is
def plot_dev_slope_stats(ep_arr, num_iter=1000):
    mu, std, real_slope, slopes = tm_stats.mean_dev_slope_stats(ep_arr, num_iter)

    plt.hist(slopes, density=True, color='grey', bins=30, zorder=0)
    prob = plot_nd(mu, std, real_slope)

    title = "Slope of Mean Wins vs Deviation in Random Shows: mean = %.2f,  std dev = %.2f\n" \
            "Slope of Fit in Actual Show: %.2f, Prob: %.3f" % (mu, std, real_slope, prob)
    plt.title(title)
    plt.tight_layout()
    plt.show()
