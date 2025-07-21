from typing import Dict

def generate_report(stats_dict: Dict, focus_player: str) -> str:
    """
    Formats the stats dictionary into a human-readable markdown format for Obsidian
    """
    output = []
    
    # Overall Stats Summary
    total_stats = stats_dict.get('total_stats', {})
    total_matches = total_stats.get('won', 0) + total_stats.get('lost', 0) + total_stats.get('tied', 0)
    win_rate = (total_stats.get('won', 0) / total_matches * 100) if total_matches > 0 else 0
    
    output.append("## Overall Performance")
    output.append("")
    output.append(f"**Total Matches:** {total_matches}")
    output.append("")
    output.append(f"**Win Rate:** {win_rate:.1f}% ({total_stats.get('won', 0)}W-{total_stats.get('lost', 0)}L-{total_stats.get('tied', 0)}T)")
    
    # Map statistics for strongest/weakest
    map_stats = stats_dict.get('map_stats', {})
    if map_stats:
        best_map = max(map_stats.items(), key=lambda x: x[1]['won'] / x[1]['total_matches'] if x[1]['total_matches'] > 0 else 0)
        worst_map = min(map_stats.items(), key=lambda x: x[1]['won'] / x[1]['total_matches'] if x[1]['total_matches'] > 0 else 1)
        
        output.append(f"- _Strongest Map:_ {best_map[0].replace('de_', '').title()} ({best_map[1]['won']}/{best_map[1]['total_matches']} wins)")
        output.append(f"- _Weakest Map:_ {worst_map[0].replace('de_', '').title()} ({worst_map[1]['won']}/{worst_map[1]['total_matches']} wins)")
        output.append("")
    
    # Players of the week
    player_stats = stats_dict.get('player_stats', {})
    if player_stats:
        output.append("**Players of the week:**")
        
        # Top fragger
        top_fragger = max(player_stats.items(), key=lambda x: x[1]['kills'] / x[1]['matches'] if x[1]['matches'] > 0 else 0)
        output.append(f"- _Top Fragger:_ {top_fragger[0]} ({top_fragger[1]['kills']/top_fragger[1]['matches']:.1f} kills/match)")
        
        # Best clutcher
        best_clutcher = max(player_stats.items(), key=lambda x: sum([x[1]['vsOneWon'], x[1]['vsTwoWon'], x[1]['vsThreeWon'], x[1]['vsFourWon'], x[1]['vsFiveWon']]))
        total_clutch_wins = sum([best_clutcher[1]['vsOneWon'], best_clutcher[1]['vsTwoWon'], best_clutcher[1]['vsThreeWon'], best_clutcher[1]['vsFourWon'], best_clutcher[1]['vsFiveWon']])
        output.append(f"- _Best Clutcher:_ {best_clutcher[0]} ({total_clutch_wins} clutch wins)")
        
        # Headshot machine (highest headshot percentage)
        headshot_machine = max(player_stats.items(), key=lambda x: (x[1]['headshots'] / x[1]['kills'] * 100) if x[1]['kills'] > 0 else 0)
        hs_percentage = (headshot_machine[1]['headshots'] / headshot_machine[1]['kills'] * 100) if headshot_machine[1]['kills'] > 0 else 0
        output.append(f"- _Headshot Machine:_ {headshot_machine[0]} ({hs_percentage:.1f}% headshot rate)")
        output.append("")
    
    # Map Performance Table
    output.append("## Map Performance")
    output.append("")
    output.append("| Map | Matches | Record | Win% | CT Win% | T Win% |")
    output.append("| --- | ------- | ------ | ---- | ------- | ------ |")
    
    # Sort maps by matches played (descending)
    sorted_maps = sorted(map_stats.items(), key=lambda x: x[1]['total_matches'], reverse=True)
    
    for map_name, stats in sorted_maps:
        matches = stats['total_matches']
        won = stats['won']
        lost = stats['lost']
        tied = stats['tied']
        map_win_rate = (won / matches * 100) if matches > 0 else 0
        
        # Format map name with italic prefix
        map_display = f"_{map_name}_"
        
        output.append(f"| {map_display} | {matches} | {won}W-{lost}L-{tied}T | {map_win_rate:.0f}% | | |")
    
    output.append("")
    
    # Player Statistics Table
    output.append("## Player Statistics")
    output.append("")
    output.append("| Player | Matches | KDA | K/D | Headshot% | MVPs | Clutch% |")
    output.append("| ------ | ------- | --- | --- | --------- | ---- | ------- |")
    
    # Sort players by matches played (descending)
    sorted_players = sorted(player_stats.items(), key=lambda x: x[1]['matches'], reverse=True)
    
    for player_name, stats in sorted_players:
        matches = stats['matches']
        kills = stats['kills']
        deaths = stats['deaths']
        assists = stats['assists']
        kd_ratio = kills / deaths if deaths > 0 else kills
        hs_percentage = (stats['headshots'] / kills * 100) if kills > 0 else 0
        
        # Clutch statistics
        total_clutches = sum([stats['vsOneCount'], stats['vsTwoCount'], stats['vsThreeCount'], 
                             stats['vsFourCount'], stats['vsFiveCount']])
        total_clutch_wins = sum([stats['vsOneWon'], stats['vsTwoWon'], stats['vsThreeWon'], 
                                stats['vsFourWon'], stats['vsFiveWon']])
        clutch_success_rate = (total_clutch_wins / total_clutches * 100) if total_clutches > 0 else 0
        player_display = f"_{player_name}_"
        
        output.append(f"| {player_display} | {matches} | {kills}/{deaths}/{assists} | {kd_ratio:.2f} | {hs_percentage:.1f}% | {stats['mvp']} | {clutch_success_rate:.1f}% |")
        
    output.append("")
    
    return '\n'.join(output)