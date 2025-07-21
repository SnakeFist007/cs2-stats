from typing import Dict


def generate_report(stats_dict: Dict) -> str:
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
    output.append(f"**Total Matches:** {total_matches} ({total_stats.get('won', 0)}W-{total_stats.get('lost', 0)}L-{total_stats.get('tied', 0)}T)")
    
    # Map statistics for strongest/weakest
    map_stats = stats_dict.get('map_stats', {})
    if map_stats:
        best_map = max(map_stats.items(), key=lambda x: x[1]['won'] / x[1]['total_matches'] if x[1]['total_matches'] > 0 else 0)
        worst_map = min(map_stats.items(), key=lambda x: x[1]['won'] / x[1]['total_matches'] if x[1]['total_matches'] > 0 else 1)
        
        output.append(f"- _Strongest Map:_ {best_map[0].replace('de_', '').title()} ({best_map[1]['won']}/{best_map[1]['total_matches']} wins)")
        output.append(f"- _Weakest Map:_ {worst_map[0].replace('de_', '').title()} ({worst_map[1]['won']}/{worst_map[1]['total_matches']} wins)")
        output.append("")
    
    # Add round statistics
    ct_rounds_total = total_stats.get('ctRoundsTotal', 0)
    ct_rounds_won = total_stats.get('ctRoundsWon', 0)
    t_rounds_total = total_stats.get('tRoundsTotal', 0)
    t_rounds_won = total_stats.get('tRoundsWon', 0)
    
    ct_win_rate = (ct_rounds_won / ct_rounds_total * 100) if ct_rounds_total > 0 else 0
    t_win_rate = (t_rounds_won / t_rounds_total * 100) if t_rounds_total > 0 else 0
    
    output.append(f"**Win Rate:** {win_rate:.1f}%")
    output.append(f"- _CT Side:_ {ct_win_rate:.1f}% ({ct_rounds_won}/{ct_rounds_total} rounds)")
    output.append(f"- _T Side:_ {t_win_rate:.1f}% ({t_rounds_won}/{t_rounds_total} rounds)")
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
    
    # Get round stats
    round_stats = stats_dict.get('round_stats', {})
    
    # Sort maps by matches played (descending)
    sorted_maps = sorted(map_stats.items(), key=lambda x: x[1]['total_matches'], reverse=True)
    
    for map_name, stats in sorted_maps:
        matches = stats['total_matches']
        won = stats['won']
        lost = stats['lost']
        tied = stats['tied']
        map_win_rate = (won / matches * 100) if matches > 0 else 0
        
        # Get CT/T win rates for this map
        map_round_stats = round_stats.get(map_name, {})
        ct_rounds = map_round_stats.get('ctRoundsTotal', 0)
        ct_wins = map_round_stats.get('ctRoundsWon', 0)
        t_rounds = map_round_stats.get('tRoundsTotal', 0)
        t_wins = map_round_stats.get('tRoundsWon', 0)
        
        ct_win_pct = (ct_wins / ct_rounds * 100) if ct_rounds > 0 else 0
        t_win_pct = (t_wins / t_rounds * 100) if t_rounds > 0 else 0
        
        # Format map name with italic prefix
        map_display = f"_{map_name}_"
        
        output.append(f"| {map_display} | {matches} | {won}W-{lost}L-{tied}T | {map_win_rate:.0f}% | {ct_win_pct:.0f}% | {t_win_pct:.0f}% |")
    
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
    
    # Add Side Performance Summary if round stats exist
    if round_stats:
        output.append("## Side Performance Summary")
        output.append("")
        output.append("| Map | CT Rounds | CT Win% | T Rounds | T Win% | Side Preference |")
        output.append("| --- | --------- | ------- | -------- | ------ | --------------- |")
        
        for map_name, stats in sorted_maps:
            map_round_stats = round_stats.get(map_name, {})
            ct_rounds = map_round_stats.get('ctRoundsTotal', 0)
            ct_wins = map_round_stats.get('ctRoundsWon', 0)
            t_rounds = map_round_stats.get('tRoundsTotal', 0)
            t_wins = map_round_stats.get('tRoundsWon', 0)
            
            if ct_rounds > 0 or t_rounds > 0:
                ct_win_pct = (ct_wins / ct_rounds * 100) if ct_rounds > 0 else 0
                t_win_pct = (t_wins / t_rounds * 100) if t_rounds > 0 else 0
                
                # Determine side preference
                if ct_win_pct > t_win_pct + 5:
                    preference = "CT-sided"
                elif t_win_pct > ct_win_pct + 5:
                    preference = "T-sided"
                else:
                    preference = "Balanced"
                
                map_display = f"_{map_name}_"
                output.append(f"| {map_display} | {ct_wins}/{ct_rounds} | {ct_win_pct:.0f}% | {t_wins}/{t_rounds} | {t_win_pct:.0f}% | {preference} |")
        
        output.append("")
    
    return '\n'.join(output)