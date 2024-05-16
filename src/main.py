from filters import apply_filters

def main(stocks, params):
    print("Starting filtering process...")
    filtered_stocks = apply_filters(stocks, params)
    if filtered_stocks:
        for stock, criteria in filtered_stocks.items():
            print(f"{stock} meets the following criteria: {', '.join(criteria)}")
    else:
        print("No stocks met the criteria.")

if __name__ == "__main__":
    test_stocks = ["AAPL", "MSFT", "GOOGL", "AMZN", "TSLA"]
    params = {'max_peg': 2, 'max_rsi': 70}  # Consider adjusting these to be more inclusive for testing
    main(test_stocks, params)
