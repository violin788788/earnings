from sec_edgar_downloader import Downloader

dl = Downloader("YourCompanyName", "your@email.com")

# Download all 8-Ks for a ticker
dl.get("8-K", "AAPL", after="2022-01-01", before="2025-01-01")
