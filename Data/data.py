import csv
import os


def reset():
    """
    Reset defaults
    :return: None
    """
    with open(os.path.join("Data", "data.csv"), "w", newline="") as file:
        file.write("0,1")


def get():
    """
    Get data from data.csv
    :return: Dictionary 'data' of the data
    :rtype: dict
    """
    data = {}
    with open(os.path.join("Data", "data.csv"), "r") as file:
        reader = csv.reader(file)
        for line in reader:
            data["highscore"] = line[0]
            data["bird"] = line[1]
    return data


def edit(hs, bird):
    """
    Edit data.csv
    :param hs: New highscore
    :param bird: New default 'bird'
    :return: None
    """
    with open(os.path.join("Data", "data.csv"), "w", newline="") as file:
        file.write(f"{hs},{bird}")
