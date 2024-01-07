import random
import csv

def read_teams_info(file_name):
    player_data = {}

    with open(file_name, 'r') as file:
        current_country = ""
        for line in file:
            line = line.strip()
            if line.startswith('Players of'):
                current_country = line.split('Players of ')[1].rstrip(':')
                player_data[current_country] = {'goalkeeper': [], 'defender': [], 'midfielder': [], 'striker': []}
            elif line.startswith('Position:'):
                position, skill, status = line.split(', ')
                position = position.split(': ')[1]
                skill = int(skill.split(': ')[1])
                player_data[current_country][position.lower()].append((skill, status))


    return player_data

def display_results(player_info):
    for country, positions in player_info.items():
        print(f"Players of {country}:")
        for position, skills in positions.items():
            for skill, status in skills:
                print(f"Position: {position.capitalize()}, Skill: {skill}, {status}")
        print('-' * 30)

def get_main_team(player_data):
    filtered_data = {}
    for country, positions in player_data.items():
        filtered_data[country] = {}
        for position, skills in positions.items():
            filtered_data[country][position] = [(skill, status) for skill, status in skills if status == 'M']
    return filtered_data

def calculate_success_probability(player_skill):    # wpływ umiejętności zawodnika na powodzenie podania lub strzalu
    base_probability = 0.5

    skill, status = player_skill
    if skill >= 85:
        return base_probability + 0.3
    elif skill >= 75:
        return base_probability + 0.2
    elif skill >= 65:
        return base_probability + 0.1
    else:
        return base_probability
    
def calculate_goal_probability(player_skill):   # prawdopodobieństwo strzelenia gola po wykonaniu celnego strzału

    return player_skill * 0.05

def simulate_match(team_a, team_b, team_a_name, team_b_name):
    score_team_a = 0
    score_team_b = 0
    positions = ['goalkeeper', 'defender', 'midfielder', 'striker']
    team_with_ball = random.choice([team_a, team_b])

    stats_team_a = {'Pass': 0, 'Shot': 0, 'Interception': 0, 'Goal': 0, 'ShotOnTarget': 0, 'OffTarget': 0}
    stats_team_b = {'Pass': 0, 'Shot': 0, 'Interception': 0, 'Goal': 0, 'ShotOnTarget': 0, 'OffTarget': 0}

    for minute in range(1, 91):
        events_in_minute = random.randint(1, 10)
        print(f"\nMinute: {minute}")
        print(f"Events in this minute: {events_in_minute}")

        for _ in range(events_in_minute):
            current_team = team_a if team_with_ball == team_a else team_b
            current_player_position = random.choice(positions)
            current_player = random.choice(current_team[current_player_position])

            if current_player_position == 'goalkeeper':
                events = ['Pass', 'Pass', 'Pass', 'Pass', 'Pass', 'Pass', 'Pass', 'Pass', 'Shot', 'Shot']
            elif current_player_position == 'defender':
                events = ['Pass', 'Pass', 'Pass', 'Pass', 'Pass', 'Shot', 'Pass', 'Pass', 'Pass', 'Pass']
            elif current_player_position == 'midfielder':
                events = ['Pass', 'Pass', 'Pass', 'Pass', 'Pass', 'Shot', 'Pass', 'Pass', 'Pass', 'Pass']
            else:
                events = ['Pass', 'Shot', 'Shot', 'Shot', 'Shot', 'Shot', 'Pass', 'Pass', 'Pass', 'Pass']

            action = random.choice(events)

            if action == 'Pass':
                next_player_position = random.choice(positions)
                next_player = random.choice(current_team[next_player_position])
                success_prob = calculate_success_probability(current_player)
                if random.random() < success_prob:
                    print(f"{current_player_position.capitalize()} passes the ball to {next_player}.")
                    if team_with_ball == team_a:
                        stats_team_a['Pass'] += 1
                    else:
                        stats_team_b['Pass'] += 1
                else:
                    print("The pass is intercepted! Opponent team gains possession.")
                    if team_with_ball == team_a:
                        stats_team_a['Interception'] += 1
                        team_with_ball = team_b
                    else:
                        stats_team_b['Interception'] += 1
                        team_with_ball = team_a
            elif action == 'Shot':
                success_prob = calculate_success_probability(current_player)
                if current_player_position != 'goalkeeper':
                    if random.random() < success_prob:
                        goal_prob = calculate_goal_probability(success_prob)
                        if random.random() < goal_prob:
                            print(f"GOAL for {team_with_ball}!")
                            if team_with_ball == team_a:
                                stats_team_a['Goal'] += 1
                                score_team_a += 1
                            else:
                                stats_team_b['Goal'] += 1
                                score_team_b += 1
                        else:
                            print(f"The shot is on target but didn't score. Possession goes to opponent.")
                            if team_with_ball == team_a:
                                stats_team_a['ShotOnTarget'] += 1
                                team_with_ball = team_b
                            else:
                                stats_team_b['ShotOnTarget'] += 1
                                team_with_ball = team_a
                    else:
                        print(f"The shot is off target! Possession goes to opponent.")
                        if team_with_ball == team_a:
                            stats_team_a['OffTarget'] += 1
                            team_with_ball = team_b
                        else:
                            stats_team_b['OffTarget'] += 1
                            team_with_ball = team_a
                else:
                    print("The goalkeeper cannot shoot!")

        print(f"Minute: {minute}")

    print(f"\nFinal Score: {team_a_name} - {score_team_a} : {score_team_b} - {team_b_name}")
    print("\nStatistics:")
    print(f"{team_a_name} - {stats_team_a}")
    print(f"{team_b_name} - {stats_team_b}")

    return {
        'Team A': score_team_a,
        'Team B': score_team_b,
        team_a_name: stats_team_a,
        team_b_name: stats_team_b
    }

