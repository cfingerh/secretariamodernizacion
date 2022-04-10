#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Oct 15 09:05:49 2021

@author: christian
"""
circum=7
radio=circum/2/3.1416
3.14*radio*radio
(3.9-1)/8

import json
import numpy as np
import matplotlib 

f = open('fishing.json',)

data = json.load(f)


def sorted_enumerate(seq):
    return [i for (v, i) in sorted((v, i) for (i, v) in enumerate(seq))]

def get_doublesquare(data, x,y):
    total_rev=0
    for deltaX in [0,1]:
        for deltaY in [0,1]:
            for k in data:
                if k.get("x") == x+deltaX and k.get("y")==y+deltaY:
                    rev = k.get("yearly_revenue")  
                    if np.isnan(rev):
                        rev=0
                    total_rev+=rev
    return total_rev
    print("coordinate not found {} {}".format(x,y))

doubles = []
XN=[]
YN=[]
for X in range(49):
    for Y in range(49):
        rev = get_doublesquare(data, X+1,Y+1)
        if np.isnan(rev):
            rev=0
            XN.append((X+1))
            YN.append((Y+1))
        
        double = {
            'X':X+1,
            'Y':Y+1,
            'rev':rev}
        doubles.append(double)
            
revenues_array= [f.get("rev") for f in doubles]

sorted_enumerate(revenues_array)[-3:]

print(doubles[sorted_enumerate(revenues_array)[-3]])
print(doubles[sorted_enumerate(revenues_array)[-2]])
print(doubles[sorted_enumerate(revenues_array)[-1]])

matplotlib.pyplot.scatter(XN,YN)

