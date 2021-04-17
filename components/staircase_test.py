# -*- coding: utf-8 -*-
"""
Created on Mon Nov 30 02:14:54 2020

@author: Praca
"""

from psychopy import data
from random import choice

staircase = {
    'nTrials': 10,
    'nReversals': 10,
    'startVal': 0.2,
    'stepType': 'lin',
#    'stepSizes': np.log(10/8)/np.log(10),
    'stepSizes': [0.05,0.05,0.02,0.02,0.001],
    'minVal': 0,
    'maxVal': 1,
    'nUp': 1,
    'nDown': 1,
    'applyInitalRule': False
    }

stair = data.StairHandler(**staircase)

for value in stair:
    x = choice([0,1])
    print(x, value)
    stair.addResponse(x)
    
print(type(stair).__name__=='StairHandler')