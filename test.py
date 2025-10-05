import yfinance as yf
df = yf.download("TSLA", start="2024-01-01", end="2025-01-01")
print(df.head()) # pyright: ignore[reportOptionalMemberAccess]
