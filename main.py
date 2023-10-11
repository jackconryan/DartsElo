import pandas as pd
import Player as pl

rankings = pd.read_csv('C:/Users/Jack Ryan/Documents/VSProjects/Darts/Coolmoyne Leaderboard Starting Ranks.csv')
#calculates and returns percentage chance that player a beats player b. 
matches = pd.read_csv('C:/Users/Jack Ryan/Documents/VSProjects/Darts/Coolmoyne Leaderboard Matches.csv')

first_throw_advantage=10
max_elo_change=32

##  populate a list of player objects 
def fill_players(list:list):
    for _, row in rankings.iterrows():
        list.append(pl.Player(row['Name'], row['Rating']))
    return list

def print_rankings():
    for player in players:
        print(f"{player.name}:{player.rating}")
def print_current_avg_elo():
    total_elo=0
    i=0
    for player in players:
        total_elo =+ total_elo + player.rating
        i = i+1
    print(f"Total elo in the system is {total_elo}\nAverage elo in the system is {total_elo/i}" )
##  calculate the percentage chance player_a should win a match against an oppenent player_b
##  return percentage chance
def predicted_win_percentage(player_a_rating, player_b_rating):
    win_percent = 1/(1+10**((player_b_rating - player_a_rating)/400)) 
    return win_percent

##  calculate the rating change for eacg player after winning a match 
##  return each players new elo
def new_rating(winner, loser):
    winner_change = (winner+max_elo_change*(1-predicted_win_percentage(winner, loser))-winner)
    loser_change =  (loser+max_elo_change*(0-predicted_win_percentage(loser, winner))-loser)
    return winner_change, loser_change

##  calculate the new elo based on the previous matches in the system
def calc_prev_match_data():
    for _, match in matches.iterrows():
        winner_name = match['Winner']
        loser_name = match['Loser']
        threw_first = match['Threw First']
        winner, loser = None,None   #redeclare each loop to prevent entirely empty row in csv from creating an error
        for player in players:
            if winner_name == player.name:
                winner = player
                continue
            if loser_name == player.name:
                loser = player
                continue
        if(winner.name ==  threw_first):
            match_result(winner, loser, True)
        elif(loser.name == threw_first):
            match_result(winner, loser, False)
        else:
            print(f"Error matching a players name with Threw First as entered in csv {winner.name}, {loser.name}, {threw_first}")

##  calculate match result based on players name only
##  this means we must look up player in list of players and is 
##  more resource intensive 
##  should always use match_result() instead in application
##  DEPRECATED
def match_result_name(winner_name, loser_name, threw_first_name):
    for player in players:
            if winner_name == player.name:
                winner = player
                continue
            if loser_name == player.name:
                loser = player
                continue
    if(winner.name ==  threw_first_name):
        match_result(winner, loser, True)
    elif(loser.name == threw_first_name):
        match_result(winner, loser, False)
    else:
        print("Error matching a players name with Threw First name")

##  match result function. takes two players objects player a is the winner and b is the loser
##  adjust the ratings of the player who threw first by 50 elo points to account for the advatage throwing first gives a player
##  ratings must be calculated and updated

def match_result(player_a: pl.Player, player_b: pl.Player, winner_threw_first:bool):
    if winner_threw_first:
        player_a_change, player_b_change = new_rating(player_a.rating+first_throw_advantage, player_b.rating)      # add 10 elo points for first throw advatage
        player_a.update_rating(player_a.rating+player_a_change)
        player_b.update_rating(player_b.rating+player_b_change)
    else:
        player_a_change, player_b_change = new_rating(player_a.rating, player_b.rating+first_throw_advantage)      # add 10 elo points for first throw advatage
        player_a.update_rating(player_a.rating+player_a_change)
        player_b.update_rating(player_b.rating+player_b_change)

##  update both players elo after completing a doubles match 
##  takes 4 player obj, averages their elo then does the usual calculation
def doubles_match_results(player_a:pl.Player, player_b: pl.Player, player_c:pl.Player, player_d: pl.Player, threw_first_name):
    winner_avg_elo = (player_a.rating + player_b.rating)/2
    loser_avg_elo = (player_c.rating + player_d.rating)/2
    
    if  threw_first_name==player_a.name or threw_first_name==player_b.name:         ##check if winning team threw first
        print(f"Team {player_a.name} and {player_b.name} won their doubles game. Team {player_c.name} and {player_d.name} Lost. {threw_first_name} threw first")
        winner_change, loser_change = new_rating(winner_avg_elo+first_throw_advantage, loser_avg_elo)      ##add 10 elo to threw first team for calculation
    elif threw_first_name == player_c.name or threw_first_name==player_d.name :
        print(f"Team {player_a.name} and {player_b.name} won their doubles game. Team {player_c.name} and {player_d.name} Lost. {threw_first_name} threw first")
        winner_change, loser_change = new_rating(winner_avg_elo, loser_avg_elo+first_throw_advantage)      ##add 10 elo to threw first team for calculation
    else:
        print("Doubles match issue: couldnt find player name in list of players")

    print(f"After their doubles game {player_a.name} and {player_b.name} gained {winner_change} elo points")
    player_a.update_rating(player_a.rating + winner_change),player_b.update_rating(player_b.rating + winner_change)
    player_c.update_rating(player_c.rating + loser_change),player_d.update_rating(player_d.rating + loser_change)

def update_rank_csv():
    player_data = [{'Name': player.name, 'Rating': player.rating} for player in players]
    player_df = pd.DataFrame(player_data)
    player_df.to_csv('C:/Users/Jack Ryan/Documents/VSProjects/Darts/Coolmoyne Leaderboard Updated Rank.csv')
players = []
##  fill players from excel sheet
fill_players(players)

##  calculate elo based on matches stored
# calc_prev_match_data()
print("After calculating the historical matches the current standings are")
print_rankings()

##  test doubles match winner threw first
doubles_match_results(players[3], players[4], players[0], players[1], players[3].name)
##  test doubles match loser threw first 
doubles_match_results(players[3], players[0], players[2], players[1], players[1].name)

##  print rankings after doubles match
print_rankings()
print_current_avg_elo()

update_rank_csv()