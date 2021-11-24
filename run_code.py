#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Nov 23 12:10:12 2021.

@author: spiros
"""

from opt import read_hoc
from opt import modify_swc

# HOC file to be transformed into SWC
filename = 'cell.hoc'

# Loop for all initial compartments
all_dict = {}
for comp in ['soma', 'dendrite', 'apical_dendrite']:
    mydict, _ = read_hoc(filename, comp)
    all_dict[comp] = mydict

# Load description file
filename2 = 'description_compartments.txt'
with open(filename2, 'r') as file:
    lines_d = file.readlines()
    lines_d = [line.strip() for line in lines_d]

# SWC to be modified
target = False  # help variable to make changes in a modified file.
for i, line in enumerate(lines_d):
    line = line.split(",")
    target = modify_swc(filename='n123.CNG.swc',
                        fsave='n123.CNG.modified.swc',
                        compartment_list=[int(x) for x in line[3:]],
                        target_id=int(line[0]),
                        name=line[1],
                        mdict=all_dict[line[1]],
                        save=True,
                        target=target)
