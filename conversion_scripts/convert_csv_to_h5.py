#
# DeepLabCut Toolbox (deeplabcut.org)
# © A. & M.W. Mathis Labs
# https://github.com/DeepLabCut/DeepLabCut
#
# Please see AUTHORS for contributors.
# https://github.com/DeepLabCut/DeepLabCut/blob/master/AUTHORS
#
# Licensed under GNU Lesser General Public License v3.0
#
"""
DeepLabCut2.0 Toolbox (deeplabcut.org)
© A. & M. Mathis Labs
https://github.com/DeepLabCut/DeepLabCut
Please see AUTHORS for contributors.

https://github.com/DeepLabCut/DeepLabCut/blob/master/AUTHORS
Licensed under GNU Lesser General Public License v3.0
"""
import os
import pandas as pd
from deeplabcut.utils import auxiliaryfunctions
from itertools import islice
from pathlib import Path


SUPPORTED_FILETYPES = "csv", "nwb"


def convertcsv2h5(config, userfeedback=True, scorer=None):
    """
    Convert (image) annotation files in folder labeled-data from csv to h5.
    This function allows the user to manually edit the csv (e.g. to correct the scorer name and then convert it into hdf format).
    WARNING: conversion might corrupt the data.

    config : string
        Full path of the config.yaml file as a string.

    userfeedback: bool, optional
        If true the user will be asked specifically for each folder in labeled-data if the containing csv shall be converted to hdf format.

    scorer: string, optional
        If a string is given, then the scorer/annotator in all csv and hdf files that are changed, will be overwritten with this name.

    Examples
    --------
    Convert csv annotation files for reaching-task project into hdf.
    >>> deeplabcut.convertcsv2h5('/analysis/project/reaching-task/config.yaml')

    --------
    Convert csv annotation files for reaching-task project into hdf while changing the scorer/annotator in all annotation files to Albert!
    >>> deeplabcut.convertcsv2h5('/analysis/project/reaching-task/config.yaml',scorer='Albert')
    --------
    """
    cfg = auxiliaryfunctions.read_config(config)
    videos = cfg["video_sets"].keys()
    video_names = [Path(i).stem for i in videos]
    folders = [Path(config).parent / "labeled-data" / Path(i) for i in video_names]
    if not scorer:
        scorer = cfg["scorer"]

    for folder in folders:
        try:
            if userfeedback:
                print("Do you want to convert the csv file in folder:", folder, "?")
                askuser = input("yes/no")
            else:
                askuser = "yes"

            if askuser in ("y", "yes", "Ja", "ha", "oui"):  # multilanguage support :)
                fn = os.path.join(
                    str(folder), "CollectedData_" + cfg["scorer"] + ".csv"
                )
                # Determine whether the data are single- or multi-animal without loading into memory
                # simply by checking whether 'individuals' is in the second line of the CSV.
                with open(fn) as datafile:
                    head = list(islice(datafile, 0, 5))
                if "individuals" in head[1]:
                    header = list(range(4))
                else:
                    header = list(range(3))
                if head[-1].split(",")[0] == "labeled-data":
                    index_col = [0, 1, 2]
                else:
                    index_col = 0
                data = pd.read_csv(fn, index_col=index_col, header=header)
                data.columns = data.columns.set_levels([scorer], level="scorer")
                guarantee_multiindex_rows(data)
                data.to_hdf(fn.replace(".csv", ".h5"), key="df_with_missing", mode="w")
                data.to_csv(fn)
        except FileNotFoundError:
            print("Attention:", folder, "does not appear to have labeled data!")