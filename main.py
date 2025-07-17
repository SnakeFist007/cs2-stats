import pandas as pd
import numpy as np
from pathlib import Path
import glob
from typing import List, Tuple, Dict, Any


def process_cs2_stats(csv_files: List[str]) -> Tuple[pd.DataFrame, pd.DataFrame]:
    """
    Processes CS2 Stats exported from CS:DM
    """
    
    # Player mapping
    player_mapping = {
        'BT-9979': 'Avdi',
        'Door stuck': 'Avdi', 
        '141 2/3 chance of winnin': 'Avdi',
        'Lales': 'Lales',
        'Melkmir': 'Lales',
        'MrAeRoZz': 'MrAeRoZz',
        'Zephiii': 'MrAeRoZz',
        'SnakeFist': 'SnakeFist',
        'vypR': 'SnakeFist'
    }
    
    # Target Outputs
    target_players = ['Avdi', 'Lales', 'MrAeRoZz', 'SnakeFist']
    
    # If csv_files is a string, convert to list
    if isinstance(csv_files, str):
        csv_files = glob.glob(csv_files)
    
    per_map_results = []
    all_data = []
    
    # Process every map
    for file_path in csv_files:
        try:
            df = pd.read_csv(file_path)
            map_name = Path(file_path).stem
            print(f"Processing {map_name}: {len(df)} lines...")
            
            # Map player names
            df['unified_name'] = df['name'].map(player_mapping)
            df['unified_name'] = df['unified_name'].fillna(df['name'])
            
            # Filter for target players
            filtered_df = df[df['unified_name'].isin(target_players)]
            
            if len(filtered_df) == 0:
                print(f"No target players found in {map_name}!")
                continue
                
            print(f"Found {len(filtered_df)} entries for target players.")
            
            # Process every player for this map
            for player in target_players:
                player_data = filtered_df[filtered_df['unified_name'] == player]
                
                if len(player_data) == 0:
                    continue
                
                # Calculate stats
                stats = calculate_player_stats(player_data, player, map_name)
                per_map_results.append(stats)
            
            # Collect data for total view
            all_data.append(filtered_df)
            
        except Exception as e:
            print(f"Fehler beim Laden von {file_path}: {e}")
    
    per_map_df = pd.DataFrame(per_map_results)
    
    # Create total view
    if all_data:
        combined_df = pd.concat(all_data, ignore_index=True)
        total_stats = []
        
        for player in target_players:
            player_data = combined_df[combined_df['unified_name'] == player]
            if len(player_data) > 0:
                stats = calculate_player_stats(player_data, player, "GESAMT")
                total_stats.append(stats)
        
        total_df = pd.DataFrame(total_stats)
    else:
        total_df = pd.DataFrame()
    
    return per_map_df, total_df


