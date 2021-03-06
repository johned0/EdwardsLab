"""

"""

import os
import sys
import argparse

import matplotlib
#matplotlib.use('Agg')
import matplotlib.pyplot as plt

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="")
    parser.add_argument('-f', help='Genome average output file (from genera_per_phage_protein.py', default='/home/redwards/Desktop/gav_all_host.out')
    parser.add_argument('-n', help='taxonomy name one of: kingdom / phylum / genus / species', default='genus')
    parser.add_argument('-v', help='verbose output', action="store_true")

    args = parser.parse_args()

    ynames = {'kingdom' : 'kingdoms', 'phylum' : 'phyla', 'genus' : 'genera', 'species' : 'species'}

    col = None
    colkey = {'kingdom' : 3, 'phylum' : 4, 'genus' : 5, 'species' : 6}
    if args.n not in colkey:
        sys.stderr.write("Sorry, taxonomy name must be one of {}\n".format("|".join(list(colkey.keys()))))
        sys.exit(-1)
    col = colkey[args.n]

    want = {'Gut', 'Mouth', 'Nose', 'Skin', 'Lungs'}

    data = {}
    with open(args.f, 'r') as fin:
        for l in fin:
            p=l.strip().split("\t")
            if p[2] not in want:
                p[2] = 'All phages'
                #continue  ## comment or uncomment this to include/exclude all data
            if p[2] not in data:
                data[p[2]] = []
            data[p[2]].append(float(p[col]))

    labels = sorted(data.keys())
    scores = []
    count = 1
    ticks = []
    for l in labels:
        scores.append(data[l])
        ticks.append(count)
        count += 1

    fig = plt.figure()
    ax = fig.add_subplot(111)

    # ax.boxplot(alldata)
    vp = ax.violinplot(scores, showmeans=True)
    for i, j in enumerate(vp['bodies']):
        if i == 0:
            j.set_color('gray')
        elif i == 1:
            j.set_color('sandybrown')
        else:
            j.set_color('lightpink')

    ax.set_xlabel("Body Site")
    ax.set_ylabel("Average number of {}".format(ynames[args.n]))
    ax.set_xticks(ticks)
    ax.set_xticklabels(labels, rotation='vertical')
    ax.get_xaxis().tick_bottom()
    ax.get_yaxis().tick_left()
    fig.set_facecolor('white')

    plt.tight_layout()
    #plt.show()
    fig.savefig("/home/redwards/Desktop/bodysites.png")
