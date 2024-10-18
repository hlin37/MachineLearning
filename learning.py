import requests
import re

# Base URL of the AUDL Stats API
game_url = "https://www.backend.ufastats.com/api/v1/games"
game_events_url = "https://www.backend.ufastats.com/api/v1/gameEvents"

# Set parameters to filter for games in 2022
params = {
    "date": 2024
}

# Send a GET request to fetch all games from 2022
response = requests.get(game_url, params=params)

games = response.json()

gameIDArray = []

for i in range(len(games['data'])):
    gameIDArray.append(games['data'][i]['gameID'])

eventParams = {
    "gameID" : None
}

counter = 0
for item in gameIDArray:
    if (counter == 0):
        eventParams["gameID"] = item
        response = requests.get(game_events_url, params=eventParams)

        text = response.text
        counter += 1


