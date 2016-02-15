# -*- coding: utf-8 -*- #

import  argparse
import  sys
import  os
import re
from collections import OrderedDict
def read_params(args):
    parser = argparse.ArgumentParser(description='''cat gene_profile ;example LC-VS-AS ''')
    parser.add_argument('-i', '--gene_profile', dest='gene_profile', metavar='FILE', type=str, required=True,
                        help="set the gene profile")
    parser.add_argument('-cutoff', '--cutoff', dest='cutoff', metavar='NUMBER', type=float, required=True,
                        help="cut off is the num of abundance")
    parser.add_argument('-o', '--out_file', dest='out_file', metavar='FILE', type=str, required=True,
                        help="set the output file")
    args = parser.parse_args()
    params = vars(args)
    return params
if __name__ == '__main__':
    params = read_params(sys.argv)
    gene_profile = params['gene_profile']
    cutoff = params['cutoff']
    out_flie = params['out_file']
    out_dir,fileName = os.path.split(out_flie)

    tab_out = OrderedDict()
    tab_in = OrderedDict()
    num_all = 0
    num_out = 0
    num_filter = 0
    with open(out_flie,mode="w") as outfq:
        with open(gene_profile,mode="r") as fq:
            head = fq.next()
            outfq.write("%s\n" % "\t".join(re.split(r'[\t\s]',head.strip())))
            for line in fq:
                num_all += 1
                zero_num = 0
                tabs = re.split(r'[\t\s]',line.strip())
                key = tabs.pop(0)
                for tab in tabs:
                    if float(tab)==0:
                        zero_num += 1
                if 1-(float(zero_num)/float(len(tabs))) >= cutoff:
                    num_out +=1
                    outfq.write("%s\t%s\n" % (key,"\t".join(tabs)))
                else:
                    num_filter += 1
    if out_dir == None or out_dir == "":
        out_dir = "./"
    log = "%s/log" % out_dir
    if os.path.isfile(log):
       os.remove(log)
    with open("%s/log" % out_dir,mode="a") as outfq2:
            outfq2.write("%s\t%s\t%s\n" % ("all","out","filter"))
            outfq2.write("%s\t%s\t%s\n" % (num_all,num_out,num_filter))
