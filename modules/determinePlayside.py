from typing import Dict


def determine_playerTeamSide(match: Dict, round_data: Dict, focusPlayer: str) -> tuple:
    """
    Determines which team (A or B) and side (CT or T) the focus player was on for a given round
    """
    
    # Find which team the focus player is on
    player_team_letter = None
    for player_name, player_data in match["players"].items():
        if player_name == focusPlayer:
            player_team_name = player_data.get("teamName")
            # Check if player is on Team A or Team B
            if player_team_name == match["teamA"]["name"] or player_team_name == "Team A":
                player_team_letter = "A"
            elif player_team_name == match["teamB"]["name"] or player_team_name == "Team B":
                player_team_letter = "B"
            break
    
    if not player_team_letter:
        return None, None
    
    # Get the side for this round
    if player_team_letter == "A":
        side = round_data.get("teamASide")
    else:
        side = round_data.get("teamBSide")
    
    # Convert side number to string (2 = CT, 3 = T in CS2)
    side_str = "CT" if side == 2 else "T" if side == 3 else None
    
    return player_team_letter, side_str