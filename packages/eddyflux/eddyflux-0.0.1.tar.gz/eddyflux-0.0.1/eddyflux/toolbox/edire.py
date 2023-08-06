# -*- coding: utf-8 -*-
"""
Created on Fri Nov 6 14:44:36 2020
Modified on Wed Dec 30 15:42:37 2020

@author: sz394@exeter.ac.uk
"""
import numpy as np
import pandas as pd
from pathlib import Path

class EdiReTbx():
    def __init__(self):
        pass
    
    def make_input_list(self, search_directory, output_file, loc = 6, screen = 0, remove_imcomplete = True, user_file_size = None):
        """
        Created on Fri Nov 6 14:44:36 2020
        Modified on Dec 30 2020: make the functions into a class.
        Search and save
        Parameters
        ----------
        search_directory : Path
            Search directory.
        output_file : Path
            Save directory.
        loc : int, optional
            The location of year in splited string by _, count starting from 0. The default is 6.
        screen : int, optional
            0: no screen output, 1: print error info, 2: print everything. The default is 0.
        remove_imcomplete : boolean, optional
            Ignore incomplete files. The default is True.
        user_file_size : float, optional
            File size threshold. The default is None.

        Returns
        -------
        None.
        
        Examples
        --------
        >>> search_directory = r"C:/Users/sz394/OneDrive - University of Exeter/Workspace/low_cost_eddy_covariance/Data/2020_09_26/Converted_200105"
        >>> output_file = r"C:/Users/sz394/OneDrive - University of Exeter/Workspace/low_cost_eddy_covariance/Data/2020_09_26/EdiRe_200105/input/input_list.txt"
        >>> ertbx = EdiReTbx()
        >>> ertbx.make_input_list(search_directory, output_file)
        """
        df = self.__search(search_directory, loc, screen, remove_imcomplete, user_file_size)
        self.__write2file(df, output_file)
        

    def __search(self, search_directory, loc, screen, remove_imcomplete, user_file_size):
        """
        Search tob file and return directories as a pandas dataframe
        Parameters
        ----------
        search_directory : Path
            Folder directory.
        loc : int
            The location of year in splited string by _, count starting from 0.
        screen : int
            0: no screen output, 1: print error info, 2: print everything.
        remove_imcomplete : boolean
            Ignore incomplete files.
        user_file_size : float
            File size threshold.

        Returns
        -------
        df : DataFrame
            Contains searched directories, columns are "directory", "year", "month", "day", "time", "file size".

        """
        #---------------------------------------------------------------------------------------------------------------------------------------
        paths = list(Path(search_directory).glob("*.dat"))

        records = []
        for pos, p in enumerate(paths):
            kwds = p.stem.split("_")
            # # example
            # kwds = "TOB1_13192_roth_200102_ts_9_2020_08_27_2300".split("_")

            if (len(kwds) > loc + 3):
                year = kwds[loc]
                month = kwds[loc + 1]
                day = kwds[loc + 2]
                minsec = kwds[loc + 3]

                if screen == 2:
                    print(year, month, day)
                if (len(year) == 4) & (len(month) == 2) & (len(day) == 2) & (len(minsec) == 4):
                    records.append([p, year, month, day, minsec, p.stat().st_size])
                else:
                    if screen:
                        print(
                            f"year length: {len(year)}, month length: {len(month)}, day length: {len(day)}"
                        )
                    else:
                        pass
            else:
                pass

        df = pd.DataFrame(records, columns = ["directory", "year", "month", "day", "time", "file size"])
        df = df.sort_values(["year", "month", "day", "time"], ascending=[True, True, True, True])

        # remove imcomplete files:
        if remove_imcomplete:
            if not user_file_size:
                max_size = df["file size"].max()
                df = df[df["file size"] == max_size]
            else:
                df = df[df["file size"] >= user_file_size]

        print("Filtering is finished...")
        return df

    def __write2file(self, df, output_file):
        with open(output_file, 'w') as f:
            f.writelines("%s\n" % placeholder.as_posix() for placeholder in df["directory"])
        print("Writting is finished...")