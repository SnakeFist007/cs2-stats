import glob
import json
from typing import Dict
from modules.demoExtractor import extract_demoData
from modules.playerFilter import filter_players
from modules.reportGenerator import generate_report
from modules.statsAnalyzer import analyze_stats


def load_playerMapping() -> Dict[str, str]:
    """
    Loads player mapping from a file.
    """
    with open("player_mapping.json", "r", encoding="utf-8") as f:
        return json.load(f)


def main() -> None:
    # Load data
    json_files = glob.glob("input/*.json")
    # Load variables
    player_mapping = load_playerMapping()
    focusPlayer = "SnakeFist"
    
    try:
        extractedDemo = extract_demoData(json_files)
        filteredData = filter_players(extractedDemo, player_mapping)
        stats = analyze_stats(filteredData, focusPlayer)
        output = generate_report(stats)
        
        print(output)

    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
