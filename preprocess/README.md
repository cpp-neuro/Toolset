Usage Instructions

::: Prerequisites :::

- All files being processed need to go in the csv folder
- All csv files in the csv folder must follow the following format
		
		field1 field2 field3 ...
		x11    x12    x13
    x21    x22    x23

- All column names in all files must match

::: Dependencies :::
Python files were written to be operating system agnostic 
** Let me know if this is not the case **

A requirements.txt file has been include
Install dependencies with the following command
pip3 install -r requirements.txt

::: Usage :::
"pyton3 average_and_combine.py"


::: Results :::
- All averaged files will be placed in csv_avg
- All averaged files will be of the form

    field1   field2   field3 ...
    avf(x1)  avg(x2)  avg(x3) ...

- Final result will be stored in "results.csv"
- All averaged files will be combined into one csv file
  with the common column names
