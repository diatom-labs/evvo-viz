import sys
from sys import argv

import matplotlib.pyplot as plt
from datetime import datetime

def main(argv):
    filename = argv[1]
    print(filename)
    try:
        plot_pop_time(filename)
        plot_pop_message_counts(filename)

    except OSError:
        print(f"Could not read file {filename}")


def plot_pop_message_counts(filename):

    def parse_line(line):
        split_line = line.split(" ")
        return datetime.strptime(split_line[0] + '000', "%H:%M:%S.%f").timestamp()

    def get_message_timestamps(message_type):
        with open(filename) as file:
            return sorted(parse_line(line) for line in file if message_type in line)

    get = get_message_timestamps("GetSolutions")
    add = get_message_timestamps("AddSolutions")
    delete = get_message_timestamps("DeleteSolutions")

    min_time = min(min(get), min(delete), min(add))

    get = [x - min_time for x in get]
    add = [x - min_time for x in add]
    delete = [x - min_time for x in delete]

    fig, (ax1, ax2, ax3) = plt.subplots(3, sharey=True)
    ax1.hist(get, bins=100)
    ax1.set(ylabel='Get')
    ax2.hist(add, bins=100)
    ax2.set(ylabel='Add')
    ax3.hist(delete, bins=100)
    ax3.set(ylabel='Delete')

    plt.show()

def plot_pop_time(filename):
    def parse_line(line):
        split_line = line.split(" ")
        timestamp = datetime.strptime(split_line[0] + '000', "%H:%M:%S.%f").timestamp()
        count = int(split_line[-1])
        return (timestamp, count)

    with open(filename) as file:
        data = [parse_line(line) for line in file if "Current population size" in line]
    data.sort(key=lambda x: x[0])

    times = [x[0] for x in data]
    mintime = min(times)
    times = [x - mintime for x in times]
    counts = [x[1] for x in data]
    print(times)
    print(counts)

    # fig, ax = plt.subplots()
    # ax.hist(times, bins=100)
    #
    # ax.set(xlabel='time (s)', ylabel='population',
    #        title='pop/time')
    # ax.grid()
    #
    # plt.show()
    fig, ax = plt.subplots()
    ax.plot(times, counts)

    ax.set(xlabel='time (s)', ylabel='population',
           title='pop/time')
    ax.grid()

    plt.show()

if __name__ == '__main__':
    if len(argv) != 2:
        print("Call with one argument, the name of the file containing the logs.")
        sys.exit(1)

    main(argv)