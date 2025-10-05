from flask import Flask, render_template, request
import yfinance as yf
import matplotlib.pyplot as plt
import io, base64
from prediction import predict_stock

app = Flask(__name__)

# Predefined stocks
STOCKS = {
    "Tesla (TSLA)": "TSLA",
    "Apple (AAPL)": "AAPL",
    "Reliance (RELIANCE.NS)": "RELIANCE.NS",
    "Infosys (INFY.NS)": "INFY.NS",
    "TCS (TCS.NS)": "TCS.NS"
}

def plot_stock(df):
    """Generate stock price trend graph and return base64 string"""
    plt.figure(figsize=(10,5))
    plt.plot(df.index, df["Close"], label="Closing Price", color="blue")
    plt.plot(df.index, df["Open"], label="Opening Price", color="orange")
    plt.xlabel("Date")
    plt.ylabel("Price")
    plt.title("Stock Price Trend")
    plt.legend()
    plt.grid(True)

    buf = io.BytesIO()
    plt.savefig(buf, format="png", bbox_inches="tight")
    buf.seek(0)
    return base64.b64encode(buf.getvalue()).decode("utf-8")

@app.route("/", methods=["GET", "POST"])
def index():
    data = None
    img = None
    prediction = None
    ticker = None

    if request.method == "POST":
        ticker = request.form["ticker"]
        start = request.form["start"]
        end = request.form["end"]

        # Fetch stock data
        df = yf.download(ticker, start=start, end=end)

        if not df.empty:
            # Show last 100 rows as Bootstrap table
            data = df.tail(100).to_html(classes="table table-striped table-bordered")
            img = plot_stock(df)

            # Predict next-day closing price
            prediction = predict_stock(df)
        else:
            data = "❌ No data available for this selection."

    return render_template("index.html", stocks=STOCKS, data=data, img=img, prediction=prediction, ticker=ticker)

if __name__ == "__main__":
    app.run(debug=True)
