import csv
import json
import sys
import pandas as pd
from inc.datastructures import WorkbenchData


"""
    File for building EEGWorkbench json files from 
    EEG data stored in CSV files
    
    Usage: lg-json_builder.py +<option> file1 file2 file3... +<option> file1 file2 file3...
    
    Options:
    +meta               : Add metadata file
    +raw_eeg            : Add raw EEG file
    +source_tf          : Add source time-frequency file
    +target_tf          : Add target time-frequency file
    +cross_tf           : Add source and target time-frequency file iff user specifies both files
    +classifier_data    : Add classification data file
    +classifier_results : Add classification results file
"""


def read_csv(csvfilename):
    """
    Parse a CSV file and return a dictionary of the data
    :param csvfilename: The path to the csvfile
    :return: Dictionary containing the CSV data
    """

    # read CSV into a pandas dataframe
    df = pd.read_csv(csvfilename)

    # convert the dataframe to a dictionary
    data = df.to_dict('list')

    return data


def add_source_tf(filenames, workbenchdata):
    workbenchdata.source_tf = dict()

    for i in range(len(filenames)):
        trial_tag = "trial {}".format(i + 1)
        data = read_csv(filenames[i])
        workbenchdata.source_tf[trial_tag] = data

    return workbenchdata


def add_target_tf(filenames, workbenchdata):
    workbenchdata.target_tf = dict()

    for i in range(len(filenames)):
        trial_tag = "trial {}".format(i + 1)
        data = read_csv(filenames[i])
        workbenchdata.target_tf[trial_tag] = data

    return workbenchdata

def add_cross_tf(filenames, workbenchdata):
    # Luis' JSON format expects 1 raw EEG file per query
    if len(filenames) != 2:
        print(
            "Could not add raw EEG file: {} files were provided but expected 2".format(
                len(filenames)
            )
        )
        return workbenchdata

    workbenchdata.cross_tf = dict()

    for i in range(len(filenames)):
        trial_tag = "trial {}".format(i + 1)
        data = read_csv(filenames[i])
        workbenchdata.cross_tf[trial_tag] = data

    return workbenchdata


def add_raw_eeg(filenames, workbenchdata):
    # Luis' JSON format expects 1 raw EEG file per query
    if len(filenames) != 1:
        print(
            "Could not add raw EEG file: {} files were provided but expected 1".format(
                len(filenames)
            )
        )
        return workbenchdata

    # extract teh filename from the argument list
    filename = filenames[0]

    # read in the specified CSV file
    raw_eeg = read_csv(filename)

    # add raw EEG to the WorkbenchData container
    workbenchdata.raw_eeg_data = raw_eeg

    return workbenchdata


def add_metadata(filenames, workbenchdata):
    """
    Add the metadata contained in a file to the workbenchdata
    :param filenames: A list of filenames
    :param workbenchdata: A WorkbenchData object
    :return: The WorkbenchData object with the metadata from the file
    """
    # Luis' JSON format supports metadata for 1 reading
    if len(filenames) != 1:
        print(
            "Could not add metadata file: {} files were provided but expected 1".format(
                len(filenames)
            )
        )
        return workbenchdata

    # extract the filename from the provided arguments
    filename = filenames[0]

    # container to hold extracted metadata
    metadata = dict()

    # extract the metadata as key value pairs
    with open(filename, 'r') as mdf:
        for line in mdf:
            key = line.split(":")[0].strip()
            value = line.replace("{}:".format(key), "").strip()
            metadata[key] = value

    # place the extracted data in the data container
    workbenchdata.set_name = metadata["title"]
    workbenchdata.record_timestamp = metadata["timestamp started"]
    workbenchdata.sample_rate = metadata["sampling"]
    workbenchdata.device_id = metadata["units"]

    return workbenchdata
            
def group_tasks(args):
    """
    Takes arguments from the command line and groups them based on the +
    symbol
    :param args: The list of command line arguments
    :return: A dictionary where each option marked with the +
        symbol serves as the key and the value consists of the
        arguments following the keyword
    """
    # join the arguments into a single string
    arg_str = " ".join(args)

    # each argument that starts with a + specifies
    # a new argument group
    task_list = arg_str.split("+")

    # load the argument groups into a dictionary
    # for quick access
    # example: the option "+source_tf file1.csv file2.csv"
    #   will appear as {"source_tf" : ["file1.csv", "file2.csv"]}
    tasks = dict()
    for task in task_list[1:]:
        task = task.strip()
        task = task.split(" ")
        tasks[task[0]] = task[1:]

    return tasks


if __name__ == "__main__":

    # extract and group tasks
    tasks = group_tasks(sys.argv[1:])

    # create workbench data object
    wbd = WorkbenchData()

    # add data to workbench data object based on command line input
    for task in tasks.keys():
        if task == "meta":
            workbenchdata = add_metadata(tasks[task], wbd)
        elif task == "raw_eeg":
            workbenchdata = add_raw_eeg(tasks[task], wbd)
        elif task == "source_tf":
            workbenchdata = add_source_tf(tasks[task], wbd)
        elif task == "target_tf":
            workbenchdata = add_target_tf(tasks[task], wbd)
        elif task == "cross_tf":
            workbenchdata = add_cross_tf(tasks[task], wbd)
        else:
            print("Error: No {} option".format())

    wbd.export_json()
