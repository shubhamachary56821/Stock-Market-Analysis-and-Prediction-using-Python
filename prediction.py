import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression

def predict_stock(df):
    """
    Takes a DataFrame with 'Date' index & 'Close' prices.
    Returns predicted next-day closing price.
    """
    df = df.reset_index()
    df['Date'] = pd.to_datetime(df['Date'])
    df['Days'] = (df['Date'] - df['Date'].min()).dt.days

    X = df[['Days']]
    y = df['Close']

    if len(X) < 2:  # Not enough data
        return None

    model = LinearRegression()
    model.fit(X, y)

    next_day = np.array([[df['Days'].max() + 1]])
    prediction = model.predict(next_day)

    # ✅ Extract the first scalar from numpy array
    return round(float(prediction[0]), 2)
