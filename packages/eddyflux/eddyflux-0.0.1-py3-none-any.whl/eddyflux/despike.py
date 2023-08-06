# -*- coding: utf-8 -*-
import numpy as np
from scipy.stats import zscore
from scipy import interpolate as itpl
from collections import namedtuple
from itertools import groupby
"""
Created on Sat Jan  2 09:14:14 2021

@author: University of Manitoba - CEOS
@website: https://github.com/UofM-CEOS/flux_capacitor
"""
VickersMahrt = namedtuple("VickersMahrt",
                          ["x", "nspikes", "ntrends", "kclass"])

def window_indices(idxs, width, step=None):
    """List of sliding window indices across an index vector
    Parameters
    ----------
    idx : numpy.ndarray
        A 1-D index vector.
    width : int
        Window width.
    step : int, optional
        Step size for sliding windows.
    Returns
    -------
    list
        List of tuples, each with the indices for a window.
    """
    return zip(*(idxs[i::step] for i in range(width)))

def get_VickersMahrt(x, zscore_thr, nrep_thr):
    """Vickers Mahrt computations in a window
    Parameters
    ----------
    x : numpy.ndarray
        A 1-D signal vectors to be despiked.
    zscore_thr : float
        The zscore beyond which an observation is considered to be an
        outlier.
    nrep_thr : int
        The maximum number of consecutive outliers that should occur for a
        spike to be detected.
    Returns
    -------
    VickersMahrt : tuple
        Tuple with (index, name in brackets):
        numpy.ndarray [0, `x`]
            1-D array with interpolated input.
        numpy.int [1, `nspikes`]
            Number of spikes detected.
        numpy.int [2, `ntrends`]
            Number of outlier trends detected.
        numpy.ndarray [3, `kclass`]
            1-D array of the same size as input, indicating the
            classification `k` for each measurement. k=0: measurement
            within plausibility range, k=[-1 or 1]: measurement outside
            plausibility range, abs(k) > 1: measurement is part of an
            outlier trend.
    """
    z = zscore(x)
    # Discern between outliers above and below the threshold
    isout_hi, isout_lo = (z > zscore_thr), (z < -zscore_thr)
    n_outs = sum(isout_hi) + sum(isout_lo)
    # Set categorical x: 0 (ok), 1 (upper outlier), -1 (lower outlier)
    xcat = np.zeros(x.shape, dtype=np.int)
    xcat[isout_hi] = 1
    xcat[isout_lo] = -1
    if n_outs > 0:
        # Create tuples for each sequence indicating whether it's outliers
        # and its length.
        grps = [(val, len(list(seq))) for val, seq in groupby(xcat)]
        vals = np.array([k[0] for k in grps])
        lens = np.array([k[1] for k in grps])
        is_spike = (vals != 0) & (lens <= nrep_thr)
        nspikes = sum(is_spike)
        # We tally trends as well
        is_trend = (vals != 0) & (lens > nrep_thr)
        ntrends = sum(is_trend)
        # If we have trends, loop through each one, knowing the length of
        # the spike and where we are along the input series.
        if ntrends > 0:
            trends = zip(vals[is_trend], lens[is_trend],
                         np.cumsum(lens)[is_trend])
            for i in trends:
                # Double the categorical value for trends and consider
                # these OK for interpolation. So abs(xcat) > 1 are trends.
                xcat[(i[2] - i[1]):i[2]] = i[0] * 2
        # Now we are left with true outliers to interpolate
        x_new = x.copy()
        xidx = np.arange(len(x))             # simple index along x
        isok = (xcat == 0) | (abs(xcat) > 1)  # ok if 0 or trend
        s = itpl.InterpolatedUnivariateSpline(xidx[isok],
                                              x[isok], k=1)
        x_itpl = s(xidx[~ isok])
        x_new[~ isok] = x_itpl
        return VickersMahrt(x_new, nspikes, ntrends, xcat)
    else:
        return VickersMahrt(x, 0, 0, xcat)


def despike_VickersMahrt(x, width, zscore_thr, nreps, step=None,
                         nrep_thr=None, interp_nan=True):
    """Vickers and Mahrt (1997) signal despiking procedure
    The interpolating function is created by the
    InterpolatedUnivariateSpline function from the scipy package, and uses
    a single knot to approximate a simple linear interpolation, so as to
    keep the original signal as untouched as possible.
    Parameters
    ----------
    x : numpy.ndarray
        A 1-D signal vectors to be despiked.
    width : int
        Window width.
    step : int, optional
        Step size for sliding windows.  Default is one-half window width.
    zscore_thr : float
        The zscore beyond which an observation is considered to be an
        outlier.  Default is zero.
    nrep_thr : int, optional
        The maximum number of consecutive outliers that should occur for a
        spike to be detected.  Default: 3.
    nreps: int, optional
        How many times to run the procedure.  Default is zero.
    interp.nan : bool, optional
        Whether missing values should be interpolated.  Interpolated values
        are computed after despiking.  Default is True.
    Returns
    -------
    VickersMahrt : tuple
        Tuple with (index, name in brackets):
        numpy.ndarray [0, `x`]
            1-D array with despiked input.
        numpy.int [1, `nspikes`]
            Number of spikes detected.
        numpy.int [2, `ntrends`]
            Number of outlier trends detected.
        numpy.int [3, `kclass`]
            Number of iterations performed.
    """
    if step is None:            # set default step as
        # step = width / 2        # one-half window size
        # sz394: step should be integer
        step = width // 2        # one-half window size
    if nrep_thr is None:
        nrep_thr = 3
    nspikes, ntrends = 0, 0
    xout = x.copy()
    # Following EddyUH implementation, fill missing values with nearest
    # value for the purpose of spike and trend detection.  This ensures
    # that we can always calculate zscores.
    is_missing = np.isnan(np.array(xout))  # need to coerce to np array
    xidx = np.arange(len(xout))            # simple index along x
    f_itpl = itpl.interp1d(xidx[~ is_missing], xout[~ is_missing],
                           kind="nearest", fill_value="extrapolate")
    x_nonan = f_itpl(xidx)
    # Get a series of tuples with indices for each window
    idxl = window_indices(range(len(x)), width, step)
    nloops = 0
    while nloops < nreps:
        nspikes_loop = 0
        for w in idxl:
            winidx = [i for i in w]  # indices of current window
            xwin = x_nonan[winidx]   # values for the current window
            xnew, nsp, ntr, xmask = get_VickersMahrt(xwin, zscore_thr,
                                                     nrep_thr)
            nspikes_loop += nsp
            ntrends += ntr
            x_nonan[winidx] = xnew
        nloops += 1
        # Increase zscore_thr by 0.3, instead of 0.1 as in V&M (1997),
        # following EddyUH implementation
        zscore_thr += 0.3
        if nspikes_loop > 0:
            nspikes += nspikes_loop
        else:                   # Stop if we haven't found any new spikes
            break
    # Interpolate through missing values, if requested (default).
    nmissing = np.count_nonzero(is_missing)
    if (nmissing > 0) and interp_nan:
        s = itpl.InterpolatedUnivariateSpline(xidx[~ is_missing],
                                              xout[~ is_missing], k=1)
        x_itpl = s(xidx[is_missing])
        xout[is_missing] = x_itpl

    return VickersMahrt(xout, nspikes, ntrends, nloops)