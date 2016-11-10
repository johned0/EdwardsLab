"""
Plot a heatmap of the coverage data from coverage_depth.py
"""

import os
import sys

import argparse
import matplotlib.pyplot as plt
import numpy as np
import math



if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Plot a heatmap")
    parser.add_argument('-f', help='file of tab delimited data', required=True)
    parser.add_argument('-w', help='window to use (default=1000)', default=1000, type=int)
    parser.add_argument('-n', help="column number to start at (default = 1; 0 indexed)", default=1, type=int)
    parser.add_argument('-l', help="Log normalize the data", action="store_true")
    parser.add_argument('-o', help='output file to save figure')
    parser.add_argument('-m', help='maximum value to use for any average', type=float)
    args = parser.parse_args()

    header = None
    data = []
    row_labels = []
    eps = 0.00000001 # epsilon since we can't do log 0

    with open(args.f, 'r') as f:
        for l in f:
            if l.startswith("#"):
                continue
            p = l.strip().split("\t")
            if len(p) > args.n:
                row_labels.append(p[0])
                s = [int(x) for x in p[args.n:]]
                counter = 0
                total = 0
                thisrow = []
                for i in range(args.n, len(s)):
                    total += s[i]
                    counter += 1
                    if counter == args.w:
                        n = 1.0 * total/counter
                        if args.m and n > args.m:
                            n = args.m
                        if n:
                            if args.l:
                                thisrow.append(1.0 * math.log(n)/math.log(10))
                            else:
                                thisrow.append(n)
                        else:
                            if args.l:
                                thisrow.append(eps)
                            else:
                                thisrow.append(0)
                        counter = 0
                        total = 0
                data.append(thisrow)


    npd = np.array(data)

    xlabels = []
    for i in range(len(data[1])):
        xlabels.append(i * args.w)

    allxlabels = []
    for i in range(len(data)):
        allxlabels.append(xlabels)
    allxlabelsd = np.array(allxlabels)

    fig, ax = plt.subplots()
    ax.xaxis.set_ticks_position('none')
    ax.yaxis.set_ticks_position('none')
    #xtl = ax.get_xticklabels()
    #ax.set_xticklabels(xlabels)

    ax.set_xlim(0, len(data[0]))
    ax.set_ylim(0, len(data))

    ax.set_xlabel("Position in genome (x100 bp)")
    ax.set_ylabel("Metagenome number")

    heatmap = ax.pcolor(npd, cmap=plt.cm.Blues)
    # heatmap = ax.pcolor(allxlabelsd, npd)

    # legend
    cbar = plt.colorbar(heatmap)
    if args.l:
        cbar.set_label('log(sequence coverage)', rotation=270)
    else:
        cbar.set_label('sequence coverage')


    if args.o:
        plt.savefig(args.o)
    else:
        plt.show()