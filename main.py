import pandas as pd
import Player as pl

file_path = 'C:/Users/Jack Ryan/Documents/VSProjects/Darts/Coolmoyne Leaderboards.xlsx'
rankings = pd.read_excel(file_path, sheet_name="Starting Rank")
#calculates and returns percentage chance that player a beats player b. 
matches = pd.read_excel(file_path, sheet_name="Matches")

##  populate a list of player objects 
def fill_players(list:list):
    for index, row in rankings.iterrows():
        list.append(pl.Player(row['Name'], row['Rating']))
    return list

##  calculate the percentage chance player_a should win a match against an oppenent player_b
##  return percentage chance
def predicted_win_percentage(player_a_rating, player_b_rating):
    win_percent = 1/(1+10**((player_b_rating - player_a_rating)/400)) 
    return win_percent

##  calculate the rating change for eacg player after winning a match 
##  return each players new elo
def new_rating(winner, loser):
    winner_new_rating = winner+32*(1-predicted_win_percentage(winner, loser))
    loser_new_rating =  loser+32*(0-predicted_win_percentage(loser, winner))
    return winner_new_rating, loser_new_rating

##  calculate the new elo based on the previous matches in the system
def calc_prev_match_data():
    for _, match in matches.iterrows():
        winner_name = match['Winner']
        loser_name = match['Loser']
        
        for player in players:
            if winner_name == player.name:
                winner = player
                continue
            if loser_name == player.name:
                loser = player
                continue
        match_result(winner, loser)

##  calculate match result based on players name only
##  this means we must look up player in list of players and is 
##  more resource intensive 
##  should always use match_result() instead in application
def match_result_name(winner_name, loser_name):
    for player in players:
            if winner_name == player.name:
                winner = player
                continue
            if loser_name == player.name:
                loser = player
                continue
    match_result(winner, loser)

##  match result function. takes two players objects player a is the winner and b is the loser
##  ratings must be calculated and updated  
def match_result(player_a: pl.Player, player_b: pl.Player):
    player_a_update, player_b_update = new_rating(player_a.rating, player_b.rating)
    player_a.update_rating(player_a_update)
    player_b.update_rating(player_b_update)


players = []
##  fill players from excel sheet
fill_players(players)

##  calculate elo based on matches in excel sheet
calc_prev_match_data()

##  print rankings
for player in players:
    print(f"{player.name}:{player.rating}\n")


##  print rankings

for player in players:
    print(f"{player.name}:{player.rating}\n")