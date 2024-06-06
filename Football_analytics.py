import requests
import pprint

base_url = 'http://api.football-data.org/v4/'
params = {'status': 'FINISHED', 'limit': 1}
headers = {'X-Auth-Token': '30bdeb1d93b348a284251780e6771fbb'}

leagues = {'pl': 'Premier League', 'bl' : 'Bundesliga', 'sa':'Serie A',  'fl1':'Ligue One','pd' : 'La Liga'}

def get_standings(league):
    standings_data = requests.get(base_url + f"competitions/{league}/standings", params=params, headers=headers).json() 
    teams = (standings_data['standings'][0]['table'])
    print("Positon | Team                           | Points | Won | Draw | Lost | GD   |")
    print("----------------------------------------------------------------------------")
    for team in teams:
        print(f"{team['position']:<7} | {team['team']['name']:<30} | {team['points']:<6} | {team['won']:<3} | {team['draw']:<4} | {team['lost']:<4} | {team['goalDifference']:<4} |")


def top_scorers(league):
    scorers_data = requests.get(base_url + f"competitions/{league}/scorers", params={'status': 'FINISHED', 'limit': 10}, headers=headers).json() 
    data = scorers_data['scorers']
    print('Player                     Goals')
    for position, player in enumerate(data):
        print(f"{position+1:<3} | {player['player']['name']:<20} | {player['goals']:<6}")


def get_matches(league):
    matches_data = requests.get(base_url + f"competitions/{league}/matches", params={'status': 'FINISHED', 'limit': 1, 'season' : '2023', 'matchday' : '1'}, headers=headers).json()
    current_matchday = matches_data['matches'][0]['season']['currentMatchday'] 
    print(f"{leagues[league.lower()]} MATCHDAY {current_matchday}")
    print('-------------------------------------')
    current_matchday_data = requests.get(base_url + f"competitions/{league}/matches", params={'status': 'FINISHED', 'limit': 1, 'season' : '2023', 'matchday' : f'{current_matchday}'}, headers=headers).json()
    for match in current_matchday_data['matches']:
        home_team = match['homeTeam']['name']
        home_score = match['score']['fullTime']['home']
        away_team = match['awayTeam']['name']
        away_score = match['score']['fullTime']['away']

        print(f'{home_team} {home_score} V {away_team} {away_score}')
        print('-------------------------------------')
 


valid_inputs = {'pl', 'bl', 'sa',  'fl1','pd'}

def main():
    print('Football Analytics')
    print('------------------------------')
    print('Available Leagues:')
    for code, name in leagues.items():
        print(f"{name} ~ {code.upper()}")

    while True:
        league = input('Select a league code (q to quit): \n').lower()
        if league == 'q':
            break
        while league not in valid_inputs:
            print('Input not valid!')
            league = input('Select a league code (q to quit): \n').lower()

        print(leagues[league].upper())
        print('------------------------------')

        while True:
            print('Commands:')
            print('Standings')
            print('Top Scorers')
            print('Recent Matches')
            print('(b to change leagues)')
            print('(q to quit)')
            command = input('Enter a command: \n').lower()

            if command == 'standings':
                get_standings(league.upper())
            elif command == 'top scorers':
                top_scorers(league.upper())
            elif command == 'recent matches':
                get_matches(league.upper())
            elif command == 'b':
                break
            elif command == 'q':
                return
            else:
                print('Invalid Command!\n')

main()