# -*- coding: utf-8 -*-
"""
Created on Mon Apr 24 19:54:03 2023

@author: Dillan
"""

###########################################################

#Computer Project 8
#Algorithm
#1. Prompt user for input file containing games and discount data
#2. Read and process the games and discount files
#3. Display a menu of options to the user
#4. Execute the selected option and display the results
#5. Repeat steps 3-4 until the user chooses to exit
#6. Display a closing message
###########################################################
import csv
from operator import itemgetter


MENU = '''\nSelect from the option: 
        1.Games in a certain year 
        2. Games by a Developer 
        3. Games of a Genre 
        4. Games by a developer in a year 
        5. Games of a Genre with no discount 
        6. Games by a developer with discount 
        7. Exit 
        Option: '''
        
      
        
def open_file(s: str):
    """
    This function prompts the user to input a csv file name to open and keeps prompting until a correct name is entered.
    The parameter s is a string to incorporate into your prompt so you are prompting the user for a particular type of file.
    
    Parameters:
    s (str): A string to incorporate into the prompt.
    
    Returns:
    fp: A file pointer to the opened file.
    """

    while True:
        try:
            file_name = input(f"\nEnter {s} file: ")
            fp = open(file_name, encoding='UTF-8')# Constants for file reading
            return fp
        except FileNotFoundError:
            print("\nNo Such file")

def read_file(fp_games):
    games_data = {}
    reader = csv.reader(fp_games)
    
    next(reader)  # Skip the header line

    for row in reader:
        name = row[0]
        release_date = row[1]
        developer = row[2].split(';')
        genres = row[3].split(';')
        player_modes = row[4].split(';')
        mode = 0 if player_modes[0].lower() == 'multi-player' else 1

        try:
            price = float(row[5].replace(',', '')) * 0.012
        except ValueError:
            price = 0.0
        
        overall_reviews = row[6]
        reviews = int(row[7])
        percent_positive = int(row[8].strip('%'))

        support_list = []
        if row[9] == '1':
            support_list.append('win_support') # Constants for platform support
        if row[10] == '1':
            support_list.append('mac_support') # Constants for platform support
        if row[11] == '1':
            support_list.append('lin_support') # Constants for platform support

        games_data[name] = [release_date, developer, genres, mode, price, overall_reviews, reviews, percent_positive, support_list]

    return games_data

def read_discount(fp_discount):
    """
    This function reads the discount file and creates a dictionary with key as the name of the game
    and value as the discount as a float rounded to 2 decimals. Remember to skip the header line.

    Parameters:
    fp_discount: A file pointer to the discount file.

    Returns:
    discounts: A dictionary with game name as the key and discount as the value (float rounded to 2 decimals).
    """
    
    discounts = {}
    reader = csv.reader(fp_discount)
    
    is_header = True

    for row in reader:
        if is_header:
            is_header = False
            continue

        game_name = row[0]
        discount = round(float(row[1]), 2)
        discounts[game_name] = discount

    return discounts



def in_year(master_D, year: int):
    """
    This function filters out games that were released in a specific year from the main dictionary
    created in the read_file function (master_D).

    Parameters:
    master_D (dict): The main dictionary containing games data.
    year (int): The year to filter games by.

    Returns:
    sorted_games (list): A sorted list of game names released in the specified year.
    """
    
    games_in_year = []

    for game, data in master_D.items():
        release_date = data[0]
        release_year = int(release_date.split('/')[-1])

        if release_year == year:
            games_in_year.append(game)

    sorted_games = sorted(games_in_year)
    return sorted_games


def by_genre(master_D, genre: str):
    """
    This function filters out games that are of a specific genre from the main dictionary
    created in the read_file function (master_D). It creates a list of game names sorted
    by percentage positive reviews in descending order.

    Parameters:
    master_D (dict): The main dictionary containing games data.
    genre (str): The genre to filter games by.

    Returns:
    sorted_games (list): A sorted list of game names based on percentage positive reviews in descending order.
    """

    def sort_key(game_tuple):
        return game_tuple[1]

    games_in_genre = []

    for game, data in master_D.items():
        genres = data[2]
        percent_positive = data[7]

        if genre in genres:
            games_in_genre.append((game, percent_positive))

    # Sort the games by percentage positive reviews in descending order
    sorted_games = [game for game, _ in sorted(games_in_genre, key=sort_key, reverse=True)]
    return sorted_games

        
def by_dev(master_D, developer: str):
    """
    This function filters out games that are made by a specific developer from the main dictionary
    created in the read_file function (master_D). It creates a list of game names sorted from
    latest to oldest released games.

    Parameters:
    master_D (dict): The main dictionary containing games data.
    developer (str): The developer to filter games by.

    Returns:
    sorted_games (list): A sorted list of game names based on release date from latest to oldest.
    """

    def sort_key(game_tuple):
        release_date = game_tuple[1].split('/')
        return int(release_date[2])

    games_by_developer = []

    for game, data in master_D.items():
        devs = data[1]
        release_date = data[0]

        if developer in devs:
            games_by_developer.append((game, release_date))

    # Sort the games by release year in descending order
    sorted_games = [game for game, _ in sorted(games_by_developer, key=sort_key, reverse=True)]
    return sorted_games


def per_discount(master_D, games, discount_D):
    """
    This function calculates and returns a list of the discounted price for each game in the list of games.

    Parameters:
    master_D (dict): The main dictionary containing games data.
    games (list): A list of games to calculate the discounted price for.
    discount_D (dict): The discount dictionary containing the discount percentages for games.

    Returns:
    discounted_prices (list): A list of discounted prices for each game in the games list.
    """

    discounted_prices = []

    for game in games:
        original_price = master_D[game][4]
        discount_percentage = discount_D.get(game, 0)
        discounted_price = original_price * (1 - discount_percentage / 100)
        discounted_prices.append(round(discounted_price, 6))

    return discounted_prices


