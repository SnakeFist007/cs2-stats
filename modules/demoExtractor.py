import json
from typing import Dict


def extract_demoData(json_files: Dict) -> Dict:
    """
    Extracts match data from JSON structure and normalizes player names
    """
    matches = {}
    
    for file_path in json_files:
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                match = json.load(f)
            
            # Store match data in the matches dictionary
            matches[match["name"]] = {
                "date": match["date"],
                "map": match["mapName"],
                "teamA": match["teamA"],
                "teamB": match["teamB"],
                "players": match["players"],
                "rounds": match["rounds"]
            }
                      
        except Exception as e:
            print(f"Error loading {file_path}: {e}")
            
    return matches