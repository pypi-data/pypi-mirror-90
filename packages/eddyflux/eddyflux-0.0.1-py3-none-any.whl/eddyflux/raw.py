# -*- coding: utf-8 -*-
"""
Created on Wed Dec 30 15:42:37 2020

@author: sz394@exeter.ac.uk
"""

import numpy as np
import pandas as pd
from pathlib import Path

class Raw():
    def __init__(self):
        # Variable type map, FP2 is the difficulty involving hex and endian conversion.
        self.TYPE_MAP = {
            "IEEE4": np.float32,
            "IEEE8": np.float64,
            "LONG": np.int32,
            "ULONG": np.uint32,
            "FP2": np.dtype('>H'),  # big-endian unsigned short
        }
        
    def __covert_fp2(self, val):
        """
        Covert big endian input val to normal value.

        Parameters
        ----------
        val : hex
            val is read as big endian.

        Returns
        -------
        val : float
            Normal float value.

        """
        pinf = 0x1fff
        ninf = 0x9fff
        anan = 0x9ffe
        # swap the bits (assume for small endian? sz at 2020-11-06)
        # val = ((val & 0xff00)>>8) | ((val & 0x00ff)<<8)
        # print(val)
        if ((val == pinf) or (val == ninf) or (val == anan)):
            val = np.nan
        else:
            # extract float components
            isNeg  =  not((val & 0x8000) == 0)
            Mantis =  val & 0x1FFF
            Expnt  =  (val & 0x6000) >> 13

            NV = Mantis
            NV = NV/(10.0**Expnt)

            if isNeg:
                NV = -1* NV
            val = NV
        return val

    def read(self, p, nlines = 5, lname = 1, lunit = 2, ldtype = 4):
        """
        Read Loggernet converted tob1 raw files.
        This version deals with FP2 data type.
        Parameters
        ----------
        p : str or windows path
            The location of tob1 raw file.
        nlines : int, optional
            Lines number of meta info. The default is 5.
        lname : int, optional
            Line number of variable names. The default is 1.
        lunit : int, optional
            Line number of variable units, can be 0. The default is 2.
        ldtype : int, optional
            Line number of variable dtype. The default is 4.

        Returns
        -------
        df : TYPE
            DESCRIPTION.

        """
        with open(p, "rb") as f:
            headers = []
            for l in range(nlines):
                headers.append(f.readline())
            names = headers[lname].decode().strip().replace('"', "").split(",")
            if lunit:
                units = headers[lunit].decode().strip().replace('"', "").split(",")
            types = headers[ldtype].decode().strip().replace('"', "").split(",")
            dtype = np.dtype([(n, self.TYPE_MAP[t]) for n, t in zip(names, types)])

            array = np.fromfile(f, dtype = dtype, count = -1)
            df = pd.DataFrame(array)

        if "FP2" in types:
            fp2_df = pd.DataFrame(zip(names, types), columns = ["name", "type"])
            fp2_names = fp2_df.loc[fp2_df["type"] == "FP2", "name"].tolist()
            df.loc[:, fp2_names] = df.loc[:, fp2_names].applymap(self.__covert_fp2)
            
        if "SECONDS" in  df.columns:
            fdel = df["SECONDS"].astype(np.int64) * 1000000000
            if "NANOSECONDS" in df.columns:
                fdel += df["NANOSECONDS"].astype(np.int64)

            datetime = np.datetime64('1990-01-01') + fdel.astype("timedelta64[ns]")
            datetime.name = "datetime"
            df.index = datetime
        if lunit:
            df.attrs["unit"] = dict(zip(names, units))
            # Alternative way that might trigger warnings
            # df.unit = dict(zip(names, units))
        return df