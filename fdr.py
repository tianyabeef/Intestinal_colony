# -*- coding: utf-8 -*- #

import argparse
import datetime
import os
import sys
from collections import OrderedDict
import os
def removeDir(dirPath):
    if not os.path.isdir(dirPath):
        return
    files = os.listdir(dirPath)
    try:
        for file in files:
            filePath = os.path.join(dirPath, file)
            if os.path.isfile(filePath):
                os.remove(filePath)
            elif os.path.isdir(filePath):
                removeDir(filePath)
        os.rmdir(dirPath)
    except Exception, e:
        print e

def read_params(args):
    parser = argparse.ArgumentParser(description='''cat gene_profile ;example LC-VS-AS ''')
    parser.add_argument('-i', '--gene_profile', dest='gene_profile', metavar='FILE', type=str, required=True,
                        help="set the gene profile")
    parser.add_argument('-p', '--p_valuefile', dest='p_valuefile', metavar='FILE', type=str, required=True,
                        help="set the p_value file")
    parser.add_argument('-p_cutoff', '--p_cutoff', dest='p_cutoff', metavar='NUMBER', type=float, required=True,
                        help="cut off p is the num of abundance")
    parser.add_argument('-q_cutoff', '--q_cutoff', dest='q_cutoff', metavar='NUMBER', type=float, required=True,
                        help="cut off q is the num of abundance")
    parser.add_argument('-o', '--out_dir', dest='out_dir', metavar='DIR', type=str, required=True,
                        help="set the output dir")
    args = parser.parse_args()
    params = vars(args)
    return params
if __name__ == '__main__':
    starttime = datetime.datetime.now()
    params = read_params(sys.argv)
    gene_profile_file = params['gene_profile']
    p_value_file = params['p_valuefile']
    p_cutoff = params['p_cutoff']
    q_cutoff = params['q_cutoff']
    out_dir = params['out_dir']
    fdr_dir = "%sfdr_%s_%s" % (out_dir,p_cutoff,q_cutoff)
    if os.path.exists(fdr_dir):
        removeDir(fdr_dir)
    os.mkdir(fdr_dir)
    gene_profile = OrderedDict()
    p_valuefile = OrderedDict()
    out_text = OrderedDict()
    with open(p_value_file,mode="r") as fq:
            for line in fq:
                (gene_id,p_value,q_value,enrich) = line.strip().split("\t")
                if(float(q_value) <= float(q_cutoff) and float(p_value) <= float(p_cutoff)):
                    p_valuefile[gene_id] = enrich
    with open(gene_profile_file,mode="r") as fq2:
        head = fq2.next()
        for line2 in fq2:
            tabs = line2.strip().split("\t")
            key = tabs[0]
            if p_valuefile.has_key(key):
                if out_text.has_key(p_valuefile[key]):
                    out_text[p_valuefile[key]].append(line2)
                else:
                    out_text[p_valuefile[key]] = []
                    out_text[p_valuefile[key]].append(line2)
    for key in  out_text.keys():
        with open("%s/%s" % (fdr_dir,os.path.basename(key)) , mode="w") as outfq:
            outfq.write(head)
            for value in out_text[key]:
                outfq.write(value)
    endtime = datetime.datetime.now()
    print "use mmap time:%s\n" % (endtime - starttime).seconds
