#!/usr/bin/env python
# -*- coding: utf-8 -*- #
__author__ = "huangy"
__copyright__ = "Copyright 2016, The metagenome Project"
__version__ = "1.0.0-dev"

import pandas as pd
import sys
from datetime import datetime

if __name__ == '__main__':
    script,input_file,out_file,cut_off = sys.argv
    reader = pd.read_csv(input_file, iterator=True, header=0,index_col=0,sep="\t")
    loop = True
    chunkSize = 10000
    chunks = []
    sum_list = []
    print "start read file\n"
    while loop:
      try:
        start = datetime.now()
        chunk = reader.get_chunk(chunkSize)
        sum_tmp = chunk.sum(axis=0)
        sum_list.append(sum_tmp)
      except StopIteration:
        loop = False
        print "Iteration is stopped.\n"
    sum = pd.DataFrame(sum_list).sum(axis=0)
    sum.to_csv(out_file,encoding="utf-8",sep="\t")