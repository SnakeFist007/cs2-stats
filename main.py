# CS2 Analyzer
import glob
from modules.demoExtractor import extract_demoData
from modules.playerFilter import filter_players
from modules.reportGenerator import generate_report
from modules.statsAnalyzer import analyze_stats


def main() -> None:
    json_files = glob.glob("input/*.json")
    
    # Player mapping
    player_mapping = {
        "BT-9979": "Avdi",
        "Door stuck": "Avdi", 
        "141 2/3 chance of winnin": "Avdi",
        "Lales": "Lales",
        "Melkmir": "Lales",
        "MrAeRoZz": "MrAeRoZz",
        "Zephiii": "MrAeRoZz",
        "SnakeFist": "SnakeFist",
        "vypR": "SnakeFist"
    }

    try:
        stats = analyze_stats(filter_players(extract_demoData(json_files), player_mapping), "SnakeFist")
        output = generate_report(stats, "SnakeFist")
        
        print(output)
        
        # TODO: Save output to file
        # with open("output/report.md", "w", encoding="utf-8") as f:
        #     f.write(output)
        #
        # print("Report saved to report.md")

    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
