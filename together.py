#!/usr/bin/env python
# -*- coding: utf-8 -*- #
import argparse
import sys
from collections import OrderedDict

import pandas as pd
import os


def read_params(args):
    parser = argparse.ArgumentParser(description='''Health among common genes''')
    parser.add_argument('-l', '--list', dest='list', metavar='FILE', type=str, required=True,
                        help="set the gene profile of list file")
    parser.add_argument('-o', '--out_file', dest='out_file', metavar='FILE', type=str, required=True,
                        help="set the output dir")
    args = parser.parse_args()
    params = vars(args)
    return params

if __name__ == '__main__':
    params = read_params(sys.argv)
    file_list = params['list']
    out_file = params['out_file']
    out_dir = os.path.dirname(out_file)
    gene = OrderedDict()
    marker_id = ""
    with open(file_list,mode='r') as fq:
        tabs = fq.next().rstrip().split("\t")
        group =tabs[0]
        df = pd.DataFrame.from_csv(tabs[1],sep="\t")
        gene[group] = df
        upward_df = df
        marker_id = df.index
        for line in fq:
            tabs = line.rstrip().split("\t")
            group =tabs[0]
            df = pd.DataFrame.from_csv(tabs[1],sep="\t")
            gene[group] = df
            marker_id = df.index.join(marker_id,how="inner")
            upward_df = df.join(upward_df,how="inner",rsuffix='_%s'% group)
    upward_df.to_csv("%s/sel.csv" % out_dir,encoding="utf-8",sep="\t")
    with open(out_file,mode="w") as outfq:
        for value in list(marker_id):
            outfq.write("%s\n" % value)
