#!/usr/bin/env python
# -*- coding: utf-8 -*- #
__author__ = "huangy"
__copyright__ = "Copyright 2016, The metagenome Project"
__version__ = "1.0.0-dev"

import pandas as pd
import sys
from datetime import datetime

def get_percent(data,sum):
    result = {}
    result["0.1"]=data[(data<=sum*0.1) & (data>0)].sum()
    result["0.2"]=data[(data<=sum*0.2) & (data>sum*0.1)].sum()
    result["0.3"]=data[(data<=sum*0.3) & (data>sum*0.2)].sum()
    result["0.4"]=data[(data<=sum*0.4) & (data>sum*0.3)].sum()
    result["0.5"]=data[(data<=sum*0.5) & (data>sum*0.4)].sum()
    result["0.6"]=data[(data<=sum*0.6) & (data>sum*0.5)].sum()
    result["0.7"]=data[(data<=sum*0.7) & (data>sum*0.6)].sum()
    result["0.8"]=data[(data<=sum*0.8) & (data>sum*0.7)].sum()
    result["0.9"]=data[(data<=sum*0.9) & (data>sum*0.8)].sum()
    result["1"]=data[(data<=sum) & (data>sum*0.9)].sum()
    return pd.Series(result)



if __name__ == '__main__':

    script,input_file,out_file,cut_off = ["","D:\\Workspaces\\gene_profile\\test","D:\\Workspaces\\gene_profile\\testd",4]
    reader = pd.read_csv(input_file, iterator=True, header=0,index_col=0,sep="\t")
    loop = True
    chunkSize = 10000
    chunks = []
    sum_list = []
    out_result = {}
    print "start read file\n"
    groups = ["A1","A2","A3","B1","B2","B3","C1","C2","C3"]
    while loop:
      try:
        start = datetime.now()
        chunk = reader.get_chunk(chunkSize)
        sum_tmp = chunk.sum(axis=0)
        sum_list.append(sum_tmp)
      except StopIteration:
        loop = False
        print "Iteration is stopped.\n"
    sum_totel = pd.DataFrame(sum_list).sum(axis=0)
    sum_totel.to_csv("%s_sum.txt" % out_file,encoding="utf-8",sep="\t")
    reader = pd.read_csv(input_file, iterator=True, header=0,index_col=0,sep="\t")
    loop = True
    chunkSize = 10000
    chunks = []
    while loop:
      try:
        start = datetime.now()
        chunk = reader.get_chunk(chunkSize)
        for ind,group in enumerate(groups):
            temp = chunk[group]
            if out_result.has_key(group):
                out_result[group].append(get_percent(temp,sum_totel[ind]))
            else:
                out_result[group] = get_percent(temp,sum_totel[ind])
      except StopIteration:
        loop = False
        print "Iteration is stopped.\n"
    for key,value in out_result.items():
        if value is not None:
            sum = pd.DataFrame(value).sum(axis=0)
            sum.to_csv("%s_%s.txt" % (out_file,key),encoding="utf-8",sep="\t")
        else:
            print "%s is None\n" % key