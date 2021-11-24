#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Nov 24 11:56:26 2021.

@author: spiros
"""


def method_l(l1, l2):
    """
    Compare two lists element-wise.

    Parameters
    ----------
    l1 : list
        First list with elements.
    l2 : list
        Second list with elements.

    Returns
    -------
    boolean
        Returns `True` if l1 is the same as l2, `False` otherwise.

    """
    return l1 == l2


def read_hoc(filename, compartment='soma'):
    """
    Read a hoc file with morphology.

    Parameters
    ----------
    filename : str
        HOC filename from which the coordinates are extracted.
    compartment : str
        Compartment to be grouped. Default is 'soma'.

    Returns
    -------
    mdict : dict
        DESCRIPTION.
    counter : int
        Number of elements in the mdict.

    """
    # load the hoc file in a list.
    with open(filename, 'r') as file:
        lines = file.readlines()
        # remove trailing whitespace
        lines = [line.rstrip() for line in lines]

    mdict = {}
    counter = -1
    # loop over all lines
    for i, line in enumerate(lines):
        # if a line starts with `{access compartment_name` do the process
        if line.startswith('{access '+f'{compartment}'):
            counter += 1
            # Starting from two lines below, because of hoc structure
            # to the end, until a blank line exists when brake the loop.
            for j in range(i+2, len(lines)):
                if lines[j]:
                    # remove white space, if any and the `{pt3dadd(`
                    xyz = lines[j].strip().replace('{pt3dadd(', '')
                    # remove the `)}` from the end
                    xyz = xyz.replace(')}', '')
                    # Split the elemnts of the string based on commas
                    xyz = xyz.split(",")
                    # Keep only the x,y,z coordinates, withdrowing the last
                    # element.
                    xyz = xyz[:-1]
                    # if the key is not exist, create it, unless append the
                    # coordinates.
                    if f'{compartment}[{counter}]' not in mdict.keys():
                        mdict[f'{compartment}[{counter}]'] = [xyz]
                    else:
                        mdict[f'{compartment}[{counter}]'].append(xyz)
                else:
                    break
    return mdict, counter


def modify_swc(filename, fsave, compartment_list, target_id, name, mdict,
               save=True, target=False):
    """
    Modify an pre-existed SWC file.

    Parameters
    ----------
    filename : str
        Original SWC file to be modified.
    fsave : str
        Target SWC filename (modified file).
    compartment_list : list
        List with all compartments belong to a group based on HOC file.
    target_id : int
        ID of the new formed group (e.g., oblique compartments take 4).
    name : str
        The name of the initial group.
    mdict : dict
        Dictionary with all coordinates belong to a group of `name`.
    save : bool, optional
        Save the modified file `fsave`. The default is True.
    target : bool, optional
        Dummy variable to indicate that all changes will be saved in the
        `fsave` file. The default is False.

    Returns
    -------
    target : bool
        Dummy variable to indicate that all changes will be saved in the
        `fsave` file. If `save=True`, return `target=True`.

    """
    # Read the SWC file
    if not target:
        fname = filename
    else:
        fname = fsave
    with open(fname, 'r') as file:
        lines_orig = file.readlines()
        lines_orig = [line.strip() for line in lines_orig]

    for i, line in enumerate(lines_orig):
        # If line is not a SWC description, process it.
        if not line.startswith('#'):
            xyz = line.split(" ")[2:5]
            # Loop all over possible compartments with the same name
            for j in compartment_list:
                coord = mdict[f'{name}[{j}]']
                # loop for all segments in a compartment
                for l1 in coord:
                    a = method_l(xyz, l1)
                    if a:
                        # Split the string
                        line_ = line.split(" ")
                        # Change the second element (i.e., compartment ID)
                        line_[1] = str(target_id)
                        # Join all elements in one string
                        lines_orig[i] = " ".join(line_)
    if save:
        # Save the modified SWC file
        with open(fsave, 'w') as f:
            for item in lines_orig:
                f.write("%s\n" % item)
        target = True

    return target
