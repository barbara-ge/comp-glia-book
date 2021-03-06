"""
plot_utils.py

Module containing several methods related to plotting, formatting axes, etc.

Methods:
- hexc(rgb)
  Provides HEX color encoding given RGB tuple.
- adjust_spines(ax, spines, position=0, smart_bounds=False)
  Format axis spines.
- adjust_ylabels(ax,x_offset=0)
  Spacing for y-axis label.

v2.0 - Added CustomColorMap
Maurizio De Pitta', INRIA, January 31st, 2018.

v1.0
Maurizio De Pitta', INRIA, January 31st, 2018.
"""

import numpy as np
import matplotlib.colors as mcolors

def hexc(rgb):
    """
    Simple function to format RGB-to-HEX colors appropriately.

    Input arguments:
    - rgb  : RGB tuple

    Return:
    - color string in HEX format
    """

    return '#%02x%02x%02x' % rgb

def adjust_spines(ax, spines, position=0, smart_bounds=False):
    """
    Set custom visibility and position of axes

    ax       : Axes
     Axes handle
    spines   : List
     String list of 'left', 'bottom', 'right', 'top' spines to show
    position : Integer
     Number of points for position of axis
    """
    for loc, spine in ax.spines.items():
        if loc in spines:
            spine.set_position(('outward', position))  # outward by 10 points
            spine.set_smart_bounds(smart_bounds)
        else:
            spine.set_color('none')  # don't draw spine

    # turn off ticks where there is no spine
    if 'left' in spines:
        ax.yaxis.set_ticks_position('left')
    elif 'right' in spines:
        ax.yaxis.set_ticks_position('right')
    else:
        # no yaxis ticks
        ax.yaxis.set_ticks([])
        ax.yaxis.set_tick_params(size=0)

    if 'bottom' in spines:
        ax.xaxis.set_ticks_position('bottom')
    elif 'top' in spines:
        ax.xaxis.set_ticks_position('top')
    else:
        # no xaxis ticks
        ax.xaxis.set_ticks([])
        ax.xaxis.set_tick_params(size=0)

def adjust_ylabels(ax,x_offset=0):
    '''
    Scan all ax list and identify the outmost y-axis position. Setting all the labels to that position + x_offset.
    '''
    if np.size(ax)==1:
        # Makes ax iterable
        ax = [ax]

    xc = 0.0
    for a in ax:
        xc = min(xc, (a.yaxis.get_label()).get_position()[0])

    for a in ax:
        a.yaxis.set_label_coords(xc + x_offset, (a.yaxis.get_label()).get_position()[1])

def set_axlw(ax, lw=1.0):
    '''
    Adjust axis line width
    '''
    for axis in ax.spines.keys():
        ax.spines[axis].set_linewidth(lw)

def set_axfs(ax, fs=14):
    '''
    Adjust axis label font size
    '''
    ax.xaxis.set_tick_params(labelsize=fs)
    ax.yaxis.set_tick_params(labelsize=fs)

def CustomColormap(vlims, cticks, color_list, cmap_name='custom'):
    """
    Create custom colormap.

    vlims      : Limits of colormap (i.e. range of values in the provided data)
    cticks     : Array-like of size N of ticks to center different colors
    color_list : Array-like of size N of different colors. Colors can be specified by any of the allowed means
    cmap_name  : String for colormap name

    NOTE: for cticks = [T1, T2, T3...] and color_list = [C1, C2, C3, ...], the colormap is generated by LinearSegmentedColormap
    in a way such that C1 is at T1 and fades towards C2. C2 is in T2 and fades towards C3. C3 is in T3 and so on.

    Return:
        cmap   : colormap object to be used by any artist instance that requires it.

    Example of use:

    DarkOrange = pu.hexc((255,127,14))
    DarkGreen  = pu.hexc((44,160,44))
    cmap = CustomColormap(vlims,np.r_[vlims[0],1,vlims[-1]],[DarkOrange,'white',DarkGreen],'OrGr')
    """
    assert len(color_list) == len(cticks), "Color Ticks must be in the same number of colors"
    # Create ad-hoc custom colormap
    vlims = np.asarray(vlims, dtype=float)
    cticks = np.asarray(cticks, dtype=float)
    cticks_norm = (cticks - vlims[0]) / np.diff(vlims)
    colors = [(cticks_norm[i], color_list[i]) for i in xrange(len(color_list))]
    cmap = mcolors.LinearSegmentedColormap.from_list(name=cmap_name, colors=colors, N=256)
    return cmap