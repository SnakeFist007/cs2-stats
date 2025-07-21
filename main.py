import glob
import json
import argparse
import sys
from pathlib import Path
from typing import Dict
from modules.demoExtractor import extract_demoData
from modules.playerFilter import filter_players
from modules.reportGenerator import generate_report
from modules.statsAnalyzer import analyze_stats


def load_playerMapping(mapping_file: str) -> Dict[str, str]:
    """
    Loads player mapping from a file.
    """
    try:
        with open(mapping_file, "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"Error: Player mapping file '{mapping_file}' not found.")
        sys.exit(1)
    except json.JSONDecodeError:
        print(f"Error: Invalid JSON format in '{mapping_file}'.")
        sys.exit(1)


def parse_arguments():
    """
    Parse command line arguments.
    """
    parser = argparse.ArgumentParser(
        description="CS2 Stats Analyzer - Generate match reports from demo JSON files",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )
    
    parser.add_argument(
        "--input-dir", "-i",
        type=str,
        default="input",
        help="Directory containing JSON demo files"
    )
    
    parser.add_argument(
        "--player-mapping", "-m",
        type=str,
        default="player_mapping.json",
        help="Path to player mapping JSON file"
    )
    
    parser.add_argument(
        "--focus-player", "-p",
        type=str,
        required=True,
        help="Name of the focus player for analysis (required)"
    )
    
    parser.add_argument(
        "--output", "-o",
        type=str,
        help="Output file path (optional, prints to console if not specified)"
    )
    
    parser.add_argument(
        "--file-pattern",
        type=str,
        default="*.json",
        help="File pattern to match JSON files"
    )
    
    return parser.parse_args()


def validate_inputs(args):
    """
    Validate the provided input arguments.
    """
    # Check if input directory exists
    input_path = Path(args.input_dir)
    if not input_path.exists():
        print(f"Error: Input directory '{args.input_dir}' does not exist.")
        sys.exit(1)
    
    if not input_path.is_dir():
        print(f"Error: '{args.input_dir}' is not a directory.")
        sys.exit(1)
    
    # Check if player mapping file exists
    mapping_path = Path(args.player_mapping)
    if not mapping_path.exists():
        print(f"Error: Player mapping file '{args.player_mapping}' does not exist.")
        sys.exit(1)
    
    # Check if there are JSON files in the input directory
    json_pattern = str(input_path / args.file_pattern)
    json_files = glob.glob(json_pattern)
    if not json_files:
        print(f"Error: No JSON files found matching pattern '{json_pattern}'.")
        sys.exit(1)
    
    print(f"Found {len(json_files)} JSON files to process.")
    return json_files


def main() -> None:
    # Parse command line arguments
    args = parse_arguments()
    
    # Validate inputs
    json_files = validate_inputs(args)
    
    # Load player mapping
    player_mapping = load_playerMapping(args.player_mapping)
    
    # Verify focus player is in mapping
    focus_player_found = False
    for mapped_names in player_mapping.values():
        if args.focus_player == mapped_names:
            focus_player_found = True
            break
    
    if not focus_player_found:
        print(f"Warning: Focus player '{args.focus_player}' not found in player mapping.")
        print("Available players:", list(set(player_mapping.values())))
        response = input("Continue anyway? (y/N): ")
        if response.lower() != 'y':
            sys.exit(1)
    
    try:
        print(f"Analyzing matches for focus player: {args.focus_player}")
        print(f"Processing {len(json_files)} demo files...")
        
        extractedDemo = extract_demoData(json_files)
        filteredData = filter_players(extractedDemo, player_mapping)
        stats = analyze_stats(filteredData, args.focus_player)
        output = generate_report(stats)
        
        # Output handling
        if args.output:
            output_path = Path(args.output)
            # Create output directory if it doesn't exist
            output_path.parent.mkdir(parents=True, exist_ok=True)
            
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(output)
            print(f"Report saved to: {args.output}")
        else:
            print("\n" + "="*50)
            print("CS2 MATCH REPORT")
            print("="*50)
            print(output)

    except Exception as e:
        print(f"Error during analysis: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()