#!/usr/bin/env python
# -*- coding: utf-8 -*- #

import argparse
import sys
from pandas import Series, DataFrame
import pandas as pd
import os
import shutil
import numpy as np

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
    dir,filename = os.path.split(out_file)
    if os.path.exists(dir):
        shutil.rmtree(dir)
    os.mkdir(dir)
    reader = pd.read_csv(gene_profile, iterator=True, header=0,index_col=0,sep="\t")
    loop = True
    chunkSize = 10000
    chunks = []
    print "start read file\n"
    while loop:
      try:
        chunk = reader.get_chunk(chunkSize)
        chunk[chunk>=cutoff] = 1
        chunk[chunk<cutoff] = 0
        chunks.append(chunk)
      except StopIteration:
        loop = False
        print "Iteration is stopped.\n"
    gene_abundance = pd.concat(chunks)
    #gene_abundance = pd.DataFrame.from_csv(gene_profile,sep="\t")
    gene_abundance.to_csv(out_file,encoding="utf-8",sep="\t")
    print "start row sum\n"
    sum_abundance = gene_abundance.values.sum(axis=0)
    out = pd.DataFrame(sum_abundance,index=gene_abundance.columns).T
    out.to_csv("%s/sum.txt" % dir,encoding="utf-8",sep="\t")
