import chess
import chess.engine
import time
from dotenv import load_dotenv
import json
from lichess_bot import start_challenge, get_game_stream, make_move, wait_for_game_ready

load_dotenv()

# Set the path to Stockfish
STOCKFISH_PATH = "C:/stockfish/stockfish-windows-x86-64-avx2.exe"
engine = chess.engine.SimpleEngine.popen_uci(STOCKFISH_PATH)

def get_best_move_from_stockfish(board):
    try:
        print("Getting best move from Stockfish...")
        result = engine.play(board, chess.engine.Limit(time=2.0))
        best_move = result.move
        print("Best move:", best_move)
        return best_move
    except Exception as e:
        print(f"Error in Stockfish: {e}")
        return None
    


def reward_system(result):
    if result == "win":
        reward = 10
    elif result == "loss":
        reward = -5
    else:  # For draw or unknown results
        reward = 1
    print(f"Reward: {reward}")

def play_game(stop_event):
    # Start a game
    game_info = start_challenge()
    print("Game Info:", game_info)

    if 'id' not in game_info:
        print("Failed to start a game or 'id' not found in response.")
        return

    game_id = game_info['id']

    # Check game status
    if game_info['status'] != 'created':
        print("Game is not in a state to be streamed.")
        return

    board = chess.Board()

    # Introduce a delay before streaming
    time.sleep(2)

    # Watch the game stream
    for line in get_game_stream(game_id):
        if line:
            event = json.loads(line)
            print(event)  # Print the entire event for debugging purposes

            # Handle game state events
            if 'type' in event:
                if event['type'] == 'gameState':
                    board.set_fen(event['state']['fen'])
                    if board.turn:
                        best_move = get_best_move_from_stockfish(board)
                        make_move(game_id, best_move.uci())
                elif event['type'] == 'gameFinish':
                    print("Game finished.")
                    if 'winner' in event:
                        result = "win" if event['winner'] == 'white' else "loss"
                    else:
                        result = "draw"
                    reward_system(result)  # Call the reward system
                    break
            else:
                print("Event does not contain 'type':", event)  # Handle unexpected events


def main():
    challenge = start_challenge()
    game_id = challenge.get('id')
    print("Challenge Response:", challenge)
    print("Game ID:", game_id)

    if game_id:
        wait_for_game_ready(game_id)
    else:
        print("Failed to get a valid game ID from the challenge.")

if __name__ == "__main__":
    main()
