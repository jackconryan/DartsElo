# DartsElo
Creating an Elo system for our local Darts matches/tournaments.

The Aim with this project is to creating a functional Elo system similar to one which can be found in games such as chess and Go for Darts.
The product must be easy to use and accessible for non technical users for use in our local darts matches which take place during our tournaments. 

## Download instructions
Run `git clone https://github.com/jackconryan/DartsElo`

Run `npm install` to download dependencies

## Client
Ensure you have R and Python installed.

## Contribute

Special thanks to Daniel Ryan for providing the R code and mathematical expertise.  
His original product can be seen in the ExcelSheet.R file and Coolmoyne Leaderboards.xlsx excel file. 
To date I have refactored his original code, added doubles match functionlaity and changed the data storage from 1 excel file to 3 csv files.

All other files by Jackcon Ryan 
(https://github.com/jackconryan)

Documentation by Jackcon Ryan and Harrison Salzverg 
(https://github.com/Harrison-Salzverg)

See CONTRIBUTING.md for details on how to contribute.

Contributions are made under the [license type] license.  The code of this repository is [license permissions].

The doubles functionality is based on getting an average elo of the two players on each team, performing the elo adjustment calculation based on these averages and applying the elo gain/loss to each player individually.
![image](https://github.com/jackconryan/DartsElo/assets/58440324/0be1f6f5-7578-4118-ad5b-a34a05ec5049)

The excel to CSV change was made in anticipation of a further update to a database system later once a deployment decision has been made.
