import os
from subprocess import call

# get all filenames from csv folder
files = os.listdir("csv")

# average each file
for f in files:
    call(["python3", "average_csv.py", "csv/{}".format(f), "csv_avg"])

# concatenate all files in the csv_avg directory
call(["python3", "csv_cat.py", ".*_avg.csv", "csv_avg", "results.csv"])
