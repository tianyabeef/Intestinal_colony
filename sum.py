#!/usr/bin/env python
# -*- coding: utf-8 -*- #
import pandas as pd
import numpy as np
import sys
import argparse
import os
import datetime
def read_params(args):
    parser = argparse.ArgumentParser(description='''cat gene_profile ;example LC-VS-AS ''')
    parser.add_argument('-i', '--gene_profile', dest='gene_profile', metavar='FILE', type=str, required=True,
                        help="set the gene profile")
    parser.add_argument('-o', '--out_file', dest='out_file', metavar='FILE', type=str, required=True,
                        help="set the output file")
    args = parser.parse_args()
    params = vars(args)
    return params
if __name__ == '__main__':
    start = datetime.datetime.now()
    params = read_params(sys.argv)
    gene_profile = params['gene_profile']
    out_file = params['out_file']
    df = pd.DataFrame.from_csv(gene_profile,sep="\t")
    #row sum
    sum_value = df.values.sum(axis=0)
    head = os.popen('head -n 1 %s' % gene_profile)
    with open(out_file,mode="w") as outfq:
        outfq.write(head)
        outfq.write(pd.DataFrame(sum_value).T)
    print sum_value
    end = datetime.datetime.now()
    print (start-end).seconds
