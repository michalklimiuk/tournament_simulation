# odczyt drużyn z pliku i odfiltrowanie zawodników głównych

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

file_name_read = 'teams_and_substitutes.txt'
players_info = read_teams_info(file_name_read)
# display_results(players_info)

main_players = get_main_team(players_info)

print(main_players)
# display_results(main_players)



import random

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

import random

def simulate_match(team_a, team_b, team_a_name, team_b_name):
    score_team_a = 0
    score_team_b = 0
    positions = ['goalkeeper', 'defender', 'midfielder', 'striker']
    team_with_ball = random.choice([team_a, team_b])

    # Inicjalizacja statystyk dla obu drużyn
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
    match_results = {}  # Słownik przechowujący wyniki meczów

    for i in range(len(team_names)):
        team_a = team_names[i]
        for j in range(i + 1, len(team_names)):
            team_b = team_names[j]
            print(f"Match between {team_a} and {team_b}")
            match_result = simulate_match(teams[team_a], teams[team_b], team_a, team_b)
            match_results[(team_a, team_b)] = match_result

    return match_results

play_matches(main_players)

import csv

def save_match_results_to_csv(results):
    with open('match_results.csv', mode='w', newline='') as csv_file:
        fieldnames = ['Team A', 'Team B', 'Team A Score', 'Team B Score']
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)

        writer.writeheader()
        for match, result in results.items():
            writer.writerow({
                'Team A': match[0],
                'Team B': match[1],
                'Team A Score': result['Team A'],
                'Team B Score': result['Team B']
            })

def save_match_stats_to_txt(results):
    with open('match_stats.txt', 'w') as txt_file:
        for match, result in results.items():
            txt_file.write(f"Match: {match[0]} vs {match[1]}\n")
            txt_file.write(f"Score: {result['Team A']} - {result['Team B']}\n")
            txt_file.write(f"{match[0]} stats: {result[match[0]]}\n")
            txt_file.write(f"{match[1]} stats: {result[match[1]]}\n")
            txt_file.write("-" * 50 + "\n")


# Przykład użycia:
results = play_matches(main_players)

save_match_results_to_csv(results)
save_match_stats_to_txt(results)
# for match, result in results.items():
#     print(f"Result for {match[0]} vs {match[1]}: {result['Team A']} - {result['Team B']}")

# Wywołanie funkcji z danymi drużyn
# play_matches(main_players)

# TEST POJEDYNCZEGO MECZU -------------------------------------------------------------------
# team_a_players = {
#     'goalkeeper': [(85, 'M')],
#     'defender': [(80, 'M'), (77, 'M'), (76, 'M'), (72, 'M')],
#     'midfielder': [(89, 'M'), (76, 'M'), (73, 'M')],
#     'striker': [(88, 'M'), (88, 'M'), (71, 'M')]
# }

# team_b_players = {
#     'goalkeeper': [(89, 'M')],
#     'defender': [(84, 'M'), (79, 'M'), (78, 'M'), (69, 'M')],
#     'midfielder': [(87, 'M'), (83, 'M'), (83, 'M')],
#     'striker': [(84, 'M'), (79, 'M'), (77, 'M')]
# }

# def play_match(team_a_players, team_b_players):
#     print("Match between Team A and Team B")
#     simulate_match(team_a_players, team_b_players)

# # Wywołanie funkcji do symulacji meczu
# play_match(team_a_players, team_b_players)
