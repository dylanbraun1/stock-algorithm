from data_fetching import get_all_data

def apply_filters(stocks, params):
    filtered_stocks = {}
    for stock in stocks:
        data = get_all_data(stock)
        criteria = []

        if 'peg_ratio' in data and data['peg_ratio'] <= params.get('max_peg', 3):
            criteria.append('peg_ratio')
        if 'rsi' in data and data['rsi'] <= params.get('max_rsi', 80):
            criteria.append('rsi')
        if 'free_cash_flow' in data and data['free_cash_flow'] > 0:
            criteria.append('free_cash_flow')

        if len(criteria) == 3:  # Stock meets all criteria
            filtered_stocks[stock] = criteria

    return filtered_stocks

