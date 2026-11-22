# Sport Car Price Analysis

**Live Streamlit app:** Add your deployed Streamlit URL here after deployment.

## Project overview
An exploratory data analysis and interactive dashboard exploring sports-car manufacturers, specifications, acceleration, and listed prices.

## Files
- `sport_car_price.csv` — supplied source dataset
- `sport_car_eda.ipynb` — complete EDA notebook
- `app.py` — Streamlit dashboard
- `requirements.txt` — Python dependencies
- `.gitignore` — files excluded from Git

## Dataset
The source file contains 1,007 rows and 8 columns. Each row represents a sports-car model/specification record.

## Data preparation
- Removed exact duplicate rows.
- Converted numeric-looking text to numeric values.
- Derived an `Engine Type` label from engine descriptions.
- Filled remaining missing numeric values with each column's median.
- Retained IQR outliers because unusually expensive or powerful cars may be genuine specialist models.

The notebook documents the cleaning and analysis in detail. Some source entries use shorthand or mixed descriptions (for example, electric engine labels and plus-suffixed horsepower); numeric extraction is a simplifying assumption and should be disclosed during the presentation.

## Run locally
```bash
pip install -r requirements.txt
streamlit run app.py
```

## Deploy
1. Push this public repository to GitHub.
2. Open https://share.streamlit.io/
3. Sign in with GitHub and choose this repository.
4. Set the main file path to `app.py`.
5. Deploy, then paste the live URL at the top of this README.

## Notebook
Open `sport_car_eda.ipynb` in Google Colab or Jupyter. Upload `sport_car_price.csv` to the same working folder before running all cells.
