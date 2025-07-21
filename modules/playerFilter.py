from typing import Dict


def filter_players(matches: Dict, player_mapping: Dict) -> Dict:
    """
    Filters players to only include those in the player mapping and normalizes their names
    """
    filtered_matches = {}
    
    for match_name, match_data in matches.items():
        filtered_players = {}
        filtered_match = {
            "date": match_data["date"],
            "map": match_data["map"],
            "teamA": match_data["teamA"],
            "teamB": match_data["teamB"],
            "players": {},
            "rounds": match_data["rounds"]
        }
        
        # Filter and normalize players
        for player_data in match_data["players"]:
            if player_data["name"] in player_mapping:
                # Use the normalized name from the mapping
                normalized_name = player_mapping[player_data["name"]]
                filtered_players[normalized_name] = player_data
        
        # Update the players dict with filtered data
        filtered_match["players"] = filtered_players
        filtered_matches[match_name] = filtered_match
    
    return filtered_matches