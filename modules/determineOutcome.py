from typing import Dict


def determine_outcome(match: Dict, focusPlayer: str) -> str:
    """
    Determines the outcome of a match (Win, Loss, Tie)
    """
    teamA_score = match["teamA"]["score"]
    teamB_score = match["teamB"]["score"]
    
    focus_player_team = None
    for player_name, player_data in match["players"].items():
        if player_name == focusPlayer:
            focus_player_team = player_data["teamName"]
            break
    
    # Check if focus player was on Team A
    if focus_player_team == match["teamA"]["name"]:
        wasOnA = True
    else:
        wasOnA = False
    
    if teamA_score > teamB_score:
        # Team A won
        matchOutcome = "Win" if wasOnA else "Loss"
    elif teamA_score < teamB_score:
        # Team B won
        matchOutcome = "Loss" if wasOnA else "Win"
    else:
        # Tie
        matchOutcome = "Tie"
    
    return matchOutcome