def play_matches(teams):
    team_names = list(teams.keys())
    match_results = {}

    for i in range(len(team_names)):
        team_a = team_names[i]
        for j in range(i + 1, len(team_names)):
            team_b = team_names[j]
            print(f"Match between {team_a} and {team_b}")
            match_result = simulate_match(teams[team_a], teams[team_b], team_a, team_b)
            match_results[(team_a, team_b)] = match_result

    return match_results

def save_match_stats_to_txt(results):
    content = ""
    for match, result in results.items():
        content += f"Match: {match[0]} vs {match[1]}\n"
        content += f"Score: {result['Team A']} - {result['Team B']}\n"
        content += f"{match[0]} stats:\n"
        for stat, value in result[match[0]].items():
            if stat != 'Shot':
                content += f"{match[0]} {stat}: {value}\n"
        content += f"{match[1]} stats:\n"
        for stat, value in result[match[1]].items():
            if stat != 'Shot':
                content += f"{match[1]} {stat}: {value}\n"
        content += "-" * 50 + "\n"

    with open('match_stats.txt', 'w') as txt_file:
        txt_file.write(content)

def display_summary_table(results):
    all_teams_stats = {}
    teams_points = {}
    teams_wins = {}
    teams_losses = {}
    teams_draws = {}

    for match, result in results.items():
        team_a, team_b = match
        score_team_a = result['Team A']
        score_team_b = result['Team B']

        if score_team_a > score_team_b:
            winner = team_a
            loser = team_b
            winner_points = 3
            loser_points = 0
        elif score_team_a < score_team_b:
            winner = team_b
            loser = team_a
            winner_points = 3
            loser_points = 0
        else:
            winner = None
            loser = None
            winner_points = 1
            loser_points = 1

        if winner:
            if winner not in teams_points:
                teams_points[winner] = 0
            teams_points[winner] += winner_points

            if winner not in teams_wins:
                teams_wins[winner] = 0
            teams_wins[winner] += 1

        if loser:
            if loser not in teams_points:
                teams_points[loser] = 0
            teams_points[loser] += loser_points

            if loser not in teams_losses:
                teams_losses[loser] = 0
            teams_losses[loser] += 1

        if winner is None and loser is None:
            for team in [team_a, team_b]:
                if team not in teams_draws:
                    teams_draws[team] = 0
                teams_draws[team] += 1
                if team not in teams_points:
                    teams_points[team] = 0
                teams_points[team] += 1

        # Liczenie statystyk meczowych
        for team_name, stats in result.items():
            if team_name not in ['Team A', 'Team B']:
                if isinstance(stats, int):
                    stats = {'Goal': stats}
                if team_name not in all_teams_stats:
                    all_teams_stats[team_name] = {
                        'Matches Played': 0,
                        'Wins': 0,
                        'Losses': 0,
                        'Draws': 0,
                        'Goals Scored': 0,
                        'Passes': 0,
                        'Interceptions': 0,
                        'Shots On Target': 0,
                        'Off Target': 0,
                        'Points': 0 
                    }
                all_teams_stats[team_name]['Matches Played'] += 1
                all_teams_stats[team_name]['Wins'] = teams_wins.get(team_name, 0)
                all_teams_stats[team_name]['Losses'] = teams_losses.get(team_name, 0)
                all_teams_stats[team_name]['Draws'] = teams_draws.get(team_name, 0)
                all_teams_stats[team_name]['Goals Scored'] += stats.get('Goal', 0)
                all_teams_stats[team_name]['Passes'] += stats.get('Pass', 0)
                all_teams_stats[team_name]['Interceptions'] += stats.get('Interception', 0)
                all_teams_stats[team_name]['Shots On Target'] += stats.get('ShotOnTarget', 0)
                all_teams_stats[team_name]['Off Target'] += stats.get('OffTarget', 0)
                all_teams_stats[team_name]['Points'] = teams_points.get(team_name, 0)

    sorted_stats = sorted(all_teams_stats.items(), key=lambda x: x[1]['Points'], reverse=True)

    print(f"{'Team':<20}{'Matches Played':<15}{'Wins':<8}{'Draws':<8}{'Losses':<8}"
          f"{'Goals Scored':<15}{'Passes':<15}{'Interceptions':<15}"
          f"{'Shots On Target':<15}{'Off Target':<15}{'Points':<10}")
    print("-" * 140)
    for team, stats in sorted_stats:
        print(f"{team:<20}{stats['Matches Played']:<15}{stats['Wins']:<8}{stats['Draws']:<8}"
              f"{stats['Losses']:<8}{stats['Goals Scored']:<15}{stats['Passes']:<15}"
              f"{stats['Interceptions']:<15}{stats['Shots On Target']:<15}"
              f"{stats['Off Target']:<15}{stats['Points']:<10}")
        
    return sorted_stats


