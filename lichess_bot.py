import requests
import os
import json
import time
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv("LICHESS_API")
print("Loaded Token:", TOKEN)

def start_challenge():
    response = requests.post(
        "https://lichess.org/api/challenge/open",
        headers={"Authorization": f"Bearer {TOKEN}"}
    )
    print("Challenge Response:", response.json())
    return response.json()
    

def wait_for_game_ready(game_id):
    time.sleep(10)  # Initial delay
    while True:
        response = requests.get(
            f"https://lichess.org/api/bot/game/stream/{game_id}",
            headers={"Authorization": f"Bearer {TOKEN}"}
        )
        print("Game ID being checked:", game_id)
        print("Game Status Response:", response.text)
        game_status = response.json()
        if 'error' in game_status:
            print("Error in fetching game status:", game_status)
            time.sleep(5)  # Retry delay
        else:
            print("Game is ready:", game_status)
            return game_status

def get_game_stream(game_id):
    response = requests.get(
        f"https://lichess.org/api/bot/game/stream/{game_id}",
        headers={"Authorization": f"Bearer {TOKEN}"}
    )
    return response.iter_lines()

def make_move(game_id, move):
    response = requests.post(
        f"https://lichess.org/api/bot/game/{game_id}/move/{move}",
        headers={"Authorization": f"Bearer {TOKEN}"}
    )
    if response.status_code != 200:
        print("Failed to make move:", response.json())

# Start the game
game_info = start_challenge()
if 'id' in game_info:
    game_id = game_info['id']
    print(f"Game ID: {game_id}")
    time.sleep(2)
    # Wait for the game to be ready
    game_state = wait_for_game_ready(game_id)

    # Start streaming game events
    for line in get_game_stream(game_id):
        if line:
            event = json.loads(line)
            print(event)
else:
    print("Failed to start a game or 'id' not found in response.")
