import os
import sys
import pandas as pd


def retrieve_fuzcav_vector(fuzcav_file):
    """
    Retrieve the fuzcav vector from the fuzcav file
    :param fuzcav_file: the fuzcav file
    :return: the fuzcav vector
    """
    fuzcav_vector = []
    with open(fuzcav_file, 'r') as f:
        lines = f.readlines()


    fuzcav_vector = [get_vector(line)[1] for line in lines]
    labels = [get_vector(line)[0] for line in lines]
    return labels, fuzcav_vector


def get_vector(line):
    """
    Get the fuzcav vector from the line
    :param line: the line
    :return: the fuzcav vector
    """
    line = line.split(" ")
    label = line[0]
    vector = line[2].strip("\n")
    vector = vector.split(";")
    fuzcav_vector = [float(x) for x in vector]
    return label, fuzcav_vector

def read_zernike(folder):
    arr = []
    labels = []
    for file in os.listdir(folder):
        if file.endswith(".inv"):
            with open(folder + "/" + file, "r") as f:
                file_lines = f.readlines()
                f.close()
            vector = file_lines[1:]
            vector = [line.strip("\n") for line in vector]
            arr.append(vector)
            labels.append(file)
    labels = [lab[0:4] for lab in labels]
    return labels, arr


def read_tm_align(file):
    arr = []
    labels = []
    with open(file, "r") as f:
        lines = f.readlines()
        f.close()

    labels = lines[0].split()
    labels = [lab[0:4] for lab in labels]
    lines = lines[1:]
    lines = [line.split() for line in lines]
    lines = [row[1:] for row in lines]
    return labels, lines