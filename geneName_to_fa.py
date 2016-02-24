#!/usr/bin/env python
# -*- coding: utf-8 -*- #
__author__ = "huangy"
__copyright__ = "Copyright 2016, The metagenome Project"
__version__ = "1.0.0-dev"
import argparse
import sys
import pandas as pd
from Bio import SeqIO
from Bio.SeqRecord import SeqRecord

def read_params(args):
    parser = argparse.ArgumentParser(description='''geneName to fasta read''')
    parser.add_argument('-n','--name',dest="name",metavar ="FILE",type=str,required=True,
                        help="gene name file")
    parser.add_argument('--gene',dest="gene_fa",metavar ="FILE",type=str,required=True,
                        help="gene fasta file")
    parser.add_argument('-o', '--out_file', dest='out_file', metavar='FILE', type=str, required=True,
                        help="set the output file")
    args = parser.parse_args()
    return args
if __name__ == '__main__':
    params = read_params(sys.argv)
    gene_name_file = params.name
    gene_file = params.gene_fa
    out_file = params.out_file
    gene_names = pd.Series.from_csv(gene_name_file,sep="\t",header=None,index_col=None).to_dict()
    for record in SeqIO.parse(open(gene_file),'fasta'):
        name = record.name
        if name in gene_names:
            out_file.write(record.format('fasta'))