def calculate_player_stats(player_data: pd.DataFrame, player_name: str, map_name: str) -> Dict[str, Any]:
    """
    Calculates all statistics for a given player
    """
    # Base stats as sums
    total_matches = player_data['match_count'].sum()
    total_kills = player_data['kill_count'].sum()
    total_assists = player_data['assist_count'].sum()
    total_deaths = player_data['death_count'].sum()
    total_score = player_data['score'].sum()
    total_mvp = player_data['mvp'].sum()
    total_headshots = player_data['headshot_count'].sum()
    
    # Calculate metrics
    kd_ratio = total_kills / total_deaths if total_deaths > 0 else total_kills
    headshot_percentage = (total_headshots / total_kills * 100) if total_kills > 0 else 0
    
    # Get averages based on match_count
    def weighted_average(series, weights):
        if weights.sum() == 0:
            return 0
        return (series * weights).sum() / weights.sum()
    
    weights = player_data['match_count']
    avg_hltv = weighted_average(player_data['HLTV'], weights)
    avg_hltv_2 = weighted_average(player_data['HLTV 2.0'], weights)
    avg_kast = weighted_average(player_data['kast'], weights)
    avg_adr = weighted_average(player_data['adr'], weights)
    avg_rank = weighted_average(player_data['rank'], weights)
    
    # Clutch stats
    def calculate_clutch_winrate(data, situation):
        total_clutches = data[situation].sum()
        won_clutches = data[f'{situation}_won'].sum()
        return (won_clutches / total_clutches * 100) if total_clutches > 0 else 0
    
    clutch_1v1 = calculate_clutch_winrate(player_data, '1v1')
    clutch_1v2 = calculate_clutch_winrate(player_data, '1v2')
    clutch_1v3 = calculate_clutch_winrate(player_data, '1v3')
    clutch_1v4 = calculate_clutch_winrate(player_data, '1v4')
    clutch_1v5 = calculate_clutch_winrate(player_data, '1v5')
    
    return {
        'Map': map_name,
        'Name': player_name,
        'Matches': total_matches,
        'Kills': total_kills,
        'Assists': total_assists,
        'Deaths': total_deaths,
        'KD': round(kd_ratio, 2),
        'Score': total_score,
        'MVP': total_mvp,
        'Headshot%': round(headshot_percentage, 1),
        'HLTV': round(avg_hltv, 2),
        'HLTV 2.0': round(avg_hltv_2, 2),
        'KAST': round(avg_kast, 1),
        'ADR': round(avg_adr, 1),
        'Rank': round(avg_rank, 1),
        '1v1 Win%': round(clutch_1v1, 1),
        '1v2 Win%': round(clutch_1v2, 1),
        '1v3 Win%': round(clutch_1v3, 1),
        '1v4 Win%': round(clutch_1v4, 1),
        '1v5 Win%': round(clutch_1v5, 1)
    }


def save_results(per_map_df: pd.DataFrame, total_df: pd.DataFrame, output_prefix: str = 'cs2_stats') -> None:
    """
    Saves results in separate csv-files.
    """
    per_map_file = f'{output_prefix}_per_map.csv'
    total_file = f'{output_prefix}_total.csv'
    
    per_map_df.to_csv(per_map_file, index=False)
    total_df.to_csv(total_file, index=False)
    
    print(f"\nSaved results:")
    print(f"  Map statistics:   {per_map_file}")
    print(f"  Total statistics: {total_file}")


def display_results(per_map_df: pd.DataFrame, total_df: pd.DataFrame) -> None:
    """
    Displays results in console
    """
    pd.set_option('display.max_columns', None)
    pd.set_option('display.width', None)
    pd.set_option('display.max_colwidth', None)
    
    print("\n" + "="*160)
    print("CS2 PLAYER STATISTICS - PER MAP")
    print("="*160)
    
    # Group results by map
    for map_name in sorted(per_map_df['Map'].unique()):
        if map_name == 'TOTAL':
            continue
        map_data = per_map_df[per_map_df['Map'] == map_name].sort_values('KD', ascending=False)
        print(f"\n{map_name.upper()}:")
        print(map_data.drop('Map', axis=1).to_string(index=False))
    
    print("\n" + "="*160)
    print("CS2 PLAYER STATISTICS - TOTAL")
    print("="*160)
    
    if not total_df.empty:
        total_display = total_df.drop('Map', axis=1).sort_values('KD', ascending=False)
        print(total_display.to_string(index=False))
    else:
        print("No total results available.")
    
    print("="*160)

def main() -> None:
    """
    Main function
    """
    csv_files = glob.glob('input/*.csv')
    
    try:
        print("Running CS2 match analysis...")
        print("Target players: Avdi, Lales, MrAeRoZz, SnakeFist")
        print("-" * 60)
        
        per_map_stats, total_stats = process_cs2_stats(csv_files)
        
        if per_map_stats.empty:
            print("No data for target players found!")
            return
        
        display_results(per_map_stats, total_stats)
        save_results(per_map_stats, total_stats)
        
        print(f"\nFinished processing!")
        print(f"  Processed maps:    {len(per_map_stats['Map'].unique())}")
        print(f"  Processed players: {len(total_stats)}")
        
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()