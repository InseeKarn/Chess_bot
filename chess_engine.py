import chess.engine

# Stockfish path setting
STOCKFISH_PATH = "C:/stockfish/stockfish-windows-x86-64-avx2.exe"
engine = chess.engine.SimpleEngine.popen_uci(STOCKFISH_PATH)

def get_best_move_from_stockfish(board):
    try:
        result = engine.play(board, chess.engine.Limit(time=2.0))  # เพิ่มเวลาหากจำเป็น
        best_move = result.move
        print("Best move:", best_move)
        return best_move
    except Exception as e:
        print(f"Error in Stockfish: {e}")
        return None

def close_engine():
    engine.quit()