file_name_read = 'teams_and_substitutes.txt'

players_info = read_teams_info(file_name_read)

main_players = get_main_team(players_info)

results = play_matches(main_players)

sorted_stats = display_summary_table(results)

def save_summary_table_to_txt(sorted_stats):
    with open('summary_table.txt', 'w') as file:
        file.write(f"{'Team':<20}{'Matches Played':<15}{'Wins':<8}{'Draws':<8}{'Losses':<8}"
                   f"{'Goals Scored':<15}{'Passes':<15}{'Interceptions':<15}"
                   f"{'Shots On Target':<15}{'Off Target':<15}{'Points':<10}\n")
        file.write("-" * 140 + "\n")
        for team, stats in sorted_stats:
            file.write(f"{team:<20}{stats['Matches Played']:<15}{stats['Wins']:<8}{stats['Draws']:<8}"
                       f"{stats['Losses']:<8}{stats['Goals Scored']:<15}{stats['Passes']:<15}"
                       f"{stats['Interceptions']:<15}{stats['Shots On Target']:<15}"
                       f"{stats['Off Target']:<15}{stats['Points']:<10}\n")

save_summary_table_to_txt(sorted_stats)

save_match_stats_to_txt(results)

def play_matches_multiple_times(teams, num_simulations):
    all_match_results = []
    all_stats = [] 

    team_names = list(teams.keys())

    for _ in range(num_simulations):
        match_results = {}

        for i in range(len(team_names)):
            team_a = team_names[i]
            for j in range(i + 1, len(team_names)):
                team_b = team_names[j]
                match_result = simulate_match(teams[team_a], teams[team_b], team_a, team_b)
                match_results[(team_a, team_b)] = match_result

        all_match_results.append(match_results)

        stats = display_summary_table(match_results)
        all_stats.append(stats)

    with open('multiple_simulations_stats.txt', 'w') as file:
        file.write(f"{'Team':<20}{'Matches Played':<15}{'Wins':<8}{'Draws':<8}{'Losses':<8}"
                   f"{'Goals Scored':<15}{'Passes':<15}{'Interceptions':<15}"
                   f"{'Shots On Target':<15}{'Off Target':<15}{'Points':<10}\n")
        file.write("-" * 140 + "\n")

        for i, stats in enumerate(all_stats, start=1):
            file.write(f"Simulation {i} Statistics:\n")
            for team, team_stats in stats:
                file.write(f"{team:<20}{team_stats['Matches Played']:<15}{team_stats['Wins']:<8}"
                           f"{team_stats['Draws']:<8}{team_stats['Losses']:<8}"
                           f"{team_stats['Goals Scored']:<15}{team_stats['Passes']:<15}"
                           f"{team_stats['Interceptions']:<15}{team_stats['Shots On Target']:<15}"
                           f"{team_stats['Off Target']:<15}{team_stats['Points']:<10}\n")
            file.write("\n")

    return all_match_results


num_simulations = 5
all_match_results = play_matches_multiple_times(main_players, num_simulations)

def save_all_match_results_to_txt(all_match_results):
    with open('all_match_results.txt', 'w') as file:
        for idx, match_results in enumerate(all_match_results, start=1):
            for match, result in match_results.items():
                file.write(f"Match: {match[0]} vs {match[1]}\n")
                file.write(f"Score: {result['Team A']} - {result['Team B']}\n")
                file.write(f"{match[0]} stats:\n")
                for stat, value in result[match[0]].items():
                    if stat != 'Shot':
                        file.write(f"{match[0]} {stat}: {value}\n")
                file.write(f"{match[1]} stats:\n")
                for stat, value in result[match[1]].items():
                    if stat != 'Shot':
                        file.write(f"{match[1]} {stat}: {value}\n")
                file.write("-" * 50 + "\n")


save_all_match_results_to_txt(all_match_results)


