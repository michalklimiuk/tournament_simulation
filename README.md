# tournament_simulation

create_database.py - used to create x (16) teams with 20 players each and save results to teams_info.txt

read_data_create_teams_main.py - read results from create_database.py and choose main teams based on skill level; save results to teams_and_substitutes.txt

simulation_main.py - read results from read_data_create_teams_main and simulate a tournament where each teams plays with every other twice; simulation is based on probablility of each position and players' skills; 
save results and statistics to match_stats.txt and match_results.csv
