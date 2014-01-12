#!/usr/bin/env python

#
# Plots a two-column csv file using matplotlib.
# The first row of the csv file is assumed to contain axis labels.
#
import csv
import datetime
import os
import sys

import matplotlib
if not os.environ.get("DISPLAY"):
    matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np



def get_data(filename):
    times = []
    y1 = []
    y2 = []
    with open(filename, "rb") as f:
        reader = csv.reader(f, delimiter=";")
        for row in reader:
            if row[1] != "" and row[2] != "":
                row = map(float, row)
                times.append(datetime.datetime.fromtimestamp(row[0]))
                y1.append(row[1])
                y2.append(row[2])
    return times, y1, y2


def make_figure(times, y1, y2):
    fig, axarr = plt.subplots(3, sharex=True)
    date_formatter = matplotlib.dates.DateFormatter("%H")
    axarr[0].xaxis.set_major_formatter(date_formatter)
    plt.grid(True)
    axarr[0].plot(times, np.array(y1) / 1e3, label="current")
    axarr[0].set_ylabel("current [mA]")
    #plt.grid()
    axarr[1].plot(times, np.array(y2) / 1e6, label="voltage")
    axarr[1].set_ylabel("voltage [V]")
    #plt.grid()
    axarr[2].plot(times, np.array(y2) / 1e6 * np.array(y1) / 1e6, label="power")
    axarr[2].set_ylabel("power [W]")
    plt.xlabel("time [hour]")
    #plt.grid()
    #plt.legend()
    return fig


if __name__ == "__main__":
    if len(sys.argv) <= 1:
        print "usage: %s [csv-file]" % sys.argv[0]
        quit()
    else:
        fig = make_figure(*get_data(sys.argv[1]))

        if os.environ.get("DISPLAY"):
            plt.show()
        else:
            plt.savefig("energiador.svg")

