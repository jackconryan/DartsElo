# DartsElo
Creating an Elo system for our local Darts matches/tournaments.

The Aim with this project is to creating a functional Elo system similar to one which can be found in games such as chess and Go for Darts.
The product must be easy to use and accessible for non technical users for use in our local darts matches which take place during our tournaments. 

Special thanks to Daniel Ryan for providing the R code and mathematical expertise. His original product can be seen in the ExcelSheet.R file and Coolmoyne Leaderboards.xlsx excel file. 

To date I have refactored his original code, added doubles match functionlaity and changed the data storage from 1 excel file to 3 csv files.

The doubles functionality is based on getting an average elo of the two players on each team, performing the elo adjustment calculation based on these averages and applying the elo gain/loss to each player individually
![image](https://github.com/jackconryan/DartsElo/assets/58440324/0be1f6f5-7578-4118-ad5b-a34a05ec5049)

A first throw handicap has been added to the elo calculations by adding an arbitrary amount, currently 10 to the person who threw first.
This added elo ensures causes them to lose slightly more when they lose and gain slightly less when they win.
Many elo systems use numbers ranging from [50-100](https://en.wikipedia.org/wiki/World_Football_Elo_Ratings#:~:text=add%20100%20points%20for%20the%20home%20team) to account for home field advantage however throwing first is not a huge advantage especially for amateurs. 

The excel to CSV change was made in anticipation of a further update to a database system later once a deployment decision has been made.
