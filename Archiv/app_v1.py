import gradio as gr
from sklearn.ensemble import RandomForestRegressor
import numpy as np
import pandas as pd
import pickle
# TODO change the file to your own model.
model_filename = "random_forest_regression.pkl"

random_forest_model = RandomForestRegressor()
with open(model_filename, 'rb') as f:
    random_forest_model = pickle.load(f)

print('Number of features: ', random_forest_model.n_features_in_)
random_forest_model
# Load genre encodings from genre_mapping.csv
df_genres = pd.read_csv('genre_mapping.csv')

def search_genre_exact_match(search_string):
    result = df_genres[df_genres['Genre'] == search_string]
    return result

# Example usage
search_string = "Action, Adventure, Comedy, Science Fiction"
exact_match = search_genre_exact_match(search_string)
print(exact_match)
def count_crew_members(crew_string):
    # Split the crew string by commas and count the resulting elements
    crew_members = crew_string.split(',')
    return len(crew_members)

# Example usage
crew_string = "Director, Producer, Writer, Cinematographer"
crew_count = count_crew_members(crew_string)
print("Number of crew members:", crew_count)
def count_overview_words(overview_string):
    # Split the overview string by spaces and count the resulting elements
    words = overview_string.split()
    return len(words)

# Example usage
overview_string = "An action-packed adventure."
overview_word_count = count_overview_words(overview_string)
print("Number of words in the overview:", overview_word_count)
def convert_date_format(date_string):
    # Split the input string by dots
    day, month, year = date_string.split('.')
    # Rearrange and return the date in YYYYMMDD format
    return int(year + month + day)

# Example usage
date_string = "01.01.2023"
converted_date = convert_date_format(date_string)
print("Converted date:", converted_date)
# Define the core prediction function
def predict_movie(budget, genre_search_string, overview_string, crew_string, release_date_string):
    # Get the genre_code using the search_genre_exact_match function
    genre_match = search_genre_exact_match(genre_search_string)
    if genre_match.empty:
        return -1  # Return -1 if no matching genre is found
    genre_code = genre_match.iloc[0]['Code']
    
    # Get the crew_code_sum using the count_crew_members function
    crew_code_sum = count_crew_members(crew_string)
    
    # Get the overview_word_count using the count_overview_words function
    overview_word_count = count_overview_words(overview_string)
    
    # Get the release_date_int using the convert_date_format function
    release_date_int = convert_date_format(release_date_string)

    # Get Crew Budget
    budget_crew = budget / crew_code_sum if crew_code_sum > 0 else 0
    
    # Create a DataFrame with the input features
    input_data = pd.DataFrame([{
        'budget': budget,
        'genre_code': genre_code,
        'overview_word_count': overview_word_count,
        'crew_code_sum': crew_code_sum,
        'release_date_int': release_date_int,
        'budget_crew': budget_crew
    }])
    
    # Make the prediction using the random forest model
    prediction = random_forest_model.predict(input_data)
    return np.round(prediction[0], 0)
predict_movie(30000000000, 'Action', 'A very Action packed movie', 'Director, Producer, Writer, Cinematographer', '01.01.2023')
# Define a function to determine if the movie is a flop or hit
def determine_flop_or_hit(budget, genre_search_string, overview_string, crew_string, release_date_string):
    # Predict the revenue using the predict_movie function
    predicted_revenue = predict_movie(budget, genre_search_string, overview_string, crew_string, release_date_string)
    
    # Determine if the movie is a flop or hit
    if predicted_revenue - budget > 0:
        return "Hit"
    else:
        return "Flop"

# Create the Gradio interface
iface = gr.Interface(
    fn=lambda budget, genre_search_string, overview_string, crew_string, release_date_string: (
        predict_movie(budget, genre_search_string, overview_string, crew_string, release_date_string),
        determine_flop_or_hit(budget, genre_search_string, overview_string, crew_string, release_date_string)
    ),
    inputs=[
        gr.Number(label="Budget"),
        gr.Textbox(label="Genre Search String"),
        gr.Textbox(label="Overview String"),
        gr.Textbox(label="Crew String"),
        gr.Textbox(label="Release Date String (DD.MM.YYYY)")
    ],
    outputs=[
        gr.Number(label="Predicted Revenue"),
        gr.Textbox(label="Flop or Hit")
    ],
    examples=[
        [30000000000, "Action", "A very Action packed movie", "Director, Producer, Writer, Cinematographer", "01.01.2023"],
        [50000000, "Comedy", "A hilarious comedy movie", "Director, Writer", "15.06.2022"]
    ]
)

iface.launch()