import re
import sys
import os
import pandas as pd

"""
Function: get_files
-------------------
get all of the files in the directory
that match the regular expression

regex: regular expression as a string
directory: directory filepath as a string

return: all files matching the regex as a list

"""


def get_files_by_regex(regex: str, directory: str) -> list:
    r = re.compile(regex)
    listdir = os.listdir(directory)
    return list(filter(r.match, listdir))


if __name__ == "__main__":
    # check for correct number of arguments
    if len(sys.argv) != 4:
        print("Usage: csv_cat.py <regex> <directory of csv files> <outfile path>")
        sys.exit(1)

    # user specifies the regular expression, directory of csv files,
    # and the directory to store the result of the concatenation
    out_path = sys.argv[3]
    directory = sys.argv[2]
    regex = sys.argv[1]

    # search for csv files in the specified directory
    csv_files = get_files_by_regex(regex, directory)

    # if no files were returned then exit
    if len(csv_files) == 0:
        print("Error: no files were found at {} with regex {}".format(
            directory,
            regex
        ))

    # create a container to store the dataframes
    dataframes = []

    # loop through the files and load them into the data frame array
    for file in csv_files:
        dataframes.append(pd.read_csv(os.path.join(directory, file)))

    # concatenate all the dataframes into one
    # throws a ValueError if columns or rows don't match
    try:
        out_dataframe = pd.concat(dataframes)
    except ValueError:
        print("Error: one or more CSV files have mismatched columns or rows that are missing values")
        sys.exit(1)

    # save to result file
    # throws a FileNotFoundError if the operating system fails
    # to find a directory in the path
    try:
        out_dataframe.reset_index(drop=True).to_csv(out_path, index=False)
    except FileNotFoundError:
        print("Error: no path {} exists")
        sys.exit(1)
