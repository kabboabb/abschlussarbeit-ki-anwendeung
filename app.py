import gradio as gr
from sklearn.ensemble import RandomForestRegressor
import numpy as np
import pandas as pd
import pickle
# TODO change the file to your own model.
model_filename = "random_forest_regression_updated_v2.pkl"

random_forest_model = RandomForestRegressor()
with open(model_filename, 'rb') as f:
    random_forest_model = pickle.load(f)

print('Number of features: ', random_forest_model.n_features_in_)
random_forest_model
def count_crew_members(crew_string):
    # Split the crew string by commas and count the resulting elements
    crew_members = crew_string.split(',')
    return len(crew_members)

# Example usage
crew_string = "Director, Producer, Writer, Cinematographer"
crew_count = count_crew_members(crew_string)
print("Number of crew members:", crew_count)
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
def predict_movie(budget, crew_string, release_date_string, duration):

    # Get the crew_code_sum using the count_crew_members function
    crew_code_sum = count_crew_members(crew_string)
    
    # Get the release_date_int using the convert_date_format function
    release_date_int = convert_date_format(release_date_string)

    # Get Crew Budget
    budget_crew = budget / crew_code_sum if crew_code_sum > 0 else 0

    # Calculate the budget per minute
    budget_per_minute = budget / duration if duration > 0 else 0
    
    # Create a DataFrame with the input features
    input_data = pd.DataFrame([{
        'budget': budget,
        'release_date_int': release_date_int,
        'budget_crew': budget_crew,
        'duration': duration,
        'budget_per_minute': budget_per_minute
    }])
    
    # Make the prediction using the random forest model
    prediction = random_forest_model.predict(input_data)
    return np.round(prediction[0], 0)
predict_movie(30000000000, 'Director, Producer, Writer, Cinematographer', '01.01.2023', 120)
def determine_flop_or_hit(budget, crew_string, release_date_string, duration):

    # Predict the revenue using the predict_movie function
    predicted_revenue = predict_movie(budget, crew_string, release_date_string, duration)
    
    # Determine if the movie is a flop or hit
    if predicted_revenue - budget > 0:
        return "Hit"
    else:
        return "Flop"

# Create the Gradio interface
iface = gr.Interface(
    fn=lambda budget, crew_string, release_date_string, duration: (
        predict_movie(budget, crew_string, release_date_string, duration),
        determine_flop_or_hit(budget, crew_string, release_date_string, duration)
    ),
    inputs=[
        gr.Number(label="Budget"),
        gr.Textbox(label="Crew String"),
        gr.Textbox(label="Release Date String (DD.MM.YYYY)"),
        gr.Number(label="Duration (in minutes)")
    ],
    outputs=[
        gr.Number(label="Predicted Revenue"),
        gr.Textbox(label="Flop or Hit")
    ],
    examples=[
        [30000000, "Jason Stattham, Chris Pratt, Scarlett Johansson", "01.01.2023", 120],
        [50000000, "Tom Holland, Chris Evans", "15.06.2022", 90],
    ]
)

iface.launch()