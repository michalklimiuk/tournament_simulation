import random

countries = ['Albania', 'Algeria', 'Argentina', 'Armenia', 'Australia', 'Austria', 'Azerbaijan', 'Belarus', 'Belgium', 'Bosnia and Herzegovina', 'Brazil', 'Bulgaria', 'Cameroon', 
            'Canada', 'Chile', 'Colombia', 'Costa Rica', "Côte d'Ivoire", 'Croatia', 'Czech Republic', 'Denmark', 'Ecuador', 'Finland', 'France', 'Georgia', 'Germany', 'Ghana', 
            'Greece', 'Hungary', 'Iceland', 'Ireland', 'Italy', 'Japan', 'Kazakhstan', 'Kenya', "Korea, Democratic People's Republic of", 'Latvia', 
            'Lithuania', 'Luxembourg', 'Macedonia, Republic of', 'Mexico', 'Moldova, Republic of', 'Montenegro', 'Morocco', 'Netherlands', 'Nigeria', 'Norway', 'Paraguay', 'Peru', 'Poland',
            'Portugal', 'Qatar', 'Romania', 'San Marino', 'Saudi Arabia', 'Senegal', 'Serbia', 'Slovakia', 'Slovenia', 'South Africa', 
            'Spain', 'Sweden', 'Switzerland', 'Tunisia', 'Turkey', 'Ukraine', 'United Kingdom', 'United States', 'Uruguay', 'Venezuela, Bolivarian Republic of', 'Wales']

num_teams = 16
teams = set()   # zamiana w set aby uniknąć powtórzeń drużyn



class Player:
    def __init__(self, position, skill):
        self.position = position
        if 60 <= skill <= 90:
            self.skill = skill
        else:
            raise ValueError("Values should be 60 - 90")

def generate_team_players():
    team = []  
    for _ in range(2): 
        goalkeeper = Player(position='goalkeeper', skill=random.randint(60, 90))
        team.append(goalkeeper)
    for _ in range(7):  
        defender = Player(position='defender', skill=random.randint(60, 90))
        team.append(defender)
    for _ in range(6):  
        midfielder = Player(position='midfielder', skill=random.randint(60, 90))
        team.append(midfielder)
    for _ in range(5):  
        striker = Player(position='striker', skill=random.randint(60, 90))
        team.append(striker)
    
    return team

def display_team_players(team_name, team):
    print(f"Players of {team_name}:")
    for player in team:
        print(f"Position: {player.position}, Skill: {player.skill}")

while len(teams) < num_teams:
    new_country = random.choice(countries)
    teams.add(new_country)

teams = list(teams)

for i, team_name in enumerate(teams):
    team_players = generate_team_players()
    display_team_players(team_name, team_players)
    print('-' * 30)  # separator

file_txt = "teams_info.txt"

with open(file_txt, 'w') as txt_file:
    for i, team_name in enumerate(teams):
        team_players = generate_team_players()
        txt_file.write(f"Players of {team_name}:\n")
        for player in team_players:
            txt_file.write(f"Position: {player.position}, Skill: {player.skill}\n")
        txt_file.write('-' * 30 + '\n')


