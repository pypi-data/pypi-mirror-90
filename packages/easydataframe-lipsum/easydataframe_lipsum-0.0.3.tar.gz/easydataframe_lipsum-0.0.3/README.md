#   Easy Dataframe

##   What is this library?
This library is used when using the xlsx file as pandas.DataFrame.

It is intended for use in small-scale development.

##  What kind of function does it have?

* A function to judge whether it is xlsx or csv from the file path and read it as a data frame(from dataframe_in import read)


* Ability to read a specific cell(from dataframe_helper import read_cell)


* Check if there is NaN or None in the data frame


* ※ Most functions try to treat the elements of the data frame as str(from dataframe_helper import _any_to_str).
##   use
` pip install easydataframe-lipsum`

python3

`>>> import lipsum_easydataframe.dataframe_helper as helper`

`>>> helper.example()`


##  Required library
pandas

##  Required System
Windows10 == useWindows and usePython >= Python3.8