# Movie Rating Prediction App

A Flask web application that predicts IMDb movie ratings using a trained ElasticNet regression model.

## Project Structure

```
movie_rating_app/
├── api.py                  # Flask server with prediction endpoint
├── assets_data_prep.py     # Data preparation function
├── trained_model.pkl       # Trained ElasticNet model
├── requirements.txt        # Required Python packages
├── README.md               # This file
└── templates/
    └── index.html          # Web interface
```

## Installation

1. Clone the repository:

```bash
git clone <repository-url>
cd movie_rating_app
```

2. Create and activate a virtual environment:

```bash
python -m venv venv

# Windows
venv\Scripts\activate
```

3. Install the required packages:

```bash
pip install -r requirements.txt
```

## Running the App

```
python api.py
```

Then open your browser and go to: `http://localhost:5000`

## How to Use

1. Enter the movie details in the form and click **Predict Rating**
2. The predicted IMDb rating (out of 10) will appear below the form

## Input Fields

| Field | Description | Expected Value |
|-------|-------------|----------------|
| Start Year | Year the movie was released | 1888–2026 |
| Runtime Minutes | Duration of the movie in minutes | Positive number, e.g. 120 |
| Genres | Comma-separated list of genres | Text, e.g. Drama, Comedy |
| Language | The movie's language | Text, e.g. English. If unknown, enter `Not Found` |
| Country | The country of production | Text, e.g. United States. If unknown, enter `Not Found` |


## Expected Ranges

- `startYear`: number between 1888 and 2026
- `runtimeMinutes`: positive number
- `genres`: comma-separated genres, for example: Drama, Comedy, Action
- `Language`: text, for example: English. If unknown, enter `Not Found`
- `Country`: text, for example: United States. If unknown, enter `Not Found`


## API

**POST /predict**

Accepts JSON input and returns a predicted rating.

Request example:
```json
{
  "startYear": 2020,
  "runtimeMinutes": 120,
  "genres": "Drama, Comedy",
  "Language": "English",
  "Country": "United States"
}
```

Response example:
```json
{
  "predicted_rating": 6.85
}
```

Error responses:
- `400` – Missing or invalid input fields
- `500` – Internal server error

## Authors

- זוהר קולפ — 322435918
- רוני פחימה — 212009260
