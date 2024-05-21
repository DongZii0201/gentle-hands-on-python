import sys

import matplotlib.pyplot as plt
from datetime import datetime
import csv


def average_observation(observations):
    temp_sum = 0
    for observation in observations:
        temp_sum = temp_sum + observation["Temperature"]

    return {
        "Temperature": temp_sum / len(observations),
        "Time": observations[len(observations) // 2]["Time"],
    }


def moving_window(data, window_size: int):
    windows = []
    for window_begin in range(len(data) - window_size + 1):
        windows = windows + [data[window_begin : (window_begin + window_size)]]

    return windows


def smoothed(data, window_size: int):
    smooth = []
    windows = moving_window(data, window_size)
    for window in windows:
        smooth = smooth + [average_observation(window)]

    return smooth


def split_data(data):
    temps = []
    dates = []
    for observation in data:
        temps = temps + [observation["Temperature"]]
        dates = dates + [observation["Time"]]

    return {"Temperatures": temps, "Dates": dates}


def plot_global_data(data: list[dict[str, float | datetime]]) -> None:
    original = split_data(data)
    smooth = split_data(smoothed(data, 84))

    plt.plot(original["Dates"], original["Temperatures"], color="lightblue")
    plt.plot(smooth["Dates"], smooth["Temperatures"], color="darkblue")
    plt.xlabel("Time")
    plt.ylabel("Temperature anomaly")
    plt.title("Global climate anomaly relative to 1960-1991 reference")
    plt.savefig("output.png")


if __name__ == "__main__":
    with open(sys.argv[1]) as f:
        reader = csv.DictReader(f)
        data = []
        for reading in reader:
            data = data + [
                {
                    "Time": datetime.fromisoformat(reading["Time"]),
                    "Temperature": float(reading["Temperature"]),
                }
            ]

    plot_global_data(data)
