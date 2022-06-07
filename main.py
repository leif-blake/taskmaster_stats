# Script to statistically analyze the distribution of scores in the hit British game show taskmaster, where
# comedians are pitted against one another in a variety of pointless exercises.

import tm_parser
import tm_plotter

# Task Types
# P - Prize Task
# E - Empirical Task
# S - Subjective Task
# L - Live Task
# B - Bonus Task

# Team/Individual Designations
# T - Team Task
# I - Individual Task

if __name__ == '__main__':
    raw_data = tm_parser.get_series_data('data/series_2')
    filtered_data = tm_parser.filter_tasks(raw_data, tasks="ES", group="IT")
    ep_array = tm_parser.get_episode_array(filtered_data)
    for row in ep_array:
        print(row)
    print("\n")

    tm_plotter.plot_num_eps_won_hist(ep_array, 2)
    tm_plotter.plot_dev_from_eps_won_mean(ep_array)
    tm_plotter.plot_dev_rand(ep_array, num_iter=1000)
    tm_plotter.plot_dev_slope_stats(ep_array, num_iter=5000)
