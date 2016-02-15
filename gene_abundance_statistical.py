#!/usr/bin/env python
# -*- coding: utf-8 -*- #


import argparse
import sys
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
    params = read_params(sys.argv)
    gene_profile = params['gene_profile']
    out_file = params['out_file']
    with open(out_file,mode="w") as outfq:
        with open(gene_profile,mode="r") as fq:
            head = fq.next()
            tab = head.strip().split("\t")
            tab.insert(0,"gene_name")
            outfq.write("%s\n" % "\t".join(tab))
            for line in  fq:
                outfq.write(line)
