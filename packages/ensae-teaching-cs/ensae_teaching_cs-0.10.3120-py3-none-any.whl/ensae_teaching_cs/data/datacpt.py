"""
@file
@brief Data for competitions
"""
import os
import random
import pandas
from pyensae.datasource import download_data
from pyquickhelper.loghelper import noLOG
from pyquickhelper.filehelper.encryption import decrypt_stream


def data_cpt_ENSAE_2016_11(folder=".", fLOG=noLOG):
    """
    Returns the data for the competition
    :epkg:`Python 2A ENSAE 2016`,
    located on github `ensae_competition_2016.zip
    <https://github.com/sdpython/ensae_teaching_cs/raw/master/_doc/competitions/
    2016_ENSAE_2A/ensae_competition_2016.zip>`_.

    @param      folder      where to download and unzip
    @param      fLOG        logging function
    @return                 2 dataframes, one with X, Y, the others one with only X
    """
    url = "https://github.com/sdpython/ensae_teaching_cs/raw/master/_doc/competitions/2016_ENSAE_2A/"
    file = "ensae_competition_2016.zip"
    files = download_data(file, url=url, whereTo=folder, fLOG=fLOG)
    df1 = pandas.read_csv([f for f in files if f.endswith("ensae_competition_train.txt")][0],
                          header=[0, 1], sep="\t", index_col=0)
    df2 = pandas.read_csv([f for f in files if "test_X" in f][0],
                          header=[0, 1], sep="\t", index_col=0)
    return df1, df2


def data_cpt_ENSAE_2016_11_blind_set(password):
    """
    Returns the evaluation set for the competition
    :epkg:`Python 2A ENSAE 2016`.

    @param      fLOG        logging function
    @return                 2 dataframes, one with X, Y, the others one with only X

    The competition is over. The password is ``xdameratxdamerat``.
    """
    if password == "dummy":
        return [random.random() for i in range(7500)]
    else:
        name = os.path.join(os.path.dirname(__file__),
                            "data_competition", "answers.bin")
        if not os.path.exists(name):
            raise FileNotFoundError(name)
        with open(name, "rb") as f:
            c = f.read()
        if password is None:
            raise ValueError("password cannot be None.")
        if not isinstance(password, bytes):
            password = bytes(password, "ascii")
        res = decrypt_stream(password, c)
        g = res.decode("ascii").replace("\r", "")
        s = g.split("\n")
        return [int(_) for _ in s if _]
