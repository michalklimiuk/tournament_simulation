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
                position, skill = line.split(', ')
                position = position.split(': ')[1]
                skill = int(skill.split(': ')[1])
                player_data[current_country][position].append(skill)

    return player_data

def display_results(player_info):
    for country, positions in player_info.items():
        print(f"Players of {country}:")
        for position, skills in positions.items():
            for skill in skills:
                print(f"Position: {position.capitalize()}, Skill: {skill}")
        print('-' * 30)

def display_players_by_position(players_info, country, position):
    if country in players_info and position in players_info[country]:
        print(f"Players of {country} as {position.capitalize()}s:")
        for skill in players_info[country][position]:
            print(f"Skill: {skill}")
    else:
        print("Country or position not found!")

def create_teams_with_attributes(players_info):
    teams = {}
    for country, positions in players_info.items():
        team = {'goalkeeper': [], 'defender': [], 'midfielder': [], 'striker': []}
        for position, skills in positions.items():
            skills.sort(reverse=True)  # Sortowanie umiejętności malejąco
            if position == 'goalkeeper':
                team[position] = [f"{skill}, M" for skill in skills[:1]] + [f"{skill}, S" for skill in skills[1:]] if skills else []
            elif position == 'defender':
                team[position] = [f"{skill}, M" for skill in skills[:4]] + [f"{skill}, S" for skill in skills[4:]] if len(skills) >= 4 else [f"{skill}, M" for skill in skills] + ['S']
            elif position == 'midfielder':
                team[position] = [f"{skill}, M" for skill in skills[:3]] + [f"{skill}, S" for skill in skills[3:]] if len(skills) >= 3 else [f"{skill}, M" for skill in skills] + ['S']
            elif position == 'striker':
                team[position] = [f"{skill}, M" for skill in skills[:3]] + [f"{skill}, S" for skill in skills[3:]] if len(skills) >= 3 else [f"{skill}, M" for skill in skills] + ['S']
        teams[country] = team
    return teams

def display_players_with_attributes(players_info, country):
    if country in players_info:
        print(f"Players of {country}:")
        for position, skills in players_info[country].items():
            for skill in skills:
                print(f"Position: {position.capitalize()}, Skill: {skill}")
    else:
        print("Country not found!")

file_name_read = 'teams_info.txt'
players_info = read_teams_info(file_name_read)



# ZMIANA: Zespoły i zmiennicy są teraz tworzone przy użyciu funkcji create_teams_with_attributes,
# więc nie potrzebujemy już funkcji create_substitutes.

output_file = "teams_and_substitutes.txt"

display_results(players_info)
created_teams = create_teams_with_attributes(players_info)
display_results(created_teams)

def save_teams_to_file_with_attributes(created_teams, file_name):
    with open(file_name, 'w') as txt_file:
        for i, team_name in enumerate(created_teams):
            team_players = created_teams[team_name]
            txt_file.write(f"Players of {team_name}:\n")
            for position, players in team_players.items():
                for player in players:
                    txt_file.write(f"Position: {position}, Skill: {player}\n")
            txt_file.write('-' * 30 + '\n')

save_teams_to_file_with_attributes(created_teams, output_file)



