#!/usr/bin/env python

#
# Plots a two-column csv file using matplotlib.
# The first row of the csv file is assumed to contain axis labels.
#
import collections
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
    rownum = 0
    datadict = {"current": [],
                "voltage": [],
                "datetime": [],
                }
    with open(filename, "rb") as f:
        reader = csv.reader(f, delimiter=";")
        for row in reader:
            rownum += 1
            if len(row) != 3 or not all(row):
                print "WARNING: skipped invalid row {}".format(rownum)
                continue
            if isinstance(row, collections.MutableMapping):
                for key in row:
                    row[key] = float(row[key])
                row["datetime"] = datetime.datetime.fromtimestamp(row["datetime"])
                rowdict = row
            else:
                rowdict = dict()
                row = map(float, row)
                rowdict["datetime"] = datetime.datetime.fromtimestamp(row[0])
                rowdict["current"] = row[1] / 1e3
                rowdict["voltage"] = row[2] / 1e6

            for key in datadict:
                datadict[key].append(rowdict[key])

    return datadict


def make_figure(datadict):
    if not "datetime" in datadict:
        raise ValueError(
            "datadict must have at least a 'datetime' key / series")

    fig, axarr = plt.subplots(len(datadict), sharex=True)
    fig.set_size_inches(18.5, 10.5)

    date_formatter = matplotlib.dates.DateFormatter("%H")
    axarr[0].xaxis.set_major_formatter(date_formatter)

    times = datadict["datetime"]

    plt.grid(True)

    for key, ylabel, ax in zip(("current", "voltage"),
                               ("current [mA]", "voltage [V]"),
                               axarr):
        if key == "datetime":
            continue
        ax.plot(times, np.array(datadict[key]), label=key)
        ax.set_ylabel(ylabel)

    axarr[-1].plot(
        times,
        np.array(datadict["voltage"]) * np.array(datadict["current"]),
        label="power")
    axarr[-1].set_ylabel("power [W]")

    plt.xlabel("time [hour]")
    #plt.grid()
    #plt.legend()
    return fig


if __name__ == "__main__":
    if len(sys.argv) <= 1:
        print "usage: %s [csv-file]" % sys.argv[0]
        quit()
    else:
        fig = make_figure(get_data(sys.argv[1]))

        if os.environ.get("DISPLAY"):
            plt.show()
        else:
            plt.savefig("energiador.svg")

