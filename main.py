import pandas as pd
import Player as pl

rankings = pd.read_csv('C:/Users/Jack Ryan/Documents/VSProjects/Darts/Coolmoyne Leaderboard Starting Ranks.csv')
#calculates and returns percentage chance that player a beats player b. 
matches = pd.read_csv('C:/Users/Jack Ryan/Documents/VSProjects/Darts/Coolmoyne Leaderboard Matches.csv')

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
# ratings must be calculated and updated  
def match_result(player_a: pl.Player, player_b: pl.Player):
    player_a_update, player_b_update = new_rating(player_a.rating, player_b.rating)
    player_a.update_rating(player_a_update)
    player_b.update_rating(player_b_update)

##  update both players elo after completing a doubles match 
##  takes 4 player obj, averages their elo then does the usual calculation
def doubles_match_results(player_a:pl.Player, player_b: pl.Player, player_c:pl.Player, player_d: pl.Player):
    winner_avg_elo = (player_a.rating + player_b.rating)/2
    loser_avg_elo = (player_c.rating + player_d.rating)/2
    winner_update, loser_update = new_rating(winner_avg_elo, loser_avg_elo)
    winner_diff = winner_update - winner_avg_elo
    loser_diff = loser_update - loser_avg_elo
    
    print(f"After their doubles game {player_a.name} and {player_b.name} gained {winner_diff} elo points")
    player_a.update_rating(player_a.rating + winner_diff),player_b.update_rating(player_b.rating + winner_diff)
    player_c.update_rating(player_c.rating + loser_diff),player_d.update_rating(player_d.rating + loser_diff)

def update_csv():
    player_data = [{'Name': player.name, 'Rating': player.rating} for player in players]
    player_df = pd.DataFrame(player_data)
    player_df.to_csv('C:/Users/Jack Ryan/Documents/VSProjects/Darts/Coolmoyne Leaderboard Updated Rank.csv')
players = []
##  fill players from excel sheet
fill_players(players)

##  calculate elo based on matches in excel sheet
calc_prev_match_data()

##  print rankings
print("After calculating the historical matches the current standings are")
for player in players:
    print(f"{player.name}:{player.rating}")

# test doubles match
doubles_match_results(players[3], players[4], players[0], players[1])

##  print rankings after doubles match
for player in players:
    print(f"{player.name}:{player.rating}")

update_csv()