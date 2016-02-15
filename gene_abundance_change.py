#!/usr/bin/env python
# -*- coding: utf-8 -*- #

import argparse
import sys
from pandas import Series, DataFrame
import pandas as pd
import os

def read_params(args):
    parser = argparse.ArgumentParser(description='''cat gene_profile ;example LC-VS-AS ''')
    parser.add_argument('-i', '--gene_profile', dest='gene_profile', metavar='FILE', type=str, required=True,
                        help="set the gene profile")
    parser.add_argument('-cutoff',dest="cutoff",metavar="number",type=float,required = True,help = "set cutoff abundance >7e-7 change 1")
    parser.add_argument('-o', '--out_file', dest='out_file', metavar='FILE', type=str, required=True,
                        help="set the output file")
    args = parser.parse_args()
    params = vars(args)
    return params
if __name__ == '__main__':
    params = read_params(sys.argv)
    gene_profile = params['gene_profile']
    cutoff = params['cutoff']
    out_file = params['out_file']
    dir = os.path.split(out_file)
    if os.path.exists(dir):
        os.remove(dir)
    else:
        os.mkdir(dir)
    gene_abundance = pd.DataFrame.from_csv(gene_profile,sep="\t")
    gene_abundance[gene_abundance>=cutoff] = 1
    gene_abundance[gene_abundance<cutoff] = 0
    gene_abundance.to_csv(out_file,encoding="utf-8",sep="\t")
    sum_abundance = gene_abundance.values.sum

    with open(gene_profile,mode="r") as fq :
        head = fq.next()
    with open("%s/sum.txt" % dir,mode="w") as fqout:
        fqout.write(head)
        fqout.write(sum_abundance)
