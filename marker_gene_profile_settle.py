#!/usr/bin/env python
# -*- coding: utf-8 -*- #
__author__ = "huangy"
__copyright__ = "Copyright 2016, The metagenome Project"
__version__ = "1.0.0-dev"

import pandas as pd
if __name__ == '__main__':

    dfdata = pd.DataFrame.from_csv("sel.csv",sep="\t")
    colname = dfdata.columns.tolist()
    out_dict = {}

    for name in colname:
        tabs = name.split("_")
        if out_dict.has_key(tabs[0]):
            continue
        else:
            out_dict[tabs[0]]=dfdata[name]
    values = out_dict.values()
    pd.concat(values,axis=1).to_csv("sel20160226.csv",encoding="utf-8",sep="\t")