import csv
import os


def reset():
    with open(os.path.join("Data", "data.csv"), "w", newline="") as file:
        file.write("0,1")


def get():
    data = {}
    with open(os.path.join("Data", "data.csv"), "r") as file:
        reader = csv.reader(file)
        for line in reader:
            data["highscore"] = line[0]
            data["bird"] = line[1]
    return data


def edit(hs, bird):
    with open(os.path.join("Data", "data.csv"), "w", newline="") as file:
        file.write(f"{hs},{bird}")
