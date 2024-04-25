### About
this script is to break apart a csv from math tournament data into two separate csv
files in preparation for loading the data into a database

If you would like to process different data place the csv, and only that csv in the input
folder. Run the script again and the data will be writen to output.
The script cant accept files that aren't formatted as expected, otherwise it will break.

The program outputs 5 separate CSVs, with institutions, teams, outstanding teams' institutions, 
institutions' number of teams, and usa teams with meritorious ranking or better. 
Average number of teams per institution is printed out in the console.
### Running the script

clone the repo
```shell
git clone https://github.com/cwdatlas/csvMathParser
```
Move into the new repo
```shell
cd csvMathParser
```
run the program
```shell
python main.py
```
