# Movie Revenue Prediction

## Project Description
Predicts revenue of a Movie an looks if it will be a hit or a flop. 

## Results
The model is still underfitting, incorporating different types of features from alternative data sources, as well as increasing the overall data volume may help improve performance. Since most of the available data is textual and needs to be converted into numerical form, and given that there are only 3,632 usable data points with varying budgets and revenues, expanding and enriching the dataset could be crucial for achieving better model accuracy and generalization. 

### Name & URL
| Name          | URL |
|--------------|----|
| Huggingface  | [Huggingface Space](https://huggingface.co/spaces/kabboabb/movie-revenue-hit-or-flop-prediction) |
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

## Model Training
### Amount of Data
- Total of 2344 apartments

### Data Splitting Method (Train/Validation/Test)
- First 80/20 Train/Test split then changed to cross-validation using 5 splits due to data limitations.

### Performance

| It. Nr | Model | Performance | Features | Description |
|--------|--------|-------------|------------|---------------|
| 1 | Linear Regression | Train: 0.56, Test: 0.42, <br>Train RMSE: 831, Test RMSE: 974 | `rooms, area, pop, pop_dens, frg_pct, emp, tax_income` | Underfitting |
| 2 | Random Forest | Train: 0.88, Test: 0.44, <br>Train RMSE: 428, Test RMSE: 964 | Same as It. 1 | Overfitting |
| 3 | Random Forest | Mean RMSE: -673.8 | Same as It. 1 | Underfitting |
| 4 | Random Forest | Mean RMSE: -136.2 | Added `room_per_m2, price_per_m2` | Used price_per_m2, making it unrealistic |
| 5 | Random Forest | Mean RMSE: -661.0 | Added `luxurious, temporary, furnished` | Underfitting |
| 6 | Random Forest | Mean RMSE: -660.4 | Added `area_cat_encoded` | Underfitting |
| 7 | Random Forest | Mean RMSE: -617.0 | `['rooms', 'area', 'pop', 'pop_dens', 'frg_pct', 'emp', 'tax_income', 'room_per_m2', 'luxurious', 'temporary', 'furnished', 'area_cat_ecoded', '(LUXURIÖS)',  '(POOL)', '(SEESICHT)',  '(EXKLUSIV)', '(ATTIKA)', '(LOFT)', 'Kreis 6', 'Kreis 11', 'Kreis 12', 'Kreis 10', 'Kreis 4', 'Kreis 1', 'Kreis 9', 'Kreis 5', 'Kreis 7', 'Kreis 3', 'Kreis 2', 'Kreis 8']` | Added one-hot encoded features for luxury types and Zurich districts <br> Underfitting, incorrect city Zurich data |
| 8 | Random Forest | Mean RMSE: -614.2 | Same as It. 7 | Fixed `pop` and `pop_dens` for Zurich city |
| 9 | Random Forest | Mean RMSE: -617.6 | `['rooms', 'area', 'pop', 'pop_dens', 'frg_pct', 'emp', 'tax_income', 'room_per_m2', 'luxurious', 'temporary', 'furnished', 'area_cat_ecoded', 'zurich_city']` | Reduced features after importance analysis <br> Still underfitting (see (#fig1)
| 10 | Random Forest | Mean RMSE: -612.6 | Same as It. 9 | Used GridSearch for best parameters |
| 11 | Random Forest | Train: 0.94, Test: 0.65, Train RMSE: 255, Test RMSE: 638 | Same as It. 9 | Changed train/test split, resulted in overfitting |

## References
![Feature Importance](doc/feature_importance.png "Feature Importance")<span id="fig1"></span>


