import pandas as pd
import Player as pl

rankings = pd.read_csv('C:/Users/Jack Ryan/Documents/VSProjects/Darts/Coolmoyne Leaderboard Starting Ranks.csv')
#calculates and returns percentage chance that player a beats player b. 
matches = pd.read_csv('C:/Users/Jack Ryan/Documents/VSProjects/Darts/Coolmoyne Leaderboard Matches.csv')

first_throw_advantage=10
max_elo_change=32

def fill_players(player_list):
    """
    Populates a list of player objects based on the existing rankings data.

    Args: 
        player_list (list): An empty list to store player onjects.

    Returns:
        list: a list of player object initialized with names and strings.
    """
    for _, row in rankings.iterrows():
        player_list.append(pl.Player(row['Name'], row['Rating']))
    return player_list

def print_rankings():
    """
    Prints the names and rankings of every player in the system.
    """
    for player in players:
        print(f"{player.name}:{player.rating}")

def print_current_avg_elo():
    """
    Calculates and prints the total and average Elo rating of all players in the system.
    """
    total_elo=0
    i=0
    for player in players:
        total_elo =+ total_elo + player.rating
        i = i+1
    print(f"Total elo in the system is {total_elo}\nAverage elo in the system is {total_elo/i}" )

def predicted_win_percentage(player_a_rating, player_b_rating):
    """
    Calculate the percentage chance that player_a should win a match against player_b

    Args: 
        player_a_rating (int): The Elo rating of player_a.
        player_b_rating (int): The Elo rating of player_b.

    Returns:
        float: The percentage chance that player_a wins the amtch.
    """
    win_percent = 1/(1+10**((player_b_rating - player_a_rating)/400)) 
    return win_percent

def new_rating(winner, loser):
    """
    Calculate the new Elo ratings for each player after a match 

    Args: 
        winner(int): The value the winners elo should be changed by 
        loser(int):the value the losers elo should be changed by

    Returns:
        tuple: A tuple containing the change in Elo ratings for the winner and loser.
    """
    winner_change = (winner+max_elo_change*(1-predicted_win_percentage(winner, loser))-winner)
    loser_change =  (loser+max_elo_change*(0-predicted_win_percentage(loser, winner))-loser)
    return winner_change, loser_change

def calc_prev_match_data():
    """
    Calculate new elo ratings based on previous match data stored in the system

    Iterates through the data stored in 'matches' and calculates the new elo ratings for each player in the match 
    based on the results. 

    Raises: 
        ValueError: if the 'Threw First' field in the csv does not match any player's name.

    """
    for _, match in matches.iterrows():
        winner_name = match['Winner']
        loser_name = match['Loser']
        threw_first = match['Threw First']
        winner, loser = None,None #redeclare each loop to prevent entirely empty row in csv from creating an error
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
            raise ValueError(f"Error matching a player's name with 'Threw First' as entered in the CSV: {winner.name}, {loser.name}, {threw_first}")

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

def match_result(player_a: pl.Player, player_b: pl.Player, winner_threw_first:bool):
    """
    Update Elo ratings of the two players invovled in a match based on the result. Player A is the winner

    Args:
        player_a (pl.Player): The winning player.
        player_b (pl.Plauer): The losing player.
        winner_threw_first (bool): Indicates whether the winner threw first in the match

    Note:
        Player A must be the winner of the match.
        Before the calculation is carried out an additional 10 elo points are given to the 
        player who threw first to account for the advantage.

    Example:
        If player A defeated player B, and player A threw the first dart, you should call this function as
        match_result(player_a, player_b, True)
        If player B threw first it should be called as
        match_result(player_a, player_b, False)
    """
    if winner_threw_first:
        player_a_change, player_b_change = new_rating(player_a.rating+first_throw_advantage, player_b.rating)      # add 10 elo points for first throw advatage
        player_a.update_rating(player_a.rating+player_a_change)
        player_b.update_rating(player_b.rating+player_b_change)
    else:
        player_a_change, player_b_change = new_rating(player_a.rating, player_b.rating+first_throw_advantage)      # add 10 elo points for first throw advatage
        player_a.update_rating(player_a.rating+player_a_change)
        player_b.update_rating(player_b.rating+player_b_change)

def doubles_match_results(player_a:pl.Player, player_b: pl.Player, player_c:pl.Player, player_d: pl.Player, threw_first_name):
    """
    Update 4 players Elos after a doubles match. player A and B are the winners player C and D are the losers.

    Args:
        player_a (pl.Player): first player from the winning team.
        player_b (pl.Player): second player from the winning team.
        player_c (pl.Player): first player from the losing team.
        player_d (pl.Player): second player from the losing team.
        threw_first_name (str): The name of the player who threw the first dart in the match.

    Note:
        The Elo ratings are averaged between the two players on both teams in order to calculate the loss and gain 
        Player a and player b should always be the winner.
        Threw first advantage is included in the calculation.
    """
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
    """
    Update and export the player rankings to a CSV file.

    This function creates a DataFrame containing the current player rankings, and the exports it to a CSV file.

    Note:
        This function should be called at the end of the program to store the new ratings
    """
    player_data = [{'Name': player.name, 'Rating': player.rating} for player in players]
    player_df = pd.DataFrame(player_data)
    player_df.to_csv('C:/Users/Jack Ryan/Documents/VSProjects/Darts/Coolmoyne Leaderboard Updated Rank.csv')

players = []
##  fill players from excel sheet
fill_players(players)

##  calculate elo based on matches stored
calc_prev_match_data()
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