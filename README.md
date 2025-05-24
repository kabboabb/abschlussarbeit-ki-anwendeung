# Movie Revenue Prediction

## Project Description
Predicts revenue of a Movie an looks if it will be a hit or a flop. 

## Results
The model is still overfitting; incorporating different types of features from alternative data sources, as well as increasing the overall data volume, may help improve performance. However, with each new feature derived from a different dataset, the number of usable data points tends to drop due to incomplete or missing entries. Since most of the available data is textual and requires conversion into numerical form, and given that there are only 1,680 usable data points with varying budgets and revenues, expanding and enriching the dataset could be crucial for achieving better model accuracy and generalization.


### Name & URL
| Name          | URL |
|--------------|----|
| Huggingface  | [Huggingface Space](https://huggingface.co/spaces/kabboabb/abschluss-movie-prediction) |
| Code         | [GitHub Repository](https://github.com/kabboabb/abschlussarbeit-ki-anwendeung) |

## Data Sources and Features Used Per Source
| Data Source | Features |
|-------------|----------|
| [Kaggle IMDb Movies dataset from 2000 - 2020](https://www.kaggle.com/datasets/chenyanglim/imdb-v2) | duration |
| [Kaggle Movie Budgets And Revenues](https://www.stadt-zuerich.ch/geodaten/download/Statistische_Quartiere) | Relese Date, Movie Name, Budget, Domestic Gross, World Wide Gross |
| [Kaggle IMDB movies dataset](https://www.kaggle.com/datasets/ashpalsingh1525/imdb-movies-dataset) | Genre, Overview, Crew|

## Features Created
|genre_code| Given each Genre cunstruct a Code|
|overview_word_count| Counted How Long the overview is|
|'crew_code_sum'|Cunted how many cast members there are|
|release_date_int| turned the date in to a number|
|budget_crew| budget / crew_count|
|budget_per_minute| budget/duration|

## Model Training
### Amount of Data
- Total of 1680 movies

### Data Splitting Method (Train/Validation/Test)
- First 80/20 Train/Test split then changed to cross-validation using 5 splits due to data limitations.

### Performance

| It. Nr | Model                                                            | Performance                                                                                                                     | Features                                                                                                               | Description                                        |
| ------ | ---------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------- | -------------------------------------------------- |
| 1      | Linear Regression                                                | Train score: 0.3974, Test score: 0.4169<br>Train RMSE: 186 082 236, Test RMSE: 181 925 341<br>Train R²: 0.3974, Test R²: 0.4169 | `score, budget`                                                                                                        | Underfitting (low explanatory power)               |
| 1      | Random Forest                                                    | Train score: 0.7386, Test score: 0.2983<br>Train RMSE: 122 568 991, Test RMSE: 199 568 440<br>Train R²: 0.7386, Test R²: 0.2983 | `score, budget`                                                                                                        | Overfitting (high train vs low test)               |
| 2      | Linear Regression                                                | CV Mean RMSE: 200 295 902                                                                                                       | `score, budget, country_code, genre_code, crew_count`                                                                  | Still underfitting, high error                     |
| 2      | Random Forest                                                    | CV Mean RMSE: 185 295 928                                                                                                       | `score, budget, country_code, genre_code, crew_count`                                                                  | Improved over LR but moderate error                |
| 3      | Linear Regression                                                | CV Mean RMSE: 196 190 560                                                                                                       | `budget, country_code, genre_code, crew_count, overview_word_count, title_word_count, crew_code_sum, release_date_int` | Slight improvement over it. 2                      |
| 3      | Random Forest                                                    | CV Mean RMSE: 188 045 871                                                                                                       | `budget, country_code, genre_code, crew_count, overview_word_count, title_word_count, crew_code_sum, release_date_int` | Slight improvement over it. 2 RF                   |
| 4      | Random Forest                                                    | CV Mean RMSE: 234 907 294<br>R² (all): 0.8194, R² (train): 0.8199, R² (test): 0.4769                                            | `budget, genre_code, overview_word_count, crew_code_sum, release_date_int, budget_crew, duration`                      | Overfitting (train/test gap)                       |
| 5      | Random Forest                                                    | CV Mean RMSE: 233 301 108<br>R² (all): 0.8209, R² (train): 0.8208, R² (test): 0.5250                                            | `budget, genre_code, overview_word_count, crew_code_sum, release_date_int, budget_crew, duration, budget_per_minute`   | Better test performance but still some overfitting |
| 6      | Random Forest (tuned: min\_samples\_split=12, n\_estimators=500) | CV Mean RMSE: 220 086 708<br>R² (all): 0.7279, R² (train): 0.7050, R² (test): 0.5681                                            | `budget, genre_code, overview_word_count, crew_code_sum, release_date_int, budget_crew, duration, budget_per_minute`   | Hyperparameter tuning → improved generalization    |


## References
![Feature Importance](feature_importance.png "Feature Importance")<span id="fig1"></span>


