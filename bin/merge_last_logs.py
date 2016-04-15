"""
Merge output from multiple lastlog outputs to give a single last log
"""

import os
import sys

import argparse
import re
import dateutil.parser

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="")
    parser.add_argument('-l', help='lastlog file(s). You can provide multiple -l at once', action='append', required=True)
    args = parser.parse_args()

    # the string is white space separated and looks like
    # redwards         pts/0    anthill          Thu Feb 11 16:39:56 -0800 2016
    # redwards         pts/42   rohan.sdsu.edu   Wed Apr 13 17:14:03 -0700 2016

    access = {}
    log = {}
    never = {}

    for f in args.l:
        with open(f, 'r') as fin:
            for l in fin:
                if 'Never logged in' in l:
                    p = l.split()
                    never[p[0]] = l
                    continue
                m = re.match('(\S+)\s+(\S+)\s+(\S+)\s+(.*?)$', l)
                if not m:
                    sys.stderr.write("Can't parse: '{}'\n".format(l))
                    continue
                if m.group(1) not in access:
                    try:
                        access[m.group(1)] = dateutil.parser.parse(m.group(4))
                        log[m.group(1)] = l
                    except:
                        sys.stderr.write("Can't parse date from '{}' in '{}'\n".format(m.group(4), l.strip()))
                elif dateutil.parser.parse(m.group(4)) > access[m.group(1)]:
                    access[m.group(1)] = dateutil.parser.parse(m.group(4))
                    log[m.group(1)] = l

# delete the never logged in if they did
sys.stderr.write("{} never logged in\n".format(len(never.keys())))
for k in log:
    if k in never:
        never.pop(k)
sys.stderr.write("{} never logged in\n".format(len(never.keys())))

print(never.values())

ke = sorted(log, key=access.__getitem__)
for l in ke:
    sys.stdout.write(log[l])