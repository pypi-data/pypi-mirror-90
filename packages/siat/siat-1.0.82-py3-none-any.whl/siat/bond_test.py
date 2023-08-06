# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

import os; os.chdir("S:/siat")
from siat.cryptocurrency import *



fsym = "ETH"; tsym = "USD"
begdate="2020-03-01"; enddate="2020-05-31"
markets=fetchCrypto_Exchange(fsym,tsym)
cp=fetchCrypto_Price_byExchList(fsym,tsym,markets,begdate,enddate)
dist1,dist2=calcSpread_in2Markets(cp)
print("Average inter-market spread:", dist1)
print("Inter-market spread volatility:", dist2)
