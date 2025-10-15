# from flask import Flask, render_template, request, redirect, url_for, session
# import yfinance as yf
# import matplotlib.pyplot as plt
# import io, base64
# from prediction import predict_stock
# import os

# # When running on Vercel, Flask might not automatically find the template path,
# # so we explicitly define it relative to this file
# app = Flask(__name__, template_folder="../templates")

# app.secret_key = os.environ.get("SECRET_KEY", "supersecretkey")  # use env var if available

# # ------------------------------
# # 📊 Predefined Stocks
# # ------------------------------
# STOCKS = {
#     "Tesla (TSLA)": "TSLA",
#     "Tata Motors (TATAMOTORS.NS)": "TATAMOTORS.NS",
#     "Mahindra & Mahindra (M&M.NS)": "M&M.NS",
#     "Maruti Suzuki (MARUTI.NS)": "MARUTI.NS",
#     "Apple (AAPL)": "AAPL",
#     "Microsoft (MSFT)": "MSFT",
#     "Google (GOOG)": "GOOG",
#     "Amazon (AMZN)": "AMZN",
#     "NVIDIA (NVDA)": "NVDA",
#     "Meta (META)": "META",
#     "Infosys (INFY.NS)": "INFY.NS",
#     "TCS (TCS.NS)": "TCS.NS",
#     "Wipro (WIPRO.NS)": "WIPRO.NS",
#     "HCL Technologies (HCLTECH.NS)": "HCLTECH.NS",
#     "HDFC Bank (HDFCBANK.NS)": "HDFCBANK.NS",
#     "ICICI Bank (ICICIBANK.NS)": "ICICIBANK.NS",
#     "State Bank of India (SBIN.NS)": "SBIN.NS",
#     "Axis Bank (AXISBANK.NS)": "AXISBANK.NS",
#     "Kotak Mahindra Bank (KOTAKBANK.NS)": "KOTAKBANK.NS",
#     "JP Morgan Chase (JPM)": "JPM",
#     "Goldman Sachs (GS)": "GS",
#     "Reliance Industries (RELIANCE.NS)": "RELIANCE.NS",
#     "ONGC (ONGC.NS)": "ONGC.NS",
#     "Indian Oil (IOC.NS)": "IOC.NS",
#     "ExxonMobil (XOM)": "XOM",
#     "Chevron (CVX)": "CVX",
#     "Hindustan Unilever (HINDUNILVR.NS)": "HINDUNILVR.NS",
#     "Nestle India (NESTLEIND.NS)": "NESTLEIND.NS",
#     "ITC (ITC.NS)": "ITC.NS",
#     "Procter & Gamble (PG)": "PG",
#     "Coca-Cola (KO)": "KO",
#     "Larsen & Toubro (LT.NS)": "LT.NS",
#     "Adani Enterprises (ADANIENT.NS)": "ADANIENT.NS",
#     "Adani Ports (ADANIPORTS.NS)": "ADANIPORTS.NS",
#     "General Electric (GE)": "GE",
#     "Caterpillar (CAT)": "CAT",
#     "Sun Pharma (SUNPHARMA.NS)": "SUNPHARMA.NS",
#     "Dr. Reddy's Labs (DRREDDY.NS)": "DRREDDY.NS",
#     "Pfizer (PFE)": "PFE",
#     "Johnson & Johnson (JNJ)": "JNJ",
#     "Cipla (CIPLA.NS)": "CIPLA.NS",
#     "IndiGo (INTERGLOBE.NS)": "INDIGO.NS",
#     "Delta Airlines (DAL)": "DAL",
#     "United Airlines (UAL)": "UAL",
#     "Tata Steel (TATASTEEL.NS)": "TATASTEEL.NS",
#     "JSW Steel (JSWSTEEL.NS)": "JSWSTEEL.NS",
#     "Coal India (COALINDIA.NS)": "COALINDIA.NS"
# }

# # ------------------------------
# # 📉 Neon Themed Plot Function
# # ------------------------------
# def plot_stock(df):
#     plt.style.use('dark_background')
#     plt.figure(figsize=(10, 5))
#     plt.plot(df.index, df["Close"], label="Closing Price", color="#00ffff", linewidth=2.5)
#     plt.plot(df.index, df["Open"], label="Opening Price", color="#ff00ff", linewidth=2.5)
#     plt.xlabel("Date", color="#00ffff", fontsize=10)
#     plt.ylabel("Price", color="#00ffff", fontsize=10)
#     plt.title("📈 Stock Price Trend", color="#ff00ff", fontsize=14, weight='bold')
#     plt.legend(facecolor="#111", edgecolor="#0ff", labelcolor="#fff")
#     plt.grid(color="#333", linestyle="--", alpha=0.5)
#     plt.tick_params(colors="#0ff")
#     plt.gcf().patch.set_facecolor("#000")
#     buf = io.BytesIO()
#     plt.savefig(buf, format="png", bbox_inches="tight", facecolor="#000")
#     buf.seek(0)
#     plt.close()
#     return base64.b64encode(buf.getvalue()).decode("utf-8")

# # ------------------------------
# # 🔐 LOGIN SYSTEM
# # ------------------------------
# @app.route("/login", methods=["GET", "POST"])
# def login():
#     if request.method == "POST":
#         username = request.form["username"]
#         password = request.form["password"]
#         if username == "admin" and password == "1234":
#             session["user"] = username
#             return redirect(url_for("index"))
#         else:
#             return render_template("login.html", error="❌ Invalid username or password")
#     return render_template("login.html")

# @app.route("/logout")
# def logout():
#     session.pop("user", None)
#     return redirect(url_for("login"))

# # ------------------------------
# # 🧠 MAIN PAGE (Protected)
# # ------------------------------
# @app.route("/", methods=["GET", "POST"])
# def index():
#     if "user" not in session:
#         return redirect(url_for("login"))

#     data = None
#     img = None
#     prediction = None
#     ticker = None

#     if request.method == "POST":
#         ticker = request.form["ticker"]
#         start = request.form["start"]
#         end = request.form["end"]
#         df = yf.download(ticker, start=start, end=end)
#         if not df.empty:
#             data = df.tail(100).to_html(
#                 classes="table table-dark table-bordered table-hover",
#                 border=0
#             ).replace(
#                 '<table border="0" class="dataframe table table-dark table-bordered table-hover">',
#                 '<table class="dataframe table table-dark table-bordered table-hover" style="background-color:rgba(0,0,0,0.85); color:#00ffff; text-shadow:0 0 5px #00ffff;">'
#             )
#             img = plot_stock(df)
#             prediction = predict_stock(df)
#         else:
#             data = "❌ No data available for this selection."

#     return render_template(
#         "index.html",
#         stocks=STOCKS,
#         data=data,
#         img=img,
#         prediction=prediction,
#         ticker=ticker
#     )

# # ⚠️ Do NOT call app.run() — Vercel handles running the server.
