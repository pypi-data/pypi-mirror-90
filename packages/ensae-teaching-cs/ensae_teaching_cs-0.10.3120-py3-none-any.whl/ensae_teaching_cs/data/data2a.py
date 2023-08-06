"""
@file
@brief Data mostly for the first year.
"""
from .data_helper import any_local_file


def anyfile(name, local=True, cache_folder=".", filename=True):
    """
    Returns any file in sub folder `data_2a
    <https://github.com/sdpython/ensae_teaching_cs/tree/master/src/ensae_teaching_cs/data/data_2a>`_.

    @param          name            file to download
    @param          local           local data or web
    @param          cache_folder    where to cache the data if downloaded a second time
    @param          filename        return the filename (True) or the content (False)
    @return                         text content (str)
    """
    return any_local_file(name, "data_2a", cache_folder=cache_folder, filename=filename)


def wines_quality(local=True, cache_folder=".", filename=True):
    """
    Datasets about wines quality.
    Source : `Wine Quality Data Set
    <https://archive.ics.uci.edu/ml/datasets/Wine+Quality>`_.

    @param          local           local data or web
    @param          cache_folder    where to cache the data if downloaded a second time
    @param          filename        return the filename (True) or the content (False)
    @return                         text content (str)
    """
    return anyfile("wines-quality.csv", local=local, cache_folder=cache_folder, filename=filename)
