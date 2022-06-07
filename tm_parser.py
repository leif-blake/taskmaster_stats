# Helper functions to load taskmaster series data from file and store in lists

import csv
import random


# Loads series data from csv into a 2d array
def get_series_data(series_name):
    data_array = []
    # Import series data into array
    with open(series_name + '.csv') as series_file:
        data_reader = csv.reader(series_file, delimiter=',')
        for row in data_reader:
            data_array.append(row)
    data_array[0][0] = 1  # first element is corrupted, but we always start on ep1

    return data_array


# Defaults to include Empirical and Subjective, Team and Individual tasks
def filter_tasks(data_array, tasks="ES", group="TI"):
    tasks = list(tasks)
    group = list(group)
    # Only keep rows matching task criteria
    data_array = [row for row in data_array if row[1] in tasks]
    data_array = [row for row in data_array if row[2] in group]

    return data_array


# Generates a 3d array with the episodes per season, from a 2d array of the season
# Episodes->Task->Scores
def get_episode_array(data_array):
    episode_array = []
    for task in data_array:
        episode = int(task[0])
        del task[0:3]  # we no longer need any info on task type or episode
        task = [int(elem) for elem in task]  # convert all scores in task to integers
        try:  # we don't know how many tasks in each episode
            episode_array[episode - 1].append(task)
        except:
            episode_array.append([])
            episode_array[episode - 1].append(task)

    return episode_array


# Puts tasks in given order, conserving episode task length
def reorder_tasks(ep_arr, order_arr):
    num_eps = len(ep_arr)
    ep_lens = [0] * num_eps  # list of 0s with same length as episodes
    all_tasks_old = []

    for ep_index in range(0, num_eps):
        for task in ep_arr[ep_index]:
            all_tasks_old.append(task)
            ep_lens[ep_index] += 1

    new_ep_arr = []
    index = 0
    for i in range(0, len(ep_lens)):
        new_ep_arr.append([])
        for j in range(0, ep_lens[i]):
            new_ep_arr[i].append(all_tasks_old[order_arr[index]])
            index += 1

    return new_ep_arr


# Returns a new episode array, with tasks randomly distributed into the episodes
def rand_ep_arr(ep_arr):
    num_tasks = 0
    for ep in ep_arr:
        for task in ep:
            num_tasks += 1
    order_arr = []
    for i in range(num_tasks - 1, -1, -1):
        order_arr.append(i)

    random.shuffle(order_arr)

    return reorder_tasks(ep_arr, order_arr)

