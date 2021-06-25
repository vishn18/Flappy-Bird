try:
    from colorama import Fore
except ModuleNotFoundError:
    print("Couldn't import colorama!")
import csv


def get_data():
    data = {}
    with open("data.csv", "r") as file:
        reader = csv.reader(file)
        for line in reader:
            data["highscore"] = line[0]
            data["defaultbird"] = line[1]
    return data


def reset():
    with open("data.csv", "w", newline="") as file:
        file.write("0,1")


with open("data.csv", "r") as file:
    if file.read() == "":
        print("Data file is empty!")
        print("Resetting data...")
        reset()
        print("\rResetting data... -done!")

print(get_data())
