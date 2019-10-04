import sys
import os
import pandas as pd
import statistics as stats


def print_usage():
    print("Usage: python3 average_csv.py <csv file>")


if __name__ == "__main__":

    # check for correct length of arguments
    if len(sys.argv) != 3:
        print_usage()

    # get desired csv file from user input
    infile = sys.argv[1]

    # extract filename from infile and construct outfile with identifying tag
    outfile = infile.split("/")[-1].split(".")[0] + "_avg.csv"

    # get the desired output directory from user arguments
    outdir = sys.argv[2]

    # construct absolute file path for output
    outpath = os.path.join(
        os.path.dirname(os.path.realpath(__file__))
        , os.path.join(outdir, outfile)
    )

    # read file in
    df = pd.read_csv(infile)

    # save the header names
    fields = df.keys()

    # create a dictionary to store the averages
    dct = dict()

    for field in fields:

        # average the column
        fld_avg = stats.mean(list(df[field]))

        # save as a key value pair
        # the average must be saved in a list for pandas
        dct[field] = [fld_avg]

    # convert averages into a data frame
    df = pd.DataFrame(dct)

    # save the file
    df.to_csv(outpath, index=False)
