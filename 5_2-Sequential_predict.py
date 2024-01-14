import numpy as np
from sklearn.model_selection import train_test_split
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense
from sklearn.metrics import mean_squared_error
import time

file_name = '999_simulations_stats.txt'

def read_summary_table(file_name):
    with open(file_name, 'r') as file:
        lines = file.readlines()[2:]
        data = []

        labels = [
            "Team", "Matches Played", "Wins", "Draws", "Losses", "Goals Scored",
            "Passes", "Interceptions", "Shots On Target", "Off Target", "Points"
        ]
        data.append(labels)

        for line in lines:
            columns = line.strip().split()

            if len(columns) >= 11:
                country_name = ' '.join(columns[:-10])

                team_stats = [
                    country_name,
                    int(columns[-10]), int(columns[-9]), int(columns[-8]), int(columns[-7]),
                    int(columns[-6]), int(columns[-5]), int(columns[-4]), int(columns[-3]),
                    int(columns[-2]), int(columns[-1])
                ]

                data.append(team_stats)

    return data

t1 = time.time()
table_data = read_summary_table(file_name)

# przetworzenie danych do sieci neuronowej
X = np.array([row[1:-1] for row in table_data[1:]])
y = np.array([row[-1] for row in table_data[1:]])

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# stworzenie modelu sieci neuronowej
model = Sequential()
model.add(Dense(64, input_shape=(X_train.shape[1],), activation='relu'))
model.add(Dense(32, activation='relu'))
model.add(Dense(1, activation='linear'))

model.compile(optimizer='adam', loss='mean_squared_error', metrics=['mae'])

# trenowanie modelu
history = model.fit(X_train, y_train, epochs=100, batch_size=32, validation_split=0.1)
y_pred = model.predict(X)
mse = mean_squared_error(y, y_pred)

# ocena modelu
loss, mae = model.evaluate(X_test, y_test)
print(f"Mean Absolute Error: {mae}")


predicted_points = model.predict(X_test)
predicted_points_rounded = np.round(predicted_points).astype(int)

predicted_results = []
for i in range(len(predicted_points_rounded)):
    country_stats = list(X_test[i])
    country_stats.append(predicted_points_rounded[i])  
    country_stats.insert(0, table_data[i + 1][0])  
    predicted_results.append(country_stats)

predicted_results.sort(key=lambda x: x[-1], reverse=True)

predicted_table = [table_data[0]] 
team_names = set() 

for row in predicted_results:
    if row[0] not in team_names and len(predicted_table) <= 16:
        predicted_table.append(row[0:11])  
        team_names.add(row[0])  

print("\nPredicted Tournament Table:")
print("-" * 115)

predicted_table = sorted(predicted_table[1:], key=lambda x: x[-1], reverse=True)
predicted_table.insert(0, table_data[0]) 

for row in predicted_table:
    row = [str(item) for item in row]
    print(f"{row[0]:<20}{row[1]:<15}{row[2]:<8}{row[3]:<8}{row[4]:<8}{row[5]:<15}"
          f"{row[6]:<15}{row[7]:<15}{row[8]:<15}{row[9]:<15}{row[10]:<10}")

t2 = time.time()
end_time = t2 - t1
print(f'Time taken: {end_time} seconds')
print(f'Mean Squared Error (MSE): {mse}')