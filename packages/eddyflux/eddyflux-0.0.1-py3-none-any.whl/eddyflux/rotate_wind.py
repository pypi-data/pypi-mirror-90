# -*- coding: utf-8 -*-
"""
Created on Sat Jan  2 08:25:53 2021

@author: University of Manitoba - CEOS
@website: https://github.com/UofM-CEOS/flux_capacitor
"""

import numpy as np
from collections import namedtuple
PlanarFitCoefs = namedtuple("PlanarFitCoefs",
                            ["k_vct", "tilt_coefs", "phi", "theta"])

RotatedVectors = namedtuple("RotatedVectors", ["rotated", "phi_theta"])

# Valid 3-D wind rotation methods
_VECTOR_ROTATION_METHODS = {"DR", "TR", "PF"}

def planarfit(vectors):
    """Calculate planar fit coefficients for coordinate rotation
    See Handbook of Micrometeorology (Lee et al. 2004).  Ported from
    getPlanarFitCoeffs.m from Patric Sturm <pasturm@ethz.ch>.
    Parameters
    ----------
    vectors : numpy.ndarray
        A 2-D (Nx3) array with `x`, `y`, and `z` vectors, expressed in a
        right-handed coordinate system.  These vectors may correspond to
        `u`, `v`, and `w` wind speed vectors, or inertial acceleration
        components.
    Returns
    -------
    PlanarFitCoefs : namedtuple
        namedtuple with (index and name in brackets):
        numpy.ndarray [0, `k_vct`]
            1-D array (1x3) unit vector parallel to the new z-axis.
        numpy.ndarray [1, `tilt_coefs`]
            1-D array (1x3) Tilt coefficients `b0`, `b1`, `b2`.
        numpy.float [2, `phi`]
            Scalar representing roll angle :math:`\\phi`.
        numpy.float [3, `theta`]
            Scalar representing pitch angle :math:`\\theta`.
    """
    vct_u = vectors[:, 0]
    vct_v = vectors[:, 1]
    vct_w = vectors[:, 2]
    vct_nrows = vectors.shape[0]
    sum_u = sum(vct_u)
    sum_v = sum(vct_v)
    sum_w = sum(vct_w)
    dot_uv = np.dot(vct_u, vct_v)
    dot_uw = np.dot(vct_u, vct_w)
    dot_vw = np.dot(vct_v, vct_w)
    dot_u2 = np.dot(vct_u, vct_u)
    dot_v2 = np.dot(vct_v, vct_v)
    H_arr = np.array([[vct_nrows, sum_u, sum_v],
                      [sum_u, dot_u2, dot_uv],
                      [sum_v, dot_uv, dot_v2]])
    g_arr = np.array([sum_w, dot_uw, dot_vw])
    tilt_coef = np.linalg.solve(H_arr, g_arr)
    # Estimated \phi (roll) and \theta (pitch) tilt angles
    phi_denom = np.sqrt(1 + (tilt_coef[2] ** 2))
    phi_sin = tilt_coef[2] / phi_denom
    phi_cos = 1 / phi_denom
    phi = np.arctan2(phi_sin, phi_cos)
    theta_denom = np.sqrt(1 + (tilt_coef[1] ** 2) + (tilt_coef[2] ** 2))
    theta_sin = -tilt_coef[1] / theta_denom
    theta_cos = np.sqrt((tilt_coef[2] ** 2) + 1) / theta_denom
    theta = np.arctan2(theta_sin, theta_cos)
    # Determine unit vector parallel to new z-axis
    k_2 = 1 / np.sqrt(1 + tilt_coef[1] ** 2 + tilt_coef[2] ** 2)
    k_0 = -tilt_coef[1] * k_2
    k_1 = -tilt_coef[2] * k_2
    k_vct = np.array([k_0, k_1, k_2])
    return PlanarFitCoefs(k_vct, tilt_coef, phi, theta)

