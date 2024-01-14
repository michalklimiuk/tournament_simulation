# tournament_simulation - file explanation

1_create_database.py - used to create x (16) teams with 20 players each and save results to teams_info.txt

2_create_main_teams_.py - read results from teams_info.txt and choose main teams based on skill level; save results to teams_and_substitutes.txt

3_single_simulation.py - read results from teams_and_substitutes.txt, get main squad for each team with the best players and simulate a tournament where each teams plays with every other twice - round robin scheduling; simulation is based on probablility of each position and players' skills; save results and statistics to match_stats.txt and summary_table.txt

4-multiple-simulations.py - improved 3_single_simulation.py; simulation performed x (input) times and summarised output is saved to all_match_results.txt and multiple_simulations_stats.txt

5_1-MLPRegressor_predict.py - used to predict winner of next tournament based of AI and Multi-layer Perceptron Regressor

5_2-Sequential_predict.py - used to predict winner of next tournament based of AI and Sequential model

xx_simulations_stats.txt - files used to evaluate existing AI models

6_MLPRegressor_enhanced - improved version of the best working AI model
