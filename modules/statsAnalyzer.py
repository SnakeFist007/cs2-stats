from typing import Dict
from collections import defaultdict
from modules.determineOutcome import determine_outcome
from modules.determinePlayside import determine_playerTeamSide


def analyze_stats(matches: Dict, focusPlayer: str) -> Dict:
    """
    Analyzes match statistics
    """
    map_stats = defaultdict(lambda: {
        'total_matches': 0,
        'won': 0, 'lost': 0, 'tied': 0,
        'total_rounds': 0
    })
    
    # Initialize round stats
    round_stats = defaultdict(lambda: {
        'ctRoundsTotal': 0,
        'ctRoundsWon': 0,
        'tRoundsTotal': 0,
        'tRoundsWon': 0
    })
    
    player_stats = defaultdict(lambda: {
        'matches': 0,
        'kills': 0, 'assists': 0, 'deaths': 0,
        'mvp': 0, 'headshots': 0,
        'vsOneCount': 0, 'vsOneWon': 0,
        'vsTwoCount': 0, 'vsTwoWon': 0,
        'vsThreeCount': 0, 'vsThreeWon': 0,
        'vsFourCount': 0, 'vsFourWon': 0,
        'vsFiveCount': 0, 'vsFiveWon': 0
    })
    
    total_stats = {
        'total_matches': 0,
        'won': 0, 'lost': 0, 'tied': 0,
        'total_rounds': 0,
        'ctRoundsTotal': 0,
        'ctRoundsWon': 0,
        'tRoundsTotal': 0,
        'tRoundsWon': 0
    }
    
    # Process matches
    for match_name, match in matches.items():
        map_name = match["map"]
    
        # Process general map statistics
        map_stats[map_name]["total_matches"] += 1
        map_stats[map_name]["total_rounds"] += (match["teamA"]["score"] + match["teamB"]["score"])
        total_stats["total_matches"] += 1
        total_stats["total_rounds"] += (match["teamA"]["score"] + match["teamB"]["score"])
        
        outcome = determine_outcome(match, focusPlayer)
        if outcome == "Win":
            map_stats[map_name]["won"] += 1
            total_stats["won"] += 1
        elif outcome == "Loss":
            map_stats[map_name]["lost"] += 1
            total_stats["lost"] += 1
        elif outcome == "Tie":
            map_stats[map_name]["tied"] += 1
            total_stats["tied"] += 1
            
        # Process round statistics
        if "rounds" in match:
            # Process each round
            for round_data in match["rounds"]:
                player_team_letter, side = determine_playerTeamSide(match, round_data, focusPlayer)
                
                if not player_team_letter or not side:
                    continue
                
                # Determine if focus player's team won
                winner_team_name = round_data.get("winnerTeamName", "")
                player_won = False
                
                if player_team_letter == "A" and winner_team_name == match["teamA"]["name"]:
                    player_won = True
                elif player_team_letter == "B" and winner_team_name == match["teamB"]["name"]:
                    player_won = True
                
                # Update statistics based on side
                if side == "CT":
                    round_stats[map_name]["ctRoundsTotal"] += 1
                    total_stats["ctRoundsTotal"] += 1
                    
                    if player_won:
                        round_stats[map_name]["ctRoundsWon"] += 1
                        total_stats["ctRoundsWon"] += 1
                        
                elif side == "T":
                    round_stats[map_name]["tRoundsTotal"] += 1
                    total_stats["tRoundsTotal"] += 1
                    
                    if player_won:
                        round_stats[map_name]["tRoundsWon"] += 1
                        total_stats["tRoundsWon"] += 1
            
        # Process players statistics
        for player_name, player in match["players"].items():
            stats = player_stats[player_name]
            
            # Basics
            stats["matches"] += 1
            stats["kills"] += player["killCount"]
            stats["assists"] += player["assistCount"]
            stats["deaths"] += player["deathCount"]
            stats["mvp"] += player["mvpCount"]
            stats["headshots"] += player["headshotCount"]
            
            # Per Round / Match stats (commented out as not in current data)
            #stats["utilityDamage"] += player["utilityDamage"]
            #stats["kast"] += player["kast"]
            #stats["hltv1"] += player["hltvRating"]
            #stats["hltv2"] += player["hltvRating2"]
            #stats["adr"] += player["averageDamagePerRound"]
            #stats["firstKills"] += player["firstKillCount"]
            #stats["firstDeaths"] += player["firstDeathCount"]
            
            # Clutches
            stats["vsOneCount"] += player["vsOneCount"]
            stats["vsOneWon"] += player["vsOneWonCount"]
            stats["vsTwoCount"] += player["vsTwoCount"]
            stats["vsTwoWon"] += player["vsTwoWonCount"]
            stats["vsThreeCount"] += player["vsThreeCount"]
            stats["vsThreeWon"] += player["vsThreeWonCount"]
            stats["vsFourCount"] += player["vsFourCount"]
            stats["vsFourWon"] += player["vsFourWonCount"]
            stats["vsFiveCount"] += player["vsFiveCount"]
            stats["vsFiveWon"] += player["vsFiveWonCount"]
            
    
    output = {
        "map_stats": dict(map_stats),
        "round_stats": dict(round_stats),
        "player_stats": dict(player_stats),
        "total_stats": dict(total_stats)
    }
    
    return output