def rotate_wind3d(wind3D, method="PF", **kwargs):
    """Transform 3D wind vectors to reference mean streamline coordinate system
    Use double rotation, triple rotation, or planar fit methods (Wilczak et
    al. 2001; Handbook of Micrometeorology).
    This is a general coordinate rotation tool, so can handle inputs such
    as wind speed and acceleration from inertial measurement units.
    Parameters
    ----------
    wind3D : numpy.ndarray
        A 2-D (Nx3) array with `x`, `y`, and `z` vector components,
        expressed in a right-handed coordinate system.  These may represent
        `u`, `v`, and `w` wind speed vectors, or inertial acceleration.
    method : {"DR", "TR", "PF"}, optional
        One of: "DR", "TR", "PF" for double rotation, triple rotation, or
        planar fit.
    k_vector : numpy.ndarray, optional
        1-D array (1x3) unit vector parallel to the new z-axis, when
        "method" is "PF" (planar fit).  If not supplied, then it is
        calculated.
    Returns
    -------
    RotatedVectors : namedtuple
        namedtuple with (index, name in brackets):
        numpy.ndarray [0, `rotated`]
            2-D array (Nx3) Array with rotated vectors
        numpy.ndarray [1, `phi_theta`]
            1-D array (1x2) :math:`\\phi` and :math:`\\theta` rotation
            angles.  The former is the estimated angle between the vertical
            unit coordinate vector in the rotated frame and the vertical
            unit vector in the measured uv plane, while the latter is wind
            direction in the measured uv plane.  Note these are *not* roll
            and pitch angles of the measurement coordinate frame relative
            to the reference frame.
    """
    if method not in _VECTOR_ROTATION_METHODS:
        msg = "method must be one of "
        raise ValueError(msg + ', '.join("\"{}\"".format(m) for m in
                                         _VECTOR_ROTATION_METHODS))

    if method == "PF":
        if "k_vector" in kwargs:
            k_vct = kwargs.get("k_vector")
        else:
            pfit = planarfit(wind3D)
            k_vct = pfit.k_vct
        j_vct = np.cross(k_vct, np.mean(wind3D, 0))
        j_vct = j_vct / np.sqrt(np.sum(j_vct ** 2))
        i_vct = np.cross(j_vct, k_vct)
        vcts_mat = np.column_stack((i_vct, j_vct, k_vct))
        vcts_new = np.dot(wind3D, vcts_mat)
        phi = np.arccos(np.dot(k_vct, np.array([0, 0, 1])))
        theta = np.arctan2(np.mean(wind3D[:, 1], 0),
                           np.mean(wind3D[:, 0], 0))
    else:
        # First rotation to set mean v to 0
        theta = np.arctan2(np.mean(wind3D[:, 1]),
                           np.mean(wind3D[:, 0]))
        rot1 = np.array([[np.cos(theta), -np.sin(theta), 0],
                         [np.sin(theta), np.cos(theta), 0],
                         [0, 0, 1]])
        vcts1 = np.dot(wind3D, rot1)
        # Second rotation to set mean w to 0
        phi = np.arctan2(np.mean(vcts1[:, 2]),
                         np.mean(vcts1[:, 0]))
        rot2 = np.array([[np.cos(phi), 0, -np.sin(phi)],
                         [0, 1, 0],
                         [np.sin(phi), 0, np.cos(phi)]])
        vcts_new = np.dot(vcts1, rot2)
        # Third rotation to set mean vw to 0
        if method == "TR":
            mean_vw = np.mean(vcts_new[:, 1] * vcts_new[:, 2])
            psi = 0.5 * np.arctan2(2 * mean_vw,
                                   np.mean(vcts_new[:, 1] ** 2) -
                                   np.mean(vcts_new[:, 2] ** 2))
            rot3 = np.array([[1, 0, 0],
                             [0, np.cos(psi), -np.sin(psi)],
                             [0, np.sin(psi), np.cos(psi)]])
            vcts_new = np.dot(vcts_new, rot3)

    return RotatedVectors(vcts_new, np.array([phi, theta]))