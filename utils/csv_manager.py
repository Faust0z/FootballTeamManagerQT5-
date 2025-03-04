import pandas as pd
import os.path

from utils.players import TeamMember

data_route = os.path.join(os.path.dirname(__file__), "..", "data", "players.csv")
os.makedirs(os.path.dirname(data_route), exist_ok=True)

def read_players() -> list:
    if not os.path.exists(data_route):
        df = pd.DataFrame(columns=["shirt_number", "last_name", "position", "time_played", "scored_goals"])
        df.to_csv(data_route, index=False, encoding="utf-8")
        return []

    df = pd.read_csv(data_route)
    players = []
    for _, row in df.iterrows():
        players.append(TeamMember(row["shirt_number"], row["last_name"], row["position"], row["time_played"], row["scored_goals"]))
    return players

def write_player(player: TeamMember) -> bool:
    try:
        df = pd.DataFrame([vars(player)], columns=["shirt_number", "last_name", "position", "time_played", "scored_goals"])
        df.to_csv(data_route, mode="a", header=False, index=False)  # Append without header/index
        return True
    except (IOError, OSError, ValueError) as e:
        print(f"Error writing CSV: {e}")
        return False

def rewrite_players(players: list) -> bool:
    try: # It's easier to just dump the list into the csv than delete a line
        players_data = [{
            'shirt_number': player.shirt_number,
            'last_name': player.last_name,
            'position': player.position,
            'time_played': player.time_played,
            'scored_goals': player.scored_goals
        } for player in players]

        df = pd.DataFrame(players_data, columns=["shirt_number", "last_name", "position", "time_played", "scored_goals"])
        df.to_csv(data_route, index=False, header=True, encoding="utf-8")
        return True
    except (IOError, OSError, ValueError) as e:
        print(f"Error writing tasks: {e}")
        return False