def by_dev_year(master_D, discount_D, developer, year):
    """
    This function filters out games by a specific developer and released in a specific year.
    It returns a list of game names sorted in increasing prices. If there is a tie, it should be sorted by the game name.

    Parameters:
    master_D (dict): The main dictionary containing games data.
    discount_D (dict): The discount dictionary containing the discount percentages for games.
    developer (str): The developer to filter games by.
    year (int): The year to filter games by.

    Returns:
    sorted_games (list): A list of game names sorted in increasing prices.
    """

    def sort_key(game_data):
        return game_data[1], game_data[0]

    filtered_games = []

    for game, data in master_D.items():
        release_date = data[0]
        game_developer = data[1]
        release_year = int(release_date.split('/')[-1])

        if developer in game_developer and release_year == year:
            original_price = data[4]
            discount_percentage = discount_D.get(game, 0)
            discounted_price = original_price * (1 - discount_percentage / 100)
            filtered_games.append((game, discounted_price))

    sorted_games = sorted(filtered_games, key=sort_key)
    return [game[0] for game in sorted_games]

          
def by_genre_no_disc(master_D, discount_D, genre):
    """
    This function filters out games by a specific genre that do not offer a discount on their price.
    It returns a list of game names sorted from cheapest to most expensive. If there is a tie,
    it should be sorted by the percentage positive reviews in descending order.

    Parameters:
    master_D (dict): The main dictionary containing games data.
    discount_D (dict): The discount dictionary containing the discount percentages for games.
    genre (str): The genre to filter games by.

    Returns:
    sorted_games (list): A list of game names sorted from cheapest to most expensive.
    """

    def sort_key(game_data):
        return game_data[1], -game_data[2]

    filtered_games = []

    for game, data in master_D.items():
        game_genres = data[2]
        price = data[4]
        percent_positive = data[7]

        if genre in game_genres and game not in discount_D:
            filtered_games.append((game, price, percent_positive))

    sorted_games = sorted(filtered_games, key=sort_key)
    return [game[0] for game in sorted_games]


def by_dev_with_disc(master_D, discount_D, developer):
    """
    This function filters the games developed by a specific developer and currently on discount. It first retrieves
    all the games by the developer using the 'by_dev' function, then checks if the game is in the discount dictionary.
    The filtered games are sorted by their original price and release date in descending order.

    Parameters:
    master_D (dict): The master dictionary containing game data.
    discount_D (dict): The discount dictionary containing games on discount.
    developer (str): The name of the developer to filter games by.

    Returns:
    list: A list of filtered game names sorted by original price and release date in descending order.
    """
    dev_games = by_dev(master_D, developer)
    filtered_games = []

    for game in dev_games:
        if game in discount_D:
            data = master_D[game]
            release_date = data[0]
            original_price = data[4]
            filtered_games.append((game, release_date, original_price))

    def sort_key(game_tuple):
        original_price = game_tuple[2]
        release_date = game_tuple[1].split('/')
        return (original_price, -int(release_date[2]))

    filtered_games.sort(key=sort_key)

    return [game[0] for game in filtered_games]
             
def main():
    file_pointer = open_file("games")
    master_D = read_file(file_pointer)
    file_pointer.close()
    
    file_pointer = open_file("discount")
    discount_D = read_discount(file_pointer)
    file_pointer.close()

    while True:
        print(MENU)
        is_valid = False
        while not is_valid:
            try:
                option = int(input())
                is_valid = True
            except ValueError:
                print("Please enter a valid number.")

        if option == 1:
            year = input("Which year: \n")
            while not year.isdigit():
                print("Please enter a valid year")
                print()
                year = input("Which year: \n")
            games = in_year(master_D, int(year))
            if games:
                print(f"Games released in {year}:")
                print(", ".join(games))
            else:
                print("Nothing to print")
                
        elif option == 2:
            developer = input("Which developer: \n")
            games = by_dev(master_D, developer)
            if games:
                print(f"Games made by {developer}:")
                print(", ".join(games))
            else:
                print("Nothing to print")
            
        elif option == 3:
            genre = input("Which genre: \n")
            games = by_genre(master_D, genre)
            if games:
                print(f"Games with {genre} genre:")
                print(", ".join(games))
            else:
                print("Nothing to print")

            
        elif option == 4:
            developer = input("Which developer: \n")
            year = input("Which year: \n")
            if not year.isdigit():
                print("Invalid year. Please enter a valid integer.")
            else:
                year = int(year)
                games = by_dev_year(master_D, discount_D, developer, year)
                if games:
                    print(f"Games made by {developer} and released in {year}:")
                    print(", ".join(games))
                else:
                    print("Nothing to print")
                
        elif option == 5:
            genre = input("Which genre: \n")
            games = by_genre_no_disc(master_D, discount_D, genre)
            if games:
                print(f"Games with {genre} genre and without a discount:")
                print(", ".join(games))
            else:
                print("Nothing to print")
            
        elif option == 6:
            developer = input("Which developer: \n")
            games = by_dev_with_disc(master_D, discount_D, developer)
            if games:
                print(f"Games made by {developer} which offer discount:")
                print(", ".join(games))
            else:
                print("Nothing to print")
            
        elif option == 7:
            print("Thank you.")
            break
            
        else:
            print("Invalid option")

if __name__ == "__main__":
    main()