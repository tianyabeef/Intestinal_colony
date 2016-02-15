#!/usr/bin/env python
# -*- coding: utf-8 -*- #

import  argparse
import  sys
import  os
from collections import OrderedDict
def read_params(args):
    parser = argparse.ArgumentParser(description='''cat gene_profile ;example LC-VS-AS ''')
    parser.add_argument('-i1', '--gene_profile1', dest='gene_profile1', metavar='FILE', type=str, required=True,
                        help="set the gene profile")
    parser.add_argument('-i2', '--gene_profile2', dest='gene_profile2', metavar='FILE', type=str, required=True,
                        help="set the gene profile")
    parser.add_argument('-o', '--out_file', dest='out_file', metavar='FILE', type=str, required=True,
                        help="set the output file")
    args = parser.parse_args()
    params = vars(args)
    return params
if __name__ == '__main__':
    params = read_params(sys.argv)
    gene_profile1 = params["gene_profile1"]
    gene_profile2 = params["gene_profile2"]
    otu_dir,fileName = os.path.split(params['out_file'])
    try:
        os.mkdir(otu_dir)
    except OSError:
        sys.stderr.write("filt %s exit\n" % (otu_dir))
    profile1 = OrderedDict()
    profile2 = OrderedDict()
    with open(gene_profile1,mode="r") as fq , open(gene_profile2,mode="r") as fq2:
        head = fq.next()
        tab = head.strip().split("\t")
        tab.insert(0,"gene_name")
        profile1["gene_name"] = head.rstrip()
        for line in  fq:
            tab = line.strip().split("\t")
            profile1[tab[0]] = line.strip()
        head = fq2.next()
        tab = head.strip().split("\t")
        profile2['gene_name'] =("\t").join(tab)
        for line in fq2:
            tab = line.strip().split("\t")
            key = tab.pop(0)
            profile2[key]  =("\t").join(tab)
    with open(params['out_file'],mode="w") as outfq:
        for key,value in profile1.items():
            if profile2.has_key(key):
                outfq.write("%s\t%s\n" % (value,profile2[key]))
            else:
                sys.stderr.write("no key %s\n" % (key